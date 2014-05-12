import os
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random

def decrypt_valuables(f):
    # TODO: For Part 2, you'll need to decrypt the contents of this file
    # The existing scheme uploads in plaintext
    # As such, we just convert it back to ASCII and print it out
    key = RSA.importKey(open('TOP_SECRET_KEYS/master_rsa').read())
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)
    cipher = PKCS1_v1_5.new(key)
    #decoded_text = str(f, 'ascii')
    decoded_text = cipher.decrypt(f, sentinel)
    digest = SHA.new(decoded_text[:-dsize]).digest()
    if digest==decoded_text[-dsize:]:
        print(decoded_text)
    else:
        print("Bad encryption")


if __name__ == "__main__": 
    fn = input("Which file in pastebot.net does the botnet master want to view? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    decrypt_valuables(f)
