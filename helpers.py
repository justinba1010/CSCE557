def primitive_roots(g, n):
    roots = []
    for i in range(2,n):
        xs = []
        x = i
        while not (x in xs) and len(xs) < n:
            xs.append(x)
            x *= i
            x %= n
        if len(xs) == n - 1:
            roots.append(i)
    return roots

def five_23():
    return [(i,pow(5, 2*i, 23)) for i in range(23//2)]
