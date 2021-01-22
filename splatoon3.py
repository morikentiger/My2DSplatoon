import pyxel

WINDOW_BASE = 16
WINDOW_H = 9 * WINDOW_BASE
WINDOW_W = 16* WINDOW_BASE
IKA_H = 22
IKA_W = 22


class Vec2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Ika:
	def __init__(self, img_id):
		self.pos = Vec2(0, WINDOW_H/2 - IKA_H/2)
		self.vec = 0
		self.speed = 2
		self.img_ika = img_id

	def update(self, x, y, dx):
		self.pos.x = x
		self.pos.y = y
		self.vec = dx

class App:
	def __init__(self):
		self.IMG_ID0 = 0
		self.IMG_ID1 = 1
		self.IMG_ID2 = 2

		self.IMG_ID0_X = WINDOW_BASE * 4
		self.IMG_ID0_Y = WINDOW_BASE * 8

		pyxel.init(WINDOW_W, WINDOW_H, caption="Splatoon3")

		pyxel.image(self.IMG_ID1).load(0, 0, "assets/ika_22x22.png")

		self.ika = Ika(self.IMG_ID1)


		pyxel.run(self.update, self.draw)

	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()
		
		# ======= ctrl ika ========
		if pyxel.btnp(pyxel.KEY_W):
			self.ika.pos.y -= self.ika.speed
		if pyxel.btnp(pyxel.KEY_A):
			self.ika.pos.x -= self.ika.speed
		if pyxel.btnp(pyxel.KEY_S):
			self.ika.pos.y += self.ika.speed
		if pyxel.btnp(pyxel.KEY_D):
			self.ika.pos.x += self.ika.speed
		

	def draw(self):
		pyxel.cls(0)

		pyxel.text(WINDOW_W/2, WINDOW_H/2, "Splatoon3", pyxel.frame_count % 16)

		pyxel.blt(self.ika.pos.x, self.ika.pos.y, self.IMG_ID1, 0, 0, -IKA_W, IKA_H, 13 )

	

App()