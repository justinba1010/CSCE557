"""
# Copyright 2020
# Justin Baum
# RSA Encryption
# CSCE557
"""
from sys import argv
import sys
from globally import BLOCKSIZE
def main():
    """
    # Encrypt plaintext
    """
    blocksize = BLOCKSIZE
    if len(argv) == 5:
        blocksize = int(argv[4])
    if len(argv) < 4:
        print("Please run program as 'python3 encrypt.py file key cipherfile'")
        sys.exit(1)
    plaintext = argv[1]
    key = argv[2]
    keyfile = open(key).read().split()
    e = int(keyfile[0])
    modulus = int(keyfile[1])
    ciphertext = argv[3]
    cipherfile = open(ciphertext, "wb")

    with open(plaintext, mode="rb") as plaintext:
        data = plaintext.read(blocksize)
        while data:
            data = data.ljust(blocksize, b'\0')
            data = int.from_bytes(data, "little")
            cipher_data = pow(data, e, modulus)
            cipherfile.write(cipher_data.to_bytes(blocksize*2, "little"))
            data = plaintext.read(blocksize)
        cipherfile.close()
        plaintext.close()



if __name__ == "__main__":
    main()
