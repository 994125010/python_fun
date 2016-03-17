class Stack:
	"A FILO Container"
	def __init__(self, iterable=[]):
		self.items = [item for item in iterable]

	@property
	def size(self):
		return len(self.items)

	def push(self, e):
		self.items.append(e)

	def pop(self):
		if self.items:
			return self.items.pop()
		print(str(self)+" is empty")

	def isEmpty(self):
		return not self.items

class Queue:
	"A FIFO Container."
	def __init__(self, iterable=[]):
		self.items = [item for item in iterable]

	@property
	def size(self):
		return len(self.items)

	def push(self, e):
		self.items.append(e)

	def pop(self):
		if self.items:
			return self.items.pop(0)
		print(str(self)+" is empty")

	def isEmpty(self):
		return not self.items

class PriorityQueue:
	def __init__(self, iterable=[], priorityFunction=None):
		self.heap = BinaryHeap(iterable, priorityFunction) \
					if priorityFunction else BinaryHeap(iterable)

	@property
	def size(self):
		return self.heap.size

	def push(self, e):
		self.heap.push(e)

	def pop(self):
		if self.size:
			return self.heap.pop()
		print(str(self)+" is empty")

	def isEmpty(self):
		return not self.size

class BinaryHeap:
	_name = "BinaryHeap"
	def __init__(self, iterable=[], key=lambda e: e, \
				reverse=False, comparator=lambda a, b: a > b):
		from math import log
		if reverse:
			comparator = lambda a, b: a < b
		self.comp = comparator
		self.items = [item for item in iterable]
		self.items.insert(0, None) # Placeholder
		self.key = key
		length, items = len(self.items) - 1, self.items

		for parent in [len(self.items) - i for i in range(1, len(self.items))]:
			while 2 * parent < length:
				c1, c2 = 2 * parent, 2 * parent + 1
				if c1 < length:
					index, larger = c1, self.key(items[c1])
					if c2 < length:
						c2_val = self.key(items[c2])
						if comparator(c2_val, larger):
							index, larger = c2, c2_val
					if not comparator(self.key(items[parent]), larger):
						items[index], items[parent] = items[parent], items[index]
						parent = index
					else:
						break

	@property
	def size(self):
		return len(self.items) - 1

	def push(self, e):
		child, parent = len(self.items), len(self.items) // 2
		items = self.items
		items.append(e)
		while parent:
			if self.comp(self.key(items[child]), self.key(items[parent])):
				items[child], items[parent] = items[parent], items[child]
			child //= 2
			parent //= 2

	def pop(self):
		items = self.items
		length = len(items) - 1
		if length < 1:
			return print(self + " is empty") or None
		retval = items.pop(1)
		items.insert(1, items.pop())
		parent = 1
		while True:
			c1, c2 = 2 * parent, 2 * parent + 1
			if c1 < length:
				index, larger = c1, self.key(items[c1])
				if c2 < length:
					c2_val = self.key(items[c2])
					if self.comp(c2_val, larger):
						index, larger = c2, c2_val
				if not self.comp(self.key(items[parent]), larger):
					items[index], items[parent] = items[parent], items[index]
					parent = index
				else:
					return retval
			else:
				return retval

	def isEmpty(self):
		return not self.size

	def peek(self):
		if not self.isEmpty():
			return self.items[1]

	def __str__(self):
		from math import log
		if len(self.items) - 1 < 1:
			return "\n"
		depth = lambda i: int(log(i) // log(2))
		widest = max(list(map(lambda e: len(str(e)), self.items[1:])) or [0]) + 2 # spaces on both sides
		deepest = 2**depth(len(self.items) - 1)
		width = deepest * widest
		string = ''
		for d in range(depth(len(self.items)) + 1):
			line = ''
			for j in range(2**d):
				try:
					line += ('{:^'+str(width // (2**d))+'s}').format(str(self.items[2**d + j]))
				except:
					break
			line += '\n'
			for k in range(2**d):
				if 2**(d + 1) + 2*k < len(self.items):
					line += ('{:^'+str(width // (2**d))+'s}').format('_' * (width // 2**(d+2)) + \
							'|' + '_' * (width // 2**(d+2)))
			line += '\n'
			string += line
		return string[:len(string) - 1]

class BinaryTree:
	_name = "BinaryTree"
	def __init__(self, entry, left=None, right=None):
		self.entry = entry
		self.left = left
		self.right = right
		self.parent = None
		self._checkBT()
		if left: self.left.parent = self
		if right: self.right.parent = self

	def _checkBT(self):
		err_msg = "{0} child [{1}] is not a {2}"
		left, right = self.left, self.right
		if left:
			assert type(left) is type(self), \
				err_msg.format("Left", left, self._name)
		if right:
			assert type(right) is type(self), \
				err_msg.format("Right", right, self._name)

	@property
	def size(self):
		if self.isLeaf:
			return 1
		return 1 + self.left.size + self.right.size

	@property
	def isLeaf(self):
		return self.left is None and self.right is None

	@property
	def height(self):
		return 1 if self.isLeaf else \
			1 + max([x.height for x in (self.left, self.right) if x])

	@property
	def depth(self):
		return 0 if not self.parent else 1 + self.parent.depth

	def BFS(self):
		lst, fringe = [], [self]
		while fringe:
			curr = fringe.pop(0)
			if curr:
				fringe.append(curr.left)
				fringe.append(curr.right)
				lst.append(curr.entry)
		return lst

	def DFS(self):
		return [self.entry] if self.isLeaf else \
			((self.left.DFS() if self.left else []) + \
			[self.entry] + \
			(self.right.DFS() if self.right else []))

	def inOrder(self):
		return self.DFS()

	def preOrder(self):
		return [self.entry] if self.isLeaf else \
			([self.entry] + \
			(self.left.preOrder() if self.left else []) + \
			(self.right.preOrder() if self.right else []))

	def postOrder(self):
		return [self.entry] if self.isLeaf else \
			((self.left.postOrder() if self.left else []) + \
			(self.right.postOrder() if self.right else []) + \
			[self.entry])
	
	def __str__(self):
		return self._print(0)

	def _print(self, depth):
		s = ''
		if self.right:
			s += self.right._print(depth + 1)
		s += '   ' * depth + str(self.entry) + '\n'
		if self.left:
			s += self.left._print(depth + 1)
		return s

class BST(BinaryTree):
	_name = "BST"
	def __init__(self, entry, left=None, right=None):
		BinaryTree.__init__(self, entry, left, right)
		self._checkBST()

	def _checkBST(self):
		s = "BST property violated\n" + \
			str(self) + "\n" \
			"{0} child entry [{1}] at depth {2} {3} Ancestor entry [{4}] at depth {5}"
		left, right = self.left, self.right
		while left:
			assert self.entry >= left.entry, \
				s.format('Left', left.entry, left.depth, '>', self.entry, self.depth)
			left = left.right
		while right:
			assert self.entry <= right.entry, \
				s.format('Right', right.entry, right.depth, '<', self.entry, self.depth)
			right = right.left

class DisjointSet:

	class Set:
		def __init__(self, item):
			self.item = item
			self.parent = item
			self.rank = 0

	def __init__(self, iterable=[]):
		self.members = {}
		for item in iterable:
			self.makeset(item)

	def makeset(self, item):
		self.members[item] = self.Set(item)

	def union(self, a, b):
		aRoot, bRoot = self.find(a), self.find(b)
		if aRoot is not bRoot:
			if self.members[aRoot].rank > self.members[bRoot].rank:
				aRoot, bRoot = bRoot, aRoot
			self.members[aRoot].parent = bRoot
			if self.members[aRoot].rank > self.members[bRoot].rank:
				self.members[bRoot].rank += 1

	def find(self, a):
		setA = self.members[a]
		if setA.parent is not a:
			setA.parent = self.find(setA.parent)
		return setA.parent

	def __str__(self):
		matched = {}
		for k, v in self.members.items():
			root = self.find(k)
			if root not in matched:
				matched[root] = []
			matched[root].append(k)
		s = ''.join([' {'+str(i)+'}' for i in range(len(matched.keys()))])
		t = s.format(*(matched[key] for key in matched.keys()))
		return '{' + t + ' }'

print("DisjointSet Testing...\n")
d1, d2 = DisjointSet([1, 2, 3, 4]), DisjointSet()
print("d1:", d1, "d2:", d2)
d2.makeset(4)
d2.makeset(7)
d1.union(3, 4)
d1.union(1, 2)
print("d1:", d1, "d2:", d2)
d1.union(3, 1)
d1.makeset(10)
print("d1:", d1)
	
