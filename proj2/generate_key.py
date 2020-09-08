"""
# Copyright 2020
# Justin Baum
# RSA Key Generation
# CSCE557
"""
from sys import argv
import base64 as b64
import rsa
from globally import * # pylint: disable=unused-wildcard-import

def main():
    """
    # Generate a key and place into file
    """
    primesize = PRIMESIZE
    if len(argv) == 4:
        primesize = int(argv[3])
    if len(argv) < 3:
        print("Please run program as 'python3 generate_key.py public_key private_key'")
        exit(1)
    public_file = argv[1]
    private_file = argv[2]
    limit = (1 << primesize) - 1
    (e, modulus, d) = rsa.generate_key(limit)
    f = open(public_file, "w")
    f.write(str(e) + "\n" + str(modulus) + "\n")
    f.close()
    f = open(private_file, "w")
    f.write(str(d) + "\n" + str(modulus) + "\n")

if __name__ == "__main__":
    main()
