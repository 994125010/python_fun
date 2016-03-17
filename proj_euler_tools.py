from math import *
from fractions import gcd

def memo(f):
    cache = {}
    def memoized(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return memoized

@memo
def Ackermann(m, n):
	if m == 0:
		return n+1
	if m > 0 and n == 0:
		return Ackermann(m-1, 1)
	if m > 0 and n > 0:
		return Ackermann(m-1, Ackermann(m, n-1))

def phi(n):
	count = 0
	for k in range(1, n):
		if gcd(k, n) == 1:
			count += 1
	if n == 1:
		count = 1
	return count


def fib_list(n):
	assert n > 2
	fib_list = [0, 1]
	for i in range(2, n+1):
		fib_list.append(fib_list[i-2]+fib_list[i-1])
	return fib_list

@memo
def fib(n):
	"""Returns the n-th fibonnacci number with n = 0 returning 0
	>>> fib(0)
	0
	>>> fib(1)
	1
	>>> fib(4)
	3
	"""
	if n == 0 or n == 1:
		return n
	if n == 2:
		return 1
	if n%2 == 0:
		return fib(n//2)*(2*fib(n//2+1)-fib(n//2))
	return fib(n//2+1)**2+fib(n//2)**2

def S_Eras(n):
	"""Produces an array with 1's in entries whose indices are prime up to the nth index
	and then produces an array with said indices to create a list of primes
	>>> S_Eras(4)
	[2, 3]
	>>> S_Eras(10)
	[2, 3, 5, 7]
	"""
	array = [1]*(n+1)
	array2 = []
	for i in range(0, n+1):
		if i == 0 or i == 1:
			array[i] = 0
		if array[i] == 1:
			for u in range(2*i, n+1, i):
				if array[u] != 0:
					array[u] = 0
			array2.append(i)
	return array2

def S_Sundaram(n):
	m = n//2
	array = [True for _ in range(m+1)]
	array2 = []
	for i in range(m + 1):
		for j in range(i, (m - i)/(2*i+1)+1):
			array[i+j+2*i*j] = False
	for k in array:
		if k is not False:
			array2.append(2*k+1)
	return array2
	

def primality(n):
	"""Returns True if n is prime
	>>> primality(32)
	False
	>>> primality(0)
	False
	>>> primality(1)
	False
	>>> primality(2)
	True
	>>> primality(73)
	True
	"""
	return n in S_Eras(n)

def nprime(n):
	"""Returns the nth prime with the 1st prime being 2
	>>> nprime(1)
	2
	>>> nprime(3)
	5
	>>> nprime(21)
	73
	"""
	if n in range (0, 25):
		return S_Eras(100)[n-1]
	approxprime = floor(2*((n-1)*log(n-1)))
	return S_Eras(approxprime)[n-1]

def is_square(n):
	"""Returns if n is a perfect square
	>>> is_square(0)
	True
	>>> is_square(2)
	False
	>>> is_square(256)
	True
	"""
	return sqrt(n) == floor(sqrt(n))

def summation(lower, upper, term):
	"""Returns a summation of terms of a function that gives the kth term in a sequence
	>>> summation(0, 10, lambda x: x)
	55
	"""
	total = 0
	for k in range(lower, upper+1):
		total += term(k)
	return total

def pro_div(n):
	"""Returns an array of the proper divisors, numbers less than n that divide n evenly, of n
	>>> pro_div(220)
	[1, 2, 4, 5, 10, 11, 20, 22, 44, 55, 110]
	>>> pro_div(1)
	[]
	>>> pro_div(12)
	[1, 2, 3, 4, 6]
	"""
	array = []
	for i in range(1, n//2+1):
		if n%i == 0:
			array.append(i)
	return array

def prime_div(n):
	"""Returns the prime divisors of n
	>>> prime_div(1)
	[]
	>>> prime_div(16)
	[2]
	>>> prime_div(42)
	[2, 3, 7]
	"""
	array = []
	pfactors = S_Eras(ceil(sqrt(n)))
	for f in pfactors:
		if n/f == n//f:
			array.append(f)
	return array

def lcm(a, b):
	"""Returns lowest common multiple of a and b"""
	if b>a:
		a, b = b, a
	if a%b == 0:
		return a
	afactors, bfactors, lcmfactors = pfactors(a), pfactors(b), {}
	lcm = 1
	for pfactor in afactors:
		lcmfactors[pfactor] = afactors[pfactor]
	for pfactor in bfactors:
		lcmfactors[pfactor] = max(lcmfactors.setdefault(pfactor, 1), bfactors[pfactor])
	for pfactor in lcmfactors:
		lcm *= pfactor**lcmfactors[pfactor]
	return lcm

def pfactors(n):
	"""Returns a dictionary of prime factors, with the powers of each factor"""
	pfactors = {}
	primes = S_Eras(n)
	for prime in primes:
		if n%prime == 0:
			k = 1
			while n%(prime**k) == 0:
				k += 1
			pfactors[prime] = k-1
	return pfactors

def factorial(n):
	"""Returns n factorial"""
	return gamma(n+1)

class Rational(object):
	def __init__(self, numer, denom):
		self.numerator = numer
		self.denominator = denom
		self.decimal = self.numerator/self.denominator
	def simplify(self):
		lols = gcd(self.numerator, self.denominator)
		self.numerator = self.numerator//lols
		self.denominator = self.denominator//lols

def add_rational(r1, r2):
	denom = lcm(r1, r2)
	numer = r1.numerator*denom//r1.denominator + r2.numerator*denom//r2.denominator
	return Rational(numer, denom)
