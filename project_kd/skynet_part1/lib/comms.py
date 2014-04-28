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
            my_public_key, my_private_key = create_dh_key()
            # Send them our public key
            #self.send(str(bytes(str(my_public_key), "ascii")))
            self.send(str(my_public_key))
            # Receive their public key
            their_public_key = int(self.recv())
            # Obtain our shared secret
            self.shared_hash = calculate_dh_secret(their_public_key, my_private_key)
            if self.verbose:
                print("Shared hash: {}".format(self.shared_hash))
            self.shared_hash = bytes.fromhex(self.shared_hash)

        # Use AES in CFB mode for encryption
        iv = b'Sixteen byte vec'
        self.cipher = AES.new(self.shared_hash, AES.MODE_CFB, iv)

    def send(self, data):
        if type(data) != type(b""):
            data = bytes(data,'ascii')
        if self.verbose:
            print("Function 'send' received data",data,type(data))
	
	#Create a HMAC and prepend it to the message
        if self.shared_hash != None:
            h = HMAC.new(self.shared_hash)
            h.update(data)
            h.update(b'aaaa')
            if self.verbose:
                print("Hex digest is:",h.hexdigest())
            mac_data = h.hexdigest() + data.decode("ascii")
        else:
            mac_data = data
        if self.verbose:
            print("Data is now encoded with HMAC",mac_data,type(mac_data))
			
        if self.cipher:
            encrypted_data = self.cipher.encrypt(mac_data)
            if self.verbose:
                print("Original data: {}".format(data))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Sending packet of length {}".format(len(encrypted_data)))
        else:
            encrypted_data = mac_data #bytes(mac_data,"ascii")
            if self.verbose:
                print("Ecrypted data is just the same as data",type(encrypted_data))

        # Encode the data's length into an unsigned two byte int ('H')
        pkt_len = struct.pack('H', len(encrypted_data))
        if self.verbose:
            print("Sending packet length",pkt_len,type(pkt_len)) 
        self.conn.sendall(pkt_len)
        if self.verbose:
            print("Sending encrypted data:",encrypted_data,type(encrypted_data))
        self.conn.sendall(encrypted_data)


    def recv(self):
        while True:
			# Decode the data's length from an unsigned two byte int ('H')
            pkt_len_packed = self.conn.recv(struct.calcsize('H'))
            unpacked_contents = struct.unpack('H', pkt_len_packed)
            pkt_len = unpacked_contents[0]
            if self.verbose:
                print("Packet length is",pkt_len)

            encrypted_data = self.conn.recv(pkt_len)
            if self.verbose:
                print("Received Encrypted Data:",encrypted_data)
            if self.cipher:
                data = self.cipher.decrypt(encrypted_data)
                if self.verbose:
                    print("Receiving packet of length {}".format(pkt_len))
                    print("Encrypted data: {}".format(repr(encrypted_data)))
                    print("Original data: {}".format(data))
            else:
                data = encrypted_data
            if self.verbose:
                print("Decrypted Data:",data)

            #strip off the HMAC and verify the message
            if self.shared_hash != None:
                h = HMAC.new(self.shared_hash)
                hmac = data[:h.digest_size*2]
                data = data[h.digest_size*2:]
                h.update(data)
                if h.hexdigest() != str(hmac, 'ascii'):
                    print("Returning none...bad message?")
                    continue;     
            return data

    def close(self):
        self.conn.close()
