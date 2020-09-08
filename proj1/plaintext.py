#! /usr/local/bin/python3
"""
Attempt to decipher using all the keys
"""


import sys
from decipher import substitute, KKEEP

def main():
    """
    Main routine
    """
    if len(sys.argv) < 2:
        print("Please enter a filename after, ./plaintext.py filename.txt")
        sys.exit(SystemExit(1))
    filename = sys.argv[1]
    words_in = open(filename).read().split()
    frequency = list("etaoinsrhdlucmfywgpbvkxqjz1234567890")
    if len(sys.argv) == 2:
        for i in range(KKEEP):
            key = list(open("key{}.txt".format(i)).read().split()[0])
            deciphered = []
            for word in words_in:
                deciphered.append(substitute(word, frequency, key))
            print("For key: {}, the plaintext may be: ".format("key{}.txt".format(i)))
            print(" ".join(deciphered))
    else:
        keyname = sys.argv[2]
        key = list(open(keyname).read().split()[0])
        deciphered = []
        for word in words_in:
            deciphered.append(substitute(word, frequency, key))
        print("For key: {}, the plaintext may be: ".format(keyname))
        print(" ".join(deciphered))

if __name__ == "__main__":
    main()
