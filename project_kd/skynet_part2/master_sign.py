import os
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

def sign_file(f):    
    # Read in the private key
    key = RSA.importKey(open(os.path.join("TOP_SECRET_KEYS", "master_rsa")).read())

    # sign using the RSASSA-PSS scheme
    # use a SHA-1 hasher for use in the RSA signing object
    h = SHA.new()
    h.update(f)
    signer = PKCS1_PSS.new(key)
    # create the signature and prepend it to the message
    signature = signer.sign(h)
    return signature + f


if __name__ == "__main__":
    fn = input("Which file in pastebot.net should be signed? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    signed_f = sign_file(f)
    signed_fn = os.path.join("pastebot.net", fn + ".signed")
    out = open(signed_fn, "wb")
    out.write(signed_f)
    out.close()
    print("Signed file written to", signed_fn)
