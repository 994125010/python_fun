def make_rational(numer, denom):
    d = gcd(numer, denom)
    if d != 1:
        numer //= d
        denom //= d
    return lambda f: f(numer)(denom)
mr = make_rational

def gcd(x, y):
    return y if x % y == 0 else gcd(y, x % y)

def get_numer(r):
    return r(lambda num: lambda denom: num)
gn = get_numer

def get_denom(r):
    return r(lambda num: lambda denom: denom)
gd = get_denom

def mul(r1, r2):
    n1, d1 = get_numer(r1), get_denom(r1)
    n2, d2 = get_numer(r2), get_denom(r2)
    return make_rational(n1 * n2, d1 * d2)

def add(r1, r2):
    n1, d1 = get_numer(r1), get_denom(r1)
    n2, d2 = get_numer(r2), get_denom(r2)
    return make_rational(n1 * d2 + n2 * d1, d1 * d2)

def sub(r1, r2):
    n1, d1 = get_numer(r1), get_denom(r1)
    n2, d2 = get_numer(r2), get_denom(r2)
    return make_rational(n1 * d2 - n2 * d1, d1 * d2)

def div(r1, r2):
    n1, d1 = get_numer(r1), get_denom(r1)
    n2, d2 = get_numer(r2), get_denom(r2)
    return make_rational(n1 * d2, d1 * n2)

def print_r(r):
    n, d = get_numer(r), get_denom(r)
    nlen, dlen = len(str(n)), len(str(d))
    line, smaller = max(nlen, dlen), min(nlen, dlen)
    nspace, dspace = (line - smaller + 1) // 2, 0
    if nlen > dlen:
        nspace, dspace = dspace, nspace
    print(" " * nspace + str(n))
    if d != 1:
        print("-" * line)
        print(" " * dspace + str(d))
p = print_r

def rtod(r, digits=10):
    printed_digits = 0
    n, d = get_numer(r), get_denom(r)
    while printed_digits < digits:
        if n < d and printed_digits == 0:
            print("0.", end='')
        elif n == 0:
            printed_digits += digits
        else:
            count = 0
            while n >= d:
                n -= d
                count += 1
            print(count, end='')
        printed_digits += 1
        n *= 10
    print()


"""
print("Testing all basic functions...")
print("Making rational for '2 / 4'")
print_r(make_rational(2, 4))
print("Making rational for '123 / 3'")
print_r(make_rational(123, 3))
print("Testing addition of '1 / 2' and '1 / 3'...")
print_r(add(make_rational(1, 2), make_rational(1, 3)))
print("Testing subtraction of '1 / 2' and '2 / 3'...")
print_r(sub(make_rational(1, 2), make_rational(2, 3)))
print("Testing multiplication of '1 / 8' and '2 / 3'...")
print_r(mul(make_rational(1, 8), make_rational(2, 3)))
print("Testing division of '4 / 5' and '243 / 10'...")
print_r(div(make_rational(4, 5), make_rational(243, 10)))
"""

