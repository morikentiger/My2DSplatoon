# 参考URL
# https://katoh4u.hatenablog.com/entry/2018/03/22/130105

import pyxel

WHITE = 0
BLACK = 1
BOARD_SIZE = 8

WINDOW_SIZE = 256
WINDOW_BASE = int(WINDOW_SIZE/BOARD_SIZE)#32
WINDOW_W = WINDOW_SIZE
WINDOW_H = WINDOW_SIZE


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


		# board = ReversiBoard()
		# print(*board.cells, sep='\n')

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
	
	def show_board(self):
		print("--" * 20)
		x = 0
		y = 0
		for i in self.cells:
			y += 1
			for cell in i:
				x += 1
				if cell == WHITE:
					pyxel.circ(x*WINDOW_BASE, y*WINDOW_BASE, 16, 7)
					print("W", end=" ")
				elif cell == BLACK:
					pyxel.circ(x*WINDOW_BASE, y*WINDOW_BASE, 16, 8)
					print("B", end=" ")
				else:
					pyxel.rect(x*WINDOW_BASE, y*WINDOW_BASE, 16, 16, 1)
					print("*", end=" ")
			print("\n", end="")
	def list_possible_cells(self, player):
		possible = []
		for x in range(BOARD_SIZE):
			for y in range(BOARD_SIZE):
				if self.cells[y][x] is not None:
					continue
				if self.list_flippable_disks(x, y, player) == []:
					continue
				else:
					possible.append((x, y))
		return possible

class Game(ReversiBoard):
	DRAW = -1

	def __init__(self, turn=0, start_player=BLACK):
		super().__init__()
		self.player = start_player
		self.turn = turn
		self.winner = None
		self.was_passed = False

	def is_finished(self):
		return self.winner is not None

	def list_possible_cells(self):
		return super().list_possible_cells(self.player)

	def get_color(self, player):
		if player == WHITE:
			return "WHITE"
		if player == BLACK:
			return "BLACK"
		else:
			return "DRAW"

	def get_current_player(self):
		return self.player

	def get_next_player(self):
		return WHITE if self.player == BLACK else BLACK

	def shift_player(self):
		self.player = self.get_next_player()

	def put_disk(self, x, y):
		if super().put_disk(x, y, self.player):
			self.was_passed = False
			self.player = self.get_next_player()
			self.turn += 1
		else:
			return False

	def pass_moving(self):
		if self.was_passed:
			return self.finish_game()

		self.was_passed = True
		self.shift_player()
	
	def show_score(self):
		# それぞれのプレイヤーの石の数を表示する
		print("{}: {}".format("BLACK", self.disks[BLACK]))
		print("{}: {}".format("WHITE", self.disks[WHITE]))

	def finish_game(self):
		self.disks = self.get_disk_map()
		white = self.disks[WHITE]
		black = self.disks[BLACK]

		if white < black:
			self.winner = BLACK
		elif black < white:
			self.winner = WHITE
		else:
			self.winner = self.on_draw()

		return self.winner

	def get_disk_map(self):
		disks = {}
		disks[WHITE] = 0
		disks[BLACK] = 0
		for i in self.cells:
			for cell in i:
				if cell == WHITE:
					disks[WHITE] += 1
				elif cell == BLACK:
					disks[BLACK] += 1
		return disks

	def on_draw(self):
		return self.DRAW
		

if __name__ == "__main__":
	game = Game()

	pyxel.init(WINDOW_W, WINDOW_H, caption="リバーシ", fps=300, quit_key=pyxel.KEY_ESCAPE)

	pyxel.mouse(True)

	pyxel.run(update, draw)

	def update(self):

		return 0

	def draw(self):

		return 0

	while(True):
		possible = game.list_possible_cells()
		player_name = game.get_color(game.get_current_player())

		if game.is_finished():
			game.show_board()
			game.show_score()
			print("Winner: {}".format(game.get_color(game.winner)))
			break

		if possible == []:
			print("player {} can not puts.".format(player_name))
			game.pass_moving()
			continue

		game.show_board()
		print("player: " + player_name)
		print("put to: " + str(possible))
		index = int(input("choose: "))

		game.put_disk(*possible[index])
	# board = ReversiBoard()
	# board.show_board()
	# board.put_disk(3, 2, BLACK)
	# board.show_board()
