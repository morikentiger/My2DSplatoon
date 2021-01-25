WHITE = 0
BLACK = 1
BOARD_SIZE = 8

class ReversiBoard(object):
	def __init__(self):
		# 2次元リストを生成する
		# 各要素の初期値はNone
		self.cells = []
		for i in range(BOARD_SIZE):
			self.cells.append([None for i in range(BOARD_SIZE)])

		# ４つの石を初期配置する
		self.cells[3][3] = WHITE
		self.cells[3][4] = BLACK
		self.cells[4][3] = BLACK
		self.cells[4][4] = WHITE


board = ReversiBoard()
print(*board.cells, sep='\n')