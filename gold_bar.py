# Write a program that given 3 coprime integers,
# returns the least number of cuts needed so that a
# gold bar can be split evenly by any of the integers

import sys
from itertools import combinations

def solve(a,b,c):
	prod = a * b * c
	nums = b * c, a * c, a * b
	find_parts(nums, prod)
	
def find_parts(nums, prod):
	nums = {n: prod//n for n in nums}
	atom = min(nums)
	parts = [atom]
	stack = [atom]
	prod -= atom
	while stack:
		print(parts)
		curr = stack.pop(0)
		for n in nums:
			potential = n - curr
			if potential == 33:
				print(curr, stack)
				print(parts)
				input()
			if atom > potential > 0 and potential not in parts:
				parts.append(potential)
				stack.append(potential)
	print(sorted(parts))
	print("!")

if __name__ == '__main__':
	solve(*map(lambda s: int(s), sys.argv[1:]))