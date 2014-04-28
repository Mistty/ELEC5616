import struct

from Crypto import Random
from Crypto.Hash import HMAC
from Crypto.Cipher import AES
from lib.helpers import read_hex

from dh import create_dh_key, calculate_dh_secret

class StealthConn(object):
    def __init__(self, conn, client=False, server=False, verbose=False):
        self.conn = conn
        self.cipher = None
        self.client = client
        self.server = server
        self.verbose = verbose
        self.shared_hash = None
        self.initiate_session()

    def initiate_session(self):
        # Perform the initial connection handshake for agreeing on a shared secret

        ### TODO: Your code here!
        # This can be broken into code run just on the server or just on the client
        if self.server or self.client:
            print("about to initiate")
            my_public_key, my_private_key = create_dh_key()
            print("public key",my_public_key,"private key",my_private_key)
            # Send them our public key
            self.send(bytes(str(my_public_key), "ascii"))
            print("public key sent")
            # Receive their public key
            their_public_key = int(self.recv())
            print("public key recieved")
            # Obtain our shared secret
            self.shared_hash = calculate_dh_secret(their_public_key, my_private_key)
            print("Shared hash: {}".format(self.shared_hash))
            self.shared_hash = bytes(hex(read_hex(self.shared_hash)), "ascii")

        # Use AES in CFB mode for encryption
        iv = b'Sixteen byte vec'
        self.cipher = AES.new(self.shared_hash, AES.MODE_CFB, iv)

    def send(self, data):
		#Create a HMAC and prepend it to the message
        if self.shared_hash != None:
            h = HMAC.new(self.shared_hash)
            h.update(data)
            mac_data = h.hexdigest() + data
        else:
            mac_data = data
			
        if self.cipher:
            encrypted_data = self.cipher.encrypt(mac_data)
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
        unpacked_contents = struct.unpack('H', pkt_len_packed)
        pkt_len = unpacked_contents[0]

        encrypted_data = self.conn.recv(pkt_len)
        if self.cipher:
            data = self.cipher.decrypt(encrypted_data)
            if self.verbose:
                print("Receiving packet of length {}".format(pkt_len))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Original data: {}".format(data))
        else:
            data = encrypted_data

		#strip off the HMAC and verify the message
        if self.shared_hash != None:
            h = HMAC.new(self.shared_hash)
            hmac = data[:h.digest_size]
            data = data[h.digest_size:]
            h.update(data)
            if h.hexdigest() != hmac:
                return None	#Bad message - return none?
			
        return data

    def close(self):
        self.conn.close()
