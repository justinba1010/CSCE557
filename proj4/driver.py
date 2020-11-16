#! /usr/bin/python3
"""
Justin Baum
16 November 2020
driver.py
Driver code for the quadratic sieve
"""
import argparse
from sys import exit
from math import sqrt

import defaults
from quadratic_sieve import quadratic_sieve

def main():
    """
    Driver Code
    """
    parser = argparse.ArgumentParser(description=
    """
    Single Polynomial Quadratic Sieve
    """
    )
    # Input File
    parser.add_argument(
        "-i",
        action="store",
        help="Input file",
    )
    # Output File
    parser.add_argument(
        "-o",
        action="store",
        help="Output file",
    )
    # Prime
    parser.add_argument(
        "-p",
        action="store",
        type=int,
        help="Input if no input file; ex: -p 15",
    )
    # Factor base size
    parser.add_argument(
        "-f",
        action="store",
        type=int,
        help=("Factor base size; default: {}".format(defaults.factorbase)),
    )
    # k
    parser.add_argument(
        "-k",
        action="store",
        type=int,
        help="K value size; default: {}".format(defaults.k),
    )
    args = parser.parse_args()
    o = args.o if args.o else "/dev/tty"
   
    with open(o, "w") as f:
        b = args.f if args.f else defaults.factorbase
        k = args.k if args.k else defaults.k
        # Check prime
        p = None
        if not args.i:
            if not args.p:
                f.write("No input given\n")
                exit(1)
            p = args.p
        else:
            with open(args.i, "r") as inputty:
                try:
                    p = int(inputty.readline())
                except _:
                    f.write("Input is not in file\n")
                    exit(1)
        factors = quadratic_sieve(p, b, k, f)
        f.write("The factors are: \n")
        for factor in factors:
            f.write("{}\n".format(factor))
        if len(factors) == 0:
            f.write("Unable to find factors\n")


if __name__ == "__main__":
    main()