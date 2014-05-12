import os
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random

def decrypt_valuables(f):
    # Get the private key and get associated hash digest size
    key = RSA.importKey(open('TOP_SECRET_KEYS/master_rsa').read())
    dsize = SHA.digest_size
    sentinel = Random.new().read(15+dsize)
    # Make a cipher object to decrypt with
    cipher = PKCS1_v1_5.new(key)
    # Decode the text
    decoded_text = cipher.decrypt(f, sentinel)
    # Grab the digest and if the digest is right, print the decrypted data
    digest = SHA.new(decoded_text[:-dsize]).digest()
    if digest==decoded_text[-dsize:]:
        # Remove the digest from the message
        decoded_text=decoded_text[:-dsize]
        decoded_text = str(decoded_text, 'ascii')
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
