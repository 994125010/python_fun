# These are very primitive functions
zero = lambda f: lambda x: x
successor = lambda n: lambda f: lambda x: f(n(f)(x))
one = successor(zero)

# This might get used
curry = lambda f: lambda x: lambda y: f(x)(y)

# This is used to actually interact with Church numerals
ctoi = lambda c: c(lambda s: s + 1)(0)
itoc = lambda i: zero if i == 0 else successor(itoc(i - 1))

# Boolean Primitives
cond = curry
true = lambda t: lambda f: t
false = lambda t: lambda f: f

# Fancy combinator
ycomb = lambda f: lambda arg: f(f)(arg)

# Pair Constructs
cons = lambda a: lambda b: lambda m: m(a)(b)
car = lambda p: p(lambda a: lambda b: a)
cdr = lambda p: p(lambda a: lambda b: b)

# Anonymous Factorial
factorial = lambda n: ycomb(lambda f: lambda n: 1 if n == 0 else n * f(f)(n -
1))(n)

# Arithmetic Operators
add = lambda c1: lambda c2: c1(successor)(c2)
mul = lambda c1: lambda c2: lambda f: lambda x: c1(c2(f))(x)
sub = lambda c1: lambda c2: c2(predecessor)(c1)
predecessor = lambda n: cdr(n((lambda p: cons(successor(car(p)))(
car(p))))(cons(zero)(zero)))

# NOT WORKING
pow = lambda b: lambda e: e(mul(b))(one)
tetra = lambda b: lambda e: e(pow(b))(b)

# Boolean Operators
AND = lambda b1: lambda b2: b1(b2)(b1)
OR = lambda b1: lambda b2: b1(b1)(b2)
NOT = lambda b: b(false)(true)
XOR = lambda b1: lambda b2: b1(NOT(b2))(b2)
EQUALS = lambda b1: lambda b2: NOT(XOR(b1)(b2))

# Interact with Booleans
ltob = lambda b: b(True)(False)

# Comparators
equals_zero = lambda c: c(lambda x: false)(true)
leq = lambda small: lambda big: equals_zero(sub(small)(big))
geq = lambda big: lambda small: leq(small)(big)
equals = lambda c1: lambda c2: AND(leq(c1)(c2))(geq(c1)(c2))

# WIP
floor = lambda tbd: lambda divider: (lambda fn: lambda a: lambda b:
fn(fn)(a)(b))(lambda f: lambda p: lambda q:
(geq(p)(q))(successor(f(f)(sub(p)(q))(q)))(zero))(tbd)(divider)
mod = lambda a: lambda m: (lambda fn: lambda x: lambda y:
fn(fn)(x)(y))(lambda f: lambda c: lambda d: (geq(c)(d))(f(f)(sub(c)(d))(d))(c))(a)(m)

