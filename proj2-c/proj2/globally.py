"""
# Copyright 2020
# Justin Baum
# RSA globals
# CSCE557
"""

"""
RSA 1024 -> 128 byte blocksize
RSA 2048 -> 256 byte blocksize
RSA 4096 -> 512 byte blocksize
"""

BLOCKSIZE = 128 # bytes
PRIMESIZE = BLOCKSIZE*4 ## bits

"""
Toggling EXTRASAFETY means adding a sieve of erasthothenes. However, the list of numbers is too large and python just crashes. If using a small prime,it can work.
"""

EXTRASAFETY = False
DIRICHLETSIEVE = (6, [1,5], BLOCKSIZE) # BLOCKSIZE is primesize/8
FERMATTEST = [2,3,5,7,11,13,17,23,29,31,37,39]
SIEVELIMIT = 41
