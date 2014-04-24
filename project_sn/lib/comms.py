import struct

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA
import binascii

from dh import create_dh_key, calculate_dh_secret

class StealthConn(object):
    def __init__(self, conn, rsaKey, client=False, server=False, verbose=False):
        self.conn = conn
        self.cipher = None
        self.client = client
        self.server = server
        self.verbose = verbose
        self.rsaKey = rsaKey
        self.initiate_session()

    def initiate_session(self):
        # Perform the initial connection handshake for agreeing on a shared secret
        if not self.rsaKey:
            raise RuntimeError("Rsa key must be initialized")

        iv_length = AES.block_size
        dh_key_length = 256

        # client is the parent - has private rsaKey
        if self.client:
            if not self.rsaKey.has_private():
                raise RuntimeError("Client needs the private key")
            # initialize dh
            my_public_key, my_private_key = create_dh_key()
            # Receive the challenge from the child (iv g**a)
            encrypted_data = self.recv()
            tmpCipher = PKCS1_OAEP.new(self.rsaKey)
            decrypted_data = tmpCipher.decrypt(encrypted_data)
            if len(decrypted_data) < iv_length + 1 + dh_key_length:
                raise RuntimeError("Expected 'IV g**a'")
            self.iv = int.from_bytes(decrypted_data[:iv_length], byteorder='big')
            their_public_key = int.from_bytes(decrypted_data[iv_length+1:], byteorder='big')
            # Respond to the challenge by the child (iv g**b signed)
            msg_to_be_signed = decrypted_data[:iv_length] + b' ' + my_public_key.to_bytes(dh_key_length, byteorder='big')
            h = SHA.new()
            h.update(msg_to_be_signed)
            signer = PKCS1_PSS.new(self.rsaKey)
            signature = signer.sign(h)
            # send the signed message
            self.send(msg_to_be_signed + bytes(' ',"ascii") + signature)
            # Obtain our shared secret
            shared_hash = calculate_dh_secret(their_public_key, my_private_key)

        # server is the child - has public rsaKey
        if self.server:
            # Generate the IV
            self.iv = int.from_bytes(Random.new().read(iv_length), byteorder='big')
            # dh init
            my_public_key, my_private_key = create_dh_key()
            # send the challenge
            challenge = self.iv.to_bytes(AES.block_size, byteorder='big') + bytes(' ', "ascii") + my_public_key.to_bytes(dh_key_length, byteorder='big')
            tmpCipher = PKCS1_OAEP.new(self.rsaKey)
            encrypted_data = tmpCipher.encrypt(challenge)
            self.send(encrypted_data)
            # verify the response
            response = self.recv()
            if len(response) < iv_length + 1 + dh_key_length + 2:
                raise RuntimeError("Expected 'IV g**b signed'")
            iv = int.from_bytes(response[:iv_length], byteorder='big')
            if iv != self.iv:
                raise RuntimeError("IV given was incorrect, challenge failed")
            # verify the signature
            msg_to_be_verified = response[:(iv_length + 1 + dh_key_length)]
            signature = response[(iv_length + 1 + dh_key_length + 1):]
            h = SHA.new()
            h.update(msg_to_be_verified)
            signer = PKCS1_PSS.new(self.rsaKey)            
            if not signer.verify(h, signature):
                raise RuntimeError("Signature was incorrect, challenge failed")
            their_public_key = int.from_bytes(response[(iv_length+1):(dh_key_length + iv_length + 1)], byteorder='big')
            shared_hash = calculate_dh_secret(their_public_key, my_private_key)            

        print("Shared hash: {}".format(shared_hash))
        # set up AES cipher
        self.cipher = AES.new(shared_hash, AES.MODE_CFB, self.iv.to_bytes(iv_length, byteorder='big'));
        print("Authentication Successful")

    def send(self, data):
        if self.cipher:
            crc = binascii.crc32(data).to_bytes(4,'big')
            data = data + crc
            encrypted_data = self.cipher.encrypt(data)
            if self.verbose:
                print("Original data: {}".format(data))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Sending packet of length {}".format(len(encrypted_data)))
        else:
            encrypted_data = data

        # Encode the data's length into an unsigned two byte int ('H')
        pkt_len = struct.pack('H', len(encrypted_data))
        self.conn.sendall(pkt_len)
        self.conn.sendall(encrypted_data)

    def recv(self):
        # Decode the data's length from an unsigned two byte int ('H')
        pkt_len_packed = self.conn.recv(struct.calcsize('H'))
        try:
            unpacked_contents = struct.unpack('H', pkt_len_packed)
        except struct.error:
            return b''
        pkt_len = unpacked_contents[0]

        encrypted_data = self.conn.recv(pkt_len)
        if self.cipher:
            data = self.cipher.decrypt(encrypted_data)
            if self.verbose:
                print("Receiving packet of length {}".format(pkt_len))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Original data: {}".format(data))
            if len(data) < 5:
                self.close()
                print('CRC error')
                return b''
            crc = binascii.crc32(data[:-4]).to_bytes(4, 'big')
            if crc != data[-4:]:
                self.close()
                print('CRC error')
                return b''
            data = data[:-4]
        else:
            data = encrypted_data

        return data

    def close(self):
        self.conn.close()
