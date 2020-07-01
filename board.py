class Board:
	# Players: True, 1 = Black, x; False, -1 = White, o
	BLACK = True
	WHITE = False

	def __init__(self):
		self.toplay = Board.BLACK
		self.lastmove = ()
		self.list0 = [[False for x in range(8)] for y in range(8)]
		self.list1 = [[Board.WHITE for x in range(8)] for y in range(8)]

		self.list0[3][3] = True
		self.list0[3][4] = True
		self.list0[4][3] = True
		self.list0[4][4] = True

		self.list1[3][3] = Board.WHITE
		self.list1[3][4] = Board.BLACK
		self.list1[4][3] = Board.BLACK
		self.list1[4][4] = Board.WHITE

	def __repr__(self):
		rtn = "---------------\n"
		rtn += "Last Move: {0}\n".format(self.lastmove)
		rtn += "  01234567\n"
		for y in range(8):
			rtn += str(y) + " "
			for x in range(8):
				if not self.haspiece((x, y)):
					rtn += "+"
				else:
					if self.color((x, y)) == Board.BLACK:
						rtn += "X"
					else:
						rtn += "O"
			rtn += "\n"
		rtn += "To Play: {0}\n".format("Black" if self.toplay == Board.BLACK else "White")
		rtn += "---------------"
		return rtn

	def haspiece(self, p):
		return self.list0[p[1]][p[0]]

	def color(self, p):
		return self.list1[p[1]][p[0]]

	def place(self, p):
		if not not p:
			self.list0[p[1]][p[0]] = True
			self.list1[p[1]][p[0]] = self.toplay

	def flip(self, p):
		self.list1[p[1]][p[0]] = not self.list1[p[1]][p[0]]

	def endturn(self, p):
		self.lastmove = p
		self.toplay = not self.toplay

	def score(self):
		sc = 0
		for x in range(8):
			for y in range(8):
				if self.haspiece((x, y)):
					if self.color((x, y)) == Board.BLACK:
						sc += 1
					else:
						sc += -1
		return sc
