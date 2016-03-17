import random

def edmonds_karp(C, E, s, t):
    """ Returns the max flow and flow matrix (f and F), of a graph G.
    C[u][v] is the capacity of the edge (u, v)
    E[u] is a list of all the edges from vertex u
    f is the value of the max flow from s to t
    F[u][v] is the flow of the edge (u, v)
    """
    f, F = 0, [[0 for _ in range(len(E))] for _ in range(len(E))]
    while True:
        m, P = bfs(C, E, s, t, F)
        if m == 0: break
        f += m
        v = t
        while v != s:
            u = P[v]
            F[u][v] += m
            F[v][u] -= m
            v = u
    return f, F

def bfs(C, E, s, t, F):
    """ BFS Algorithm with additional parameters for edmonds_karp. """
    maxf, prev = {}, {}
    for edge in E:
        prev[edge] = -1
    maxf[s], prev[s] = float('inf'), -2
    Q = Queue()
    Q.enqueue(s)
    while Q.size() > 0:
        u = Q.dequeue()
        for v in E[u]:
            residual_capacity = C[u][v] - F[u][v]
            if residual_capacity > 0 and prev[v] == -1:
                prev[v] = u
                maxf[v] = min(maxf[u], residual_capacity)
                if v != t:
                    Q.enqueue(v)
                else:
                    return maxf[t], prev
    return 0, prev



class ArrayList:
    """ ArrayList that supports constant time append given constant time malloc. """
    def __init__(self, iterable=[0]*16):
        self.items = iterable
        self._new_items = None
        self.size = 0
        self.capacity = len(self.items)

    def __getitem__(self, index):
        if index < self.size:
            return self.items[index]
        raise IndexError

    def append(self, item):
        if self.size * 2 == self.capacity:
            self._new_items = [0] * self.capacity * 2
        if self.size * 2 >= self.capacity:
            self.items[self.size] = item
            self._new_items[self.size - self.capacity // 2] = self.items[self.size - self.capacity // 2]
        if self.size == self.capacity:
            self.items = self._new_items
        self.items[self.size] = item
        self.size += 1

class Sudoku:

    r = range(1, 10)

    def __init__(self, board = [[0]*9 for _ in range(9)]):
        self.variables = [self.var(n, i, j) \
                            for i in self.r \
                            for j in self.r \
                            for n in self.r]
        self.board = board
        self.clauses = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j]:
                    self.clauses.append("ASSERT( " + \
                            self.var(self.board[i][j], i+1, j+1) + " );\n")
        self.unique = '( {0}' + ''.join([' AND (NOT({'+str(i)+'})' \
                        for i in range(1, 9)]) + ')'*9
        for num in self.r:
            for i in self.r:
                self.clauses.append(self.unique_in_row(i, num))
                self.clauses.append(self.unique_in_col(i, num))
            for row in (1, 4, 7):
                for col in (1, 4, 7):
                    self.clauses.append(self.unique_in_reg(num, row, col))
        for i in self.r:
            for j in self.r:
                self.clauses.append(self.unique_in_cell(i, j))

    def write(self):
        f = open('sudoku_stp.in', 'w', newline='\n')
        f.write(self.declare_vars())
        for c in self.clauses:
            f.write(c)
        f.close()
    
    def var(self, n, i, j):
        return str(n) + '@' + str(i) + str(j)

    def unique_in(self, variables):
        s = 'ASSERT'
        for v in variables:
            args = [v] + list(filter(lambda s: s != v, variables))
            s += self.unique.format(*args) + ' OR ('
        return s[:-5] + ')' * 8 + ';\n'

    def unique_in_row(self, row, num):
        """row has exactly one of num"""
        return self.unique_in([self.var(num, row, j) for j in self.r])

    def unique_in_col(self, col, num):
        """col has exactly one of num"""
        return self.unique_in([self.var(num, j, col) for j in self.r])

    def unique_in_reg(self, num, row, col):
        """3x3 region with top left at (row, col) and has exactly one of num"""
        return self.unique_in([self.var(num, row+i, col+j) \
                for i in range(3) for j in range(3)])

    def unique_in_cell(self, row, col):
        """only one number in row, col"""
        return self.unique_in([self.var(j, row, col) for j in self.r])

    def declare_vars(self):
        """returns the string that declares boolean variables"""
        return ''.join([v+', ' for v in self.variables])[:-2] + ' : BOOLEAN;\n'

def hw10():
    s = Sudoku([[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 8, 5],
            [0, 0, 1, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 7, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 1, 0, 0],
            [0, 9, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 7, 3],
            [0, 0, 2, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 9]])

import sys

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("hw12part1", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

def hw12():
    import csv
    import numpy as np
    import heapq
    PATH = lambda part, data: 'hw12data/{0}/{1}.csv'.format(part, data)
    PART1 = 'digitsDataset'
    PART2 = 'emailDataset'
    TRAIN_FEATS, TRAIN_LABELS = 'trainFeatures', 'trainLabels'
    VALID_FEATS, VALID_LABELS = 'valFeatures', 'valLabels'
    TESTS = 'testFeatures'

    def getData(part, data):
        return np.asarray([np.asfarray(e) for e in csv.reader(open(PATH(part, data)))])

    def getTraining(part):
        return getData(part, TRAIN_FEATS), getData(part, TRAIN_LABELS)

    def getValidation(part):
        return getData(part, VALID_FEATS), getData(part, VALID_LABELS)

    def k_nearest(k, data, candidate):
        #print("Calculating distances...", end=' ')
        candidate = np.asfarray(candidate)
        # nearest, stored = [], 0
        # enum = enumerate(data)
        # for i, feat in enum:
        #     diff = candidate - feat
        #     heapq.heappush(nearest, (-diff.dot(diff), i))
        #     if i == k - 1:
        #         break
        # for i, feat in enum:
        #     diff = candidate - feat
        #     heapq.heappush(nearest, (-diff.dot(diff), i))
        #     heapq.heappop(nearest)
        # return [i for diff, i in nearest]
        distances = np.sum((data-candidate)**2, axis=1)
        return np.argsort(distances, axis=0)[:k]

    def majority(nearest, labels):
        #print("Deciding majority...")
        votes = [labels[neighbour] for neighbour in nearest]
        return max(votes, key=lambda c: votes.count(c))

    def part1():
        sys.stdout = Logger()
        train_feats, train_labels = getTraining(PART1)
        print("Training done. ", end="")
        val_feats, val_labels = getValidation(PART1)
        bestk, bestscore = 1, 0
        for k in (1, 2, 5, 10, 25):
            print("Checking validation on k =", k)
            successes = 0
            for i, candidate in enumerate(val_feats):
                print("Matching candidate {0}/{1}".format(i+1, len(val_feats)), end='\r')
                guess = majority(k_nearest(k, train_feats, candidate), train_labels)
                if guess == val_labels[i]:
                    successes += 1
            score = successes/len(val_feats)
            print("\nSuccess Rate: {0}".format(score))
            if score > bestscore:
                bestk, bestscore = k, score
        print("Best kNN: k = {0}".format(bestk))

    part1()

def multiply_20_steps(x, y):
    "GIven addition, subtraction, inverse"
    def square(x):
        if x != -1:
            """
            x           ->      1/x
            x           ->      x+1
            x+1         ->      1/(x+1)
            1/x-1/(x+1) ->      1/(x^2+x)
            1/(x^2+x)   ->      x^2+x
            x^2+x       ->      x^2
            """
    """
    x, y                    ->          x + y
    x, y                    ->          x - y
    (x + y)                 ->          (x + y)^2
    (x - y)                 ->          (x - y)^2
    (x + y)^2 - (x - y)^2   ->          4xy
    4xy                     ->          1/4xy
    1/4xy + 1/4xy           ->          2/4xy
    2/4xy + 2/4xy           ->          4/4xy
    1/xy                    ->          xy
    """



