# from splatoon3 import Vec2
import pyxel
import numpy as np


WINDOW_BASE = 8
WINDOW_RATIO_H = 24
WINDOW_RATIO_W = 32
WINDOW_H = WINDOW_RATIO_H * WINDOW_BASE
WINDOW_W = WINDOW_RATIO_W * WINDOW_BASE
# WINDOW_H_B = int(WINDOW_H/8)
# WINDOW_W_B = int(WINDOW_W/8)
IKA_H = 22
IKA_W = 22
INK_H = WINDOW_BASE
INK_W = WINDOW_BASE

class Vec2:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
class Ika:
	def __init__(self, img_id):
		self.pos = Vec2(0, int(WINDOW_H/2 - IKA_H/2))
		self.vec = 0
		self.dx = 0
		self.dy = 0
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

		pyxel.init(WINDOW_W,WINDOW_H,caption="Splatoon3",fps=600, quit_key=pyxel.KEY_ESCAPE,fullscreen=True)

		pyxel.image(self.IMG_ID1).load(0, 0, "assets/ika_22x22.png")

		pyxel.mouse(True)

		# make instance
		self.ika = Ika(self.IMG_ID1)
		self.inks = []

		pyxel.run(self.update, self.draw)

	def update(self):

		# ======= ctrl ika ========
		if pyxel.btnp(pyxel.KEY_W, True, 1):
			self.ika.pos.y -= self.ika.speed
			self.ika.dy = 1
		if pyxel.btnp(pyxel.KEY_A, True, 1):
			self.ika.pos.x -= self.ika.speed
			self.ika.dx = -1
		if pyxel.btnp(pyxel.KEY_S, True, 1):
			self.ika.pos.y += self.ika.speed
			self.ika.dy = -1
		if pyxel.btnp(pyxel.KEY_D, True, 1):
			self.ika.pos.x += self.ika.speed
			self.ika.dx = 1

		if self.ika.dx != 0:
			self.ika.update(self.ika.pos.x, self.ika.pos.y, self.ika.dx)
		elif self.ika.dy != 0:
			self.ika.update(self.ika.pos.x, self.ika.pos.y, self.ika.vec)

	def draw(self):
		pyxel.cls(10)

		# ======== draw ika ========
		if self.ika.vec > 0:
			pyxel.blt(self.ika.pos.x, self.ika.pos.y, self.IMG_ID1, 0, 0, -IKA_W, IKA_H, 13 )
		else:
			pyxel.blt(self.ika.pos.x, self.ika.pos.y, self.IMG_ID1, 0, 0, IKA_W, IKA_H, 13 )


App()