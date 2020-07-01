import engine
from board import Board
from engine import Node, MCNode
from random import choice as rchoice
import time
from copy import deepcopy


class Player:
	def __init__(self, b):
		self.player = b

	def choosemove(self, lastmove, poss):
		return poss[0]


class Human(Player):
	def __init__(self, b):
		super().__init__(b)

	def choosemove(self, lastmove, poss):
		print(poss)
		move = [()]
		while move not in poss:
			moveinput = input("Select move: ")
			move = (int(moveinput[0]), int(moveinput[2]))
		return move


class RandomMove(Player):
	def __init__(self, b):
		super().__init__(b)

	def choosemove(self, lastmove, poss):
		return rchoice(poss)


class MoveList(Player):
	def __init__(self, b):
		super().__init__(b)
		self.mlist = [0, 0, 0, 0, 0, 0, 0] if b else [0, 0, 0, 0, 0, 0, 0]

	def choosemove(self, lastmove, poss):
		return poss[self.mlist.pop(0)]


class Minimax(Player):
	def __init__(self, b, depth=5, add=2, board=Board()):
		super().__init__(b)
		self.root = Node(deepcopy(board))
		self.depth = depth
		self.add = add
		self.first = True
		self.build()

	def build(self):
		engine.buildtree(self.root, self.depth)

	def choosemove(self, lastmove, poss):
		self.update(lastmove)
		result = engine.negamax(self.root, 100, 1 if self.player else -1)
		self.update(result[0])
		return result[0]

	def update(self, lastmove):
		if self.first and self.player == Board.BLACK:
			self.first = False
			return
		for child in self.root.children:
			if lastmove == child.board.lastmove:
				self.root = child
				break
		else:
			print("Failure Lastmove: ", lastmove)
			raise NameError("Update failed")
		engine.addlayers(self.root, self.add)


class MonteCarlo(Player):
	def __init__(self, b, depth=5, board=Board()):
		super().__init__(b)
		self.root = MCNode(deepcopy(board), None)
		engine.mcbuildtree(self.root, depth)
		self.first = True

	def choosemove(self, lastmove, poss):
		self.update(lastmove)
		start = time.perf_counter()
		for i in range(500):
			self.step()
			if i % 50 == 0:
				print(".", end="", flush=True)
		print()
		end = time.perf_counter()
		print(end-start)
		tmp = []
		for n in self.root.children:
			tmp.append(1 if n.sims == 0 else n.wins/n.sims)
			print("{0} {1:.2f}, {2}".format(n.board.lastmove, tmp[-1], n.sims))
			for n2 in n.children:
				print("-{0} {1:.2f}, {2}".format(n2.board.lastmove, -1 if n2.sims==0 else n2.wins/n2.sims, n2.sims))
		index = tmp.index(min(tmp))
		self.root = self.root.children[index]
		return self.root.board.lastmove

	def update(self, lastmove):
		if self.first and self.player == Board.BLACK:
			self.first = False
			return
		for child in self.root.children:
			if lastmove == child.board.lastmove:
				self.root = child
				break
		else:
			print("Failure Lastmove: ", lastmove)
			raise NameError("Update failed")
		self.root.parent = None
		engine.mcaddlayers(self.root, 2)

	def step(self):
		node = engine.selection(self.root)
		engine.expansion(node)
		win = engine.simulation(node)
		engine.backpropagation(node, win)
