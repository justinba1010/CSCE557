"""
# Copyright 2020
# Justin Baum
# RSA Core Algorithm
# CSCE557

# Written in a functional style, because
"""

from random import randint
from math import sqrt, gcd
from globally import * # pylint: disable=unused-wildcard-import wildcard-import

# DEBUG
DEBUG = False

def lcm(a, b):
    # pylint: disable=invalid-name
    """
    # Why is this not in the stdlib
    """
    return abs(a*b) // gcd(a, b)

def print_d(x):
    # pylint: disable=invalid-name
    """
    # Debug print
    """
    if DEBUG:
        print(x)

def generate_prime_candidates(limit):
    """
    # Optimization
    # Primes take the form of 6n + 1 or 6n - 1, we can find other
    # through Dirichlet's Theorem, so find a random candidate to be prime
    # We want some level of redundancy, to ensure we do not generate primes
    # that are too small
    #
    # The redundant bytes allow us to ensure that we end up with a totient that is
    # is large enough for application
    """
    (residue_class, sieve, redundantbytes) = DIRICHLETSIEVE
    lower_bound = limit  // residue_class >> redundantbytes
    upper_bound = limit // residue_class
    candidate_multiple = randint(lower_bound, upper_bound) * residue_class
    return [candidate_multiple + i for i in sieve]

def fermat_primality_test(num):
    """
    # We have to be careful for Carmichael numbers
    # Probability is pretty decent for primes up to 40
    """

    # We use the pow method here because we want fast modulo exponentiation
    # Just like the fast exponentiation algorithm with squaring and multiplying,
    # just over a field, with modulo.
    if num < SIEVELIMIT:
        return sieve_erasthothenes(num)
    return all([pow(i, num - 1, num) == 1\
            and (EXTRASAFETY or sieve_erasthothenes(num))\
            for i in FERMATTEST])

def generate_prime(limit):
    """
    # Generate a random prime
    """
    while True:
        candidates = generate_prime_candidates(limit)
        for i in candidates:
            if fermat_primality_test(i):
                return i

def sieve_erasthothenes(num):
    """
    # For testing our probabilistic prime generation
    """
    limit = int(sqrt(num)) + 1
    numbers = list(range(2, limit + 1))
    while len(numbers) > 0:
        print_d(numbers)
        prime = numbers.pop()
        if num % prime == 0:
            return False
        numbers = list(filter(lambda a: a % prime != 0, numbers))
    return True

def test(trials, limit):
    """
    # Test for my own sanity
    """
    primes = [generate_prime(limit) for _ in range(trials)]
    print_d(primes)
    return all([sieve_erasthothenes(i) for i in primes])

def multiplicative_inverse(a, field):
    # pylint: disable=invalid-name
    """
    # Stripped down ext Euclid Algorithm, iterative, because doing look ahead
    # is just extra steps
    """
    original_field = field
    y = 0
    x = 1
    if field <= 1:
        return 0

    while a > 1:
        quotient = a // field
        (a, field) = (field, a % field)
        (x, y) = (y, x - quotient * y)
    return x % original_field

def generate_key(limit):
    # pylint: disable=invalid-name
    """
    # Generate the key
    """

    # Wikipedia says these two primes should have a few bits
    # difference in length. This is where I use the redundancy bits.
    # I can see why with small numbers.
    # Originally I was getting prime pairs such as 19 and 19. Where
    # Just a normal square root gave you the prime factorization.
    # Square roots can be calculated exceptionally fast, and having
    # two primes close to each other can lead to problems.
    p1 = generate_prime(limit)
    p2 = p1
    while p2 == p1:
        p2 = generate_prime(limit)
    print_d("Prime %s, %s " % (p1, p2))
    modulus = p1 * p2
    totient = lcm((p1 - 1), (p2 - 1))
    # Find a coprime
    e = totient
    while gcd(e, totient) != 1:
        e = randint(totient//2, totient)
    d = multiplicative_inverse(e, totient)
    return (e, modulus, d)
