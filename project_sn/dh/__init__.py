from Crypto.Hash import SHA256
from Crypto.Random import random

from lib.helpers import read_hex

# Project TODO: Is this the best choice of prime? Why? Why not? Feel free to replace!

# 2048 bit safe prime for Diffie-Hellman key exchange
# obtained from RFC 3526
raw_prime = """FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF"""

# Convert from the value supplied in the RFC to an integer
prime = read_hex(raw_prime)

# Project TODO: write the appropriate code to perform DH key exchange

def create_dh_key():
    # Creates a Diffie-Hellman key
    # Returns (public, private)
    a = random.randint(0, int(2**2047))
    return (pow(2,a,prime), a)

def calculate_dh_secret(their_public, my_private):
    # Calculate the shared secret
    shared_secret = pow(their_public, my_private, prime).to_bytes(256, byteorder = 'big')

    # Hash the value so that:
    # (a) There's no bias in the bits of the output
    #     (there may be bias if the shared secret is used raw)
    # (b) We can convert to raw bytes easily
    # (c) We could add additional information if we wanted
    # Feel free to change SHA256 to a different value if more appropriate
    shared_hash = int(SHA256.new(shared_secret).hexdigest(),16).to_bytes(32, byteorder='big')
    return shared_hash
