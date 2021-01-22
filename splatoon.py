import pyxel

WINDOW_BASE = 16
WINDOW_H = 9 * WINDOW_BASE
WINDOW_W = 16* WINDOW_BASE
CAT_H = 16
CAT_W = 16

class app:
	def __init__(self):
		self.IMG_ID0 = 0
		self.IMG_ID1 = 1
		self.IMG_ID2 = 2

		self.IMG_ID0_X = WINDOW_BASE * 4
		self.IMG_ID0_Y = WINDOW_BASE * 8

		pyxel.init(WINDOW_W, WINDOW_H, caption="Splatoon3")

		pyxel.image(self.IMG_ID1).load(0, 0, "assets/cat_16x16.png")


		pyxel.run(self.update, self.draw)

	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

	def draw(self):
		pyxel.cls(0)

		pyxel.text(WINDOW_W/2, WINDOW_H/2, "Splatoon3", pyxel.frame_count % 16)

		pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, self.IMG_ID1, 0, 0, CAT_W, CAT_H, 13 )


app()