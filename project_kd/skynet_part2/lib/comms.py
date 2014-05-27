# Randomly added line
import struct
import datetime

from Crypto import Random
from Crypto.Hash import HMAC
from Crypto.Cipher import AES
from lib.helpers import read_hex

from dh import create_dh_key, calculate_dh_secret

# Format the time stamp to the milliseconds for preventing replay attacks
timestamp_format = "%Y-%m-%d %H:%M:%S:%f"
timestamp_format_len = 26

class StealthConn(object):
    def __init__(self, conn, client=False, server=False, verbose=False):
        self.conn = conn
        self.cipher = None
        self.client = client
        self.server = server
        self.verbose = verbose
        self.shared_hash = None
        self.last_message_time = datetime.datetime.now()
        self.initiate_session()

    def initiate_session(self):
        # Perform the initial connection handshake for agreeing on a shared secret
        if self.server or self.client:
            my_public_key, my_private_key = create_dh_key()
            # Send them our public key
            self.send(str(my_public_key))
            # Receive their public key
            their_public_key = int(self.recv())
            # Obtain our shared secret
            self.shared_hash = calculate_dh_secret(their_public_key, my_private_key)
            if self.verbose:
                print("Shared hash: {}".format(self.shared_hash))
            self.shared_hash = bytes.fromhex(self.shared_hash)

        # Use AES in CFB mode for encryption
        iv = self.shared_hash[:16] # set the initialization vector
        self.cipher = AES.new(self.shared_hash, AES.MODE_CFB, iv) # create cipher object

    def send(self, data):
        # Sort out encoding problems
        if type(data) != type(b""):
            data = bytes(data,'ascii')
        if self.verbose:
            print("Function 'send' received data",data,type(data))
	
        #Create a HMAC and prepend it to the message
        if self.shared_hash != None:
            h = HMAC.new(self.shared_hash)
            h.update(data)
            if self.verbose:
                print("Hex digest is:",h.hexdigest())
            mac_data = bytes(h.hexdigest(),"ascii") + data
            # Use the following code if you want to test what happens when the HMAC is bad
            #mac_data = h.hexdigest()[:-1] + "a"  + data.decode("ascii") # replace a random character in the digest
        else:
            mac_data = data
        if self.verbose:
            print("Data is now encoded with HMAC",mac_data,type(mac_data))
        
        # Add a timestamp to the message
        current_time = datetime.datetime.now()
        # Use the following code to test if it works: subtract some time from now
        #current_time = self.last_message_time - datetime.timedelta(1,0) # Take away a day from the last recieved message
        timestr = datetime.datetime.strftime(current_time, timestamp_format) #format the timestamp
        mac_data = bytes(timestr, 'ascii') + mac_data # prepend it to the message
			
        if self.cipher:
            encrypted_data = self.cipher.encrypt(mac_data) #Encrypt the message
            if self.verbose:
                print("Original data: {}".format(data))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Sending packet of length {}".format(len(encrypted_data)))
        else:
            encrypted_data = mac_data
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
        # Decode the data's length from an unsigned two byte int ('H')
        pkt_len_packed = self.conn.recv(struct.calcsize('H'))
        unpacked_contents = struct.unpack('H', pkt_len_packed)
        pkt_len = unpacked_contents[0]
        if self.verbose:
            print("Packet length is",pkt_len)

        encrypted_data = self.conn.recv(pkt_len) # Recieve the message
        if self.verbose:
            print("Received Encrypted Data:",encrypted_data)
        if self.cipher:
            data = self.cipher.decrypt(encrypted_data) # Decrypt the message
            if self.verbose:
                print("Receiving packet of length {}".format(pkt_len))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Original data: {}".format(data))
        else:
            data = encrypted_data
        if self.verbose:
            print("Decrypted Data:",data)

        #strip off the HMAC and timestamp and verify the message
        
        #take off the timestamp first
        tstamp = str(data[:timestamp_format_len], 'ascii')
        data = data[timestamp_format_len:]
        
        #get the HMAC, if we're using one
        if self.shared_hash != None:
            h = HMAC.new(self.shared_hash)
            hmac = data[:h.digest_size*2] #Get the HMAC part of the message
            data = data[h.digest_size*2:] # Get the data part of the message
            h.update(data)
            if h.hexdigest() != str(hmac, 'ascii'): #HMAC is not right, so raise an error
                if self.verbose:
                    print("Bad message")
                    print("HMAC from message:",str(hmac,'ascii'))
                    print("HMAC from digest:",h.hexdigest())
                    print("Not verifying message:",data)
                raise RuntimeError("Bad message: HMAC does not match")
        elif self.verbose:
            print("Shared hash is null")
        
        #we'll only accept messages that have timstamps after the one we last recieved
        msg_time = datetime.datetime.strptime(tstamp, timestamp_format);
        if self.verbose:
            print(msg_time)
        if msg_time <= self.last_message_time: #If the timestamp is not newer, then raise an error
            if self.verbose:
                print("Bad timestamp")
                print("timestamp:",tstamp)
            raise RuntimeError("Bad timestamp: message not newer than last recieved one")

        self.last_message_time = msg_time # Update message time
                 
        return data

    def close(self):
        self.conn.close()
