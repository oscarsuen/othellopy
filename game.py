import engine
import players
from board import Board
import time
import matplotlib.pyplot as plt


class Game:
	def __init__(self):
		self.board = Board()

		self.pblack = players.MonteCarlo(Board.BLACK)
		self.pwhite = players.Minimax(Board.WHITE, 6, 3)

	def play(self):
		playing = 0
		while playing == 0:
			print(self.board)
			playing = self.move()
		return playing

	def move(self):
		poss = engine.possible(self.board)
		if poss == [()] and self.board.lastmove == ():
			sc = self.board.score()
			print("Score: ", sc)
			if sc < 0:
				print("White wins.")
				return -1
			elif sc > 0:
				print("Black wins.")
				return 1
			else:
				print("Tie.")
				return 2
		player = self.pblack if self.board.toplay else self.pwhite
		m = player.choosemove(self.board.lastmove, poss)
		print("Move: ", m)
		engine.turn(self.board, m)
		return 0


if __name__ == '__main__':
	n = 5
	ct = [0]
	start = time.perf_counter()
	for i in range(n):
		g = Game()
		j = g.play()
		ct.append(ct[-1] + (j if not j == 2 else 0))
	end = time.perf_counter()
	print("Av Time: ", (end-start)/n)
	print("Final: ", ct[-1])
	if n > 1:
		plt.plot(ct)
		plt.show()
	# n = 5000
	# ct = [0]
	# node = engine.MCNode(Board(),None)
	# start = time.perf_counter()
	# for i in range(n):
	# 	ct.append(ct[-1] + engine.simulation(node))
	# end = time.perf_counter()
	# print("Av Time: ", (end-start)/n)
	# print("Final: ", ct[-1])
	# plt.plot(ct)
	# plt.show()
