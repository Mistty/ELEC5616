import os
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def decrypt_valuables(f, rsaKey):
    encrypted_text = f
    if len(encrypted_text) % 512 != 0:
        raise RuntimeError("Encrypted text should be in 512 byte blocks, length is " + str(len(encrypted_text)))
    if not rsaKey.has_private():
        raise RuntimeError("Need Private Key")
    decoded_text = ''
    tmpCipher = PKCS1_OAEP.new(rsaKey)
    for i in range(int(len(encrypted_text)/512)):
        decoded_text += tmpCipher.decrypt(encrypted_text[(512*i):(512*(i+1))]).decode("utf-8")
    print(decoded_text)

if __name__ == "__main__":
    fn = input("Which file in pastebot.net does the botnet master want to view? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    fkey = open("clientPrivate.pem", 'r')
    rsaKey = RSA.importKey(fkey.read())
    fkey.close()    
    decrypt_valuables(f, rsaKey)
