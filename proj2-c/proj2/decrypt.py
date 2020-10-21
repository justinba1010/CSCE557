"""
# Copyright 2020
# Justin Baum
# RSA Decryption
# CSCE557
"""
from sys import argv
import sys
from globally import BLOCKSIZE

def main():
    """
    # Decrypt plaintext
    """
    blocksize = BLOCKSIZE
    if len(argv) == 5:
        blocksize = int(argv[4])
    if len(argv) < 4:
        print("Please run program as 'python3 decrypt.py cipherfile key decryptedfile'")
        sys.exit(1)
    cipherfile = argv[1]
    key = argv[2]
    keyfile = open(key).read().split()
    d = int(keyfile[0])
    modulus = int(keyfile[1])
    plaintext = argv[3]
    plainfile = open(plaintext, "wb")
    with open(cipherfile, "rb") as ciphertext:
        data = ciphertext.read(blocksize*2)
        while data:
            data = int.from_bytes(data, "little")
            decrypted = pow(data, d, modulus)
            plainfile.write(decrypted.to_bytes(blocksize, "little"))
            data = ciphertext.read(BLOCKSIZE*2)
        plainfile.close()
        ciphertext.close()
    # Strip trailing \x00
    plainfile = open(plaintext, "rb").read()
    while plainfile[-1] == 0:
        plainfile = plainfile[:-1]
    plainfile2 = open(plaintext, "wb")
    plainfile2.write(plainfile)
    plainfile2.close()


if __name__ == "__main__":
    main()
