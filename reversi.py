# 参考URL
# https://katoh4u.hatenablog.com/entry/2018/03/22/130105

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

	def put_disk(self, x, y, player):
		# すでに他の石があれば置くことができない
		if self.cells[y][x] is not None:
			return False

		# 獲得できる石がない場合も置くことができない
		flippable = self.list_flippable_disks(x, y, player)
		if flippable == []:
			return False

		# 実際に石を置く処理
		self.cells[y][x] = player
		for x,y in flippable:
			self.cells[y][x] = player

		return True

	def list_flippable_disks(self, x, y, player):
		PREV = -1
		NEXT = 1
		DIRECTION = [PREV, 0, NEXT]
		flippable = []

		for dx in DIRECTION:
			for dy in DIRECTION:
				if dx == 0 and dy == 0:
					continue

				tmp = []
				depth = 0
				while(True):
					depth += 1

					# 方向 x 深さ（距離）を要求座標に加算し直線的な探査をする
					rx = x + (dx * depth)
					ry = y + (dy * depth)

					# 調べる座標(rx, ry)がボードの範囲内ならば
					if 0 <= rx < BOARD_SIZE and 0 <= ry < BOARD_SIZE:
						request = self.cells[ry][rx]

						# Noneを獲得することはできない
						if request is None:
							break

						if request == player:	# 自分の石が見つかったとき
							if tmp != []:		# 探査した範囲内に獲得可能な石があれば
								flippable.extend(tmp)	# flippableに追加

						# 相手の石が見つかったとき
						else:
							# 獲得可能な石として一時保存
							tmp.append((rx, ry))
					else:
						break		
		return flippable
