from random import choice as rchoice
from math import sqrt, log
from board import Board
from copy import deepcopy

directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def sign(a):
	return (a > 0) - (a < 0)


def inbounds(coord):
	return 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7


def legal(b, p):
	flips = []
	if b.haspiece(p) or not p:
		return flips
	for d in directions:
		c = [p[0]+d[0], p[1]+d[1]]
		skipped = False
		tmp = []
		while inbounds(c):
			if not b.haspiece(c):
				break
			if b.color(c) == (not b.toplay):
				skipped = True
				tmp.append(tuple(c))
				c[0] += d[0]
				c[1] += d[1]
			else:
				if not skipped:
					break
				else:
					for t in tmp:
						flips.append(t)
					break
	return flips


def possible(b):
	rtn = []
	for x in range(8):
		for y in range(8):
			if not not legal(b, (x, y)):
				rtn.append((x, y))
	if not rtn:
		return [()]
	return rtn


def turn(b, p):
	if not p:
		b.endturn(p)
		return
	l = legal(b, p)
	if not l:
		return False
	b.place(p)
	for i in l:
		b.flip(i)
	b.endturn(p)


def end(b):
	return possible(b) == [()] and b.lastmove == ()


def buildchildren(root):
	poss = possible(root.board)
	for p in poss:
		tmp = deepcopy(root.board)
		turn(tmp, p)
		root.children.append(Node(tmp))


def mcbuildchildren(root):
	poss = possible(root.board)
	for p in poss:
		tmp = deepcopy(root.board)
		turn(tmp, p)
		root.children.append(MCNode(tmp, root))


def buildtree(root, n):
	if n == 0:
		return
	else:
		buildchildren(root)
		for node in root.children:
			buildtree(node, n - 1)


def mcbuildtree(root, n):
	if n == 0:
		return
	else:
		mcbuildchildren(root)
		for node in root.children:
			mcbuildtree(node, n - 1)


def addlayers(root, n):
	if n == 0:
		return
	if not root.children:
		buildchildren(root)
		for node in root.children:
			addlayers(node, n - 1)
	else:
		for node in root.children:
			addlayers(node, n - 1)


def mcaddlayers(root, n=2):
	if n == 0:
		return
	if not root.children:
		mcbuildchildren(root)
		for node in root.children:
			mcaddlayers(node, n - 1)
	else:
		for node in root.children:
			mcaddlayers(node, n - 1)


def score(board):
	sc = board.score()
	if end(board):
		if sc < 0:
			return -65
		elif sc > 0:
			return 65
		else:
			return 0
	else:
		return sc


def negamax(node, depth, color):
	if depth == 0 or node.children == []:
		return (node.board.lastmove, color * node.score)

	bestmove = ((), -66)
	for child in node.children:
		nr = negamax(child, depth - 1, -color)
		m = (nr[0], -nr[1])
		if m[1] > bestmove[1]:
			bestmove = (child.board.lastmove, m[1])
	return bestmove


def uct(node):
	return 10 if node.sims == 0 else 1 - node.wins / node.sims + sqrt(2 * log(node.parent.sims) / node.sims)


def simulation(node):
	# assert not node.children
	tmp = deepcopy(node.board)
	while not end(tmp):
		poss = possible(tmp)
		choice = rchoice(poss)
		turn(tmp, choice)
	sc = tmp.score()
	return sign(sc)


def selection(node):
	if not node.children:
		return node
	if node.sims == 0:
		return selection(rchoice(node.children))
	tmp = [uct(cn) for cn in node.children]
	m = tmp.index(max(tmp))
	return selection(node.children[m])


def backpropagation(node, p):
	node.sims += 1
	if node.board.toplay == Board.BLACK and p == 1:
		node.wins += 1
	elif node.board.toplay == Board.WHITE and p == -1:
		node.wins += 1
	if not node.parent:
		return
	else:
		backpropagation(node.parent, p)


def expansion(node):
	if node.sims > 15:
		mcbuildchildren(node)


class Node:
	def __init__(self, board):
		self.board = board
		self.children = []
		self.score = score(self.board)

	def printnode(self, prefix=""):
		print(prefix + str(self.board.lastmove) + " " + str(self.score))
		if not self.children:
			return
		else:
			for n in self.children:
				n.printnode(prefix + "-")


class MCNode(Node):
	def __init__(self, board, parent):
		super().__init__(board)
		self.parent = parent
		self.sims = 0
		self.wins = 0
