def dp(arr, k):
	A = [0]*(len(arr)+k)
	for i,c in enumerate(arr):
		prev = A[i:i+k]
		A[i+k] = c + min(A[i:i+k])
	return min(A[-k:])

def lin(arr, k):
	A = [0]*(len(arr)+k)
	b = A[:k]
	m = 0
	for i,c in enumerate(arr):
		A[i+k] = c + m
		removed = b.pop(0)
		b.append(A[i+k])
		if removed == m:
			m = min(b)
	return min(A[-k:])

print(lin([1,2,3,4,3,5,2,3,1,1,2,3,5], 4))