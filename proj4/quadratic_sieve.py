from math import sqrt, gcd
from sympy import Matrix

import defaults

"""
Not going to make this a parameter
It has cheaper operations right above the square root unless negative values are used

Instead of R + i being i in -k...k, it will be R + i i in 1 ... k
"""

kFROM0 = True

# pylint: disable=invalid-name

def prod(vector):
    x = 1
    for v in vector:
        x *= v
    return x

def factorsToExponentVector(f, factors):
    vector = [0 for _ in factors]
    for (i, factor) in enumerate(factors):
       while f % factor == 0:
           f /= factor
           vector[i] += 1
    if f != 1:
        return None
    return vector

def transposeMatrix(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def matrixMod2(matrix):
    # Positives only; optimized for & 1
    return [[val & 1 for val in row] for row in matrix]

def vectorMod2(vector):
    return [val % 2 for val in vector]

def sumVectors(vectors):
    m2 = transposeMatrix(vectors)
    m1 = [sum(v) for v in m2]
    return (m1)

def expVectorToProduct(vector, factors, N):
    prod = 1
    for (factor, exponent) in zip(factors, vector):
        prod *= pow(factor, exponent, N)
        prod %= N
    return prod

def divideVectorBy2(vector):
    return [x // 2 for x in vector]

def gaussian(matrix, f):
    # Compute nullspace vector
    # Not actually gaussian
    # Chooses least complex
    linalgmatrix = list(filter(lambda row: sum(row) != 0, matrix))
    try:
        solutions = []
        for sol in Matrix(linalgmatrix).nullspace():
            solutions.append(vectorMod2(list(sol)))
        solutions.sort(key=lambda x: sum(x))
        solution = solutions[0]
    except:
        f.write("The k value was not large enough\n")
        return None
    return [x % 2 for x in solution]

def quadratic_sieve(N, b, k, f):
    R = int(sqrt(N))
    k = min(R - 1, k)
    factors = defaults.primes[:b]
    if R**2 == N:
        return [R, R]
    L = [(R + i, pow(R + i, 2, N)) for i in range(1 if kFROM0 else -k, k + 1)]
    Lexp = [(r, factorsToExponentVector(l, factors)) for (r, l) in L]
    Lexp2 = list(filter(lambda x: x[1] != None, Lexp))
    Lexp3 = [x[1] for x in Lexp2]
    if (len(Lexp3) == 0):
        f.write("Not enough smooth numbers, make k or f larger\n")
    else:
        linearEquations = matrixMod2(transposeMatrix(Lexp3))
        solution = gaussian(linearEquations, f)
        if solution:
            values = []
            for (i, sol) in enumerate(solution):
                if sol:
                    values.append(Lexp2[i])
            vectors = [value[1] for value in values]
            magic_number = sumVectors(vectors)
            magic_number2 = prod([value[0] for value in values])
            magic_number = divideVectorBy2(magic_number)
            magic_number = expVectorToProduct(magic_number, factors, N)
            val1 = magic_number2 + magic_number
            val2 = magic_number2 - magic_number
            val1 %= N
            val2 %= N
            val1 = gcd(val1, N)
            val2 = gcd(val2, N)
            answers = []
            if N % val1 == 0:
                answers.append(val1)
                answers.append(N//val1)
            if N % val2 == 0:
                answers.append(val2)
                answers.append(N//val2)
            answers = list(set(answers))
            return answers
    return []
    