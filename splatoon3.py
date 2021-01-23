import pyxel
import itertools
import numpy as np

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
		# self.tempos = Vec2(0, 0)
		self.vec = 0
		self.dx = 0
		self.dy = 0
		self.speed = 2
		self.img_ika = img_id

	def update(self, x, y, dx):
		self.pos.x = x
		self.pos.y = y
		self.vec = dx

class Ink:
	def __init__(self):
		self.pos = Vec2(0, 0)
		self.vec = 0
		self.size = 2
		self.speed = 4
		self.range = 32
		self.color = 8 # 212,24,108

	def update(self, x, y, dx, size, speed, range, color):
		self.pos.x = x
		self.pos.y = y
		self.vec = dx
		self.size = size
		self.speed = speed
		self.range = range
		self.color = color

class Stage:
	def __init__(self):
		self.size = Vec2(WINDOW_W, WINDOW_H)
		self.color = 2
		self.isInk = np.zeros((WINDOW_H, WINDOW_W))
		# self.isInk = [[self.color] * self.size.x for i in range(self.size.y)]
		# print(self.isInk)
		# ======== draw stage ======
		# for j in range(WINDOW_H):
		# 	for i in range(WINDOW_W):
		# 		pyxel.rect(i, j, 1, 1, self.color)
		
	def update(self, isInk, x, y, size, color):
		# for y in range(WINDOW_H):
		# 	for x in range(WINDOW_W):
		self.isInk = isInk
		self.x = x
		self.y = y
		self.size = size
		self.color = color

class App:
	def __init__(self):
		self.IMG_ID0 = 0
		self.IMG_ID1 = 1
		self.IMG_ID2 = 2

		self.IMG_ID0_X = WINDOW_BASE * 4
		self.IMG_ID0_Y = WINDOW_BASE * 8

		pyxel.init(WINDOW_W, WINDOW_H, caption="Splatoon3")

		pyxel.image(self.IMG_ID1).load(0, 0, "assets/ika_22x22.png")

		# make instance
		self.ika = Ika(self.IMG_ID1)
		self.inks = []
		self.temp_ink = Ink()
		self.inks.append(self.temp_ink)

		self.stage = Stage()

		pyxel.run(self.update, self.draw)

	def update(self):
		if pyxel.btnp(pyxel.KEY_ESCAPE):
			pyxel.quit()
		
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

		# ======= ctrl Ink ========
		if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON, True, self.temp_ink.speed):
			new_ink = Ink()
			if self.ika.vec > 0:
				new_ink.update(self.ika.pos.x + IKA_W/2 + 5,
								self.ika.pos.y + IKA_H/2, self.ika.vec,
								new_ink.size, new_ink.speed, new_ink.range, new_ink.color)
				self.stage.update(self.stage.isInk,self.ika.pos.x + IKA_W/2 + 5, self.ika.pos.y + IKA_H/2, new_ink.size, new_ink.color)
			else:
				new_ink.update(self.ika.pos.x + IKA_W/2 - 5,
								self.ika.pos.y + IKA_H/2, self.ika.vec,
								new_ink.size, new_ink.speed, new_ink.range, new_ink.color)
				self.stage.update(self.stage.isInk, self.ika.pos.x + IKA_W/2 - 5, self.ika.pos.y + IKA_H/2, new_ink.size, new_ink.color)
			self.inks.append(new_ink)

		ink_count = len(self.inks)
		for i in range(ink_count):
			if self.ika.pos.x + IKA_W/2 - self.inks[i].range < self.inks[i].pos.x and self.inks[i].pos.x < self.ika.pos.x + IKA_W/2 + self.inks[i].range:
				# ink update
				if self.inks[i].vec > 0:
					self.inks[i].update(self.inks[i].pos.x + self.inks[i].speed,
										self.inks[i].pos.y,
										self.inks[i].vec, self.inks[i].size,
										self.inks[i].speed, 
										self.inks[i].range, 
										self.inks[i].color)
				else:
					self.inks[i].update(self.inks[i].pos.x - self.inks[i].speed,
										self.inks[i].pos.y,
										self.inks[i].vec, self.inks[i].size,
										self.inks[i].speed, 
										self.inks[i].range, 
										self.inks[i].color)
			else:
				self.stage.update(self.stage.isInk, self.inks[i].pos.x, self.inks[i].pos.y,self.inks[i].size, self.inks[i].color)
				del self.inks[i]
				break

	def draw(self):
		pyxel.cls(0)

		pyxel.text(WINDOW_W/2, WINDOW_H/2, "Splatoon3", pyxel.frame_count % 16)
		pyxel.text(0,0, str(self.ika.vec),13)
		
		# ======== draw stage ======
		i_list = list(range(WINDOW_W))
		j_list = list(range(WINDOW_H))

		for j in j_list:
			for i in i_list:
				pyxel.rect(i, j, 1, 1, self.stage.color)
		
		# ======== draw ika ========
		if self.ika.vec > 0:
			pyxel.blt(self.ika.pos.x, self.ika.pos.y, self.IMG_ID1, 0, 0, -IKA_W, IKA_H, 13 )
		else:
			pyxel.blt(self.ika.pos.x, self.ika.pos.y, self.IMG_ID1, 0, 0, IKA_W, IKA_H, 13 )

		# ======== draw inks =========
		for ink in self.inks:
			pyxel.circ(ink.pos.x, ink.pos.y, ink.size, ink.color)
			# pyxel.circb(ink.pos.x, ink.pos.y, ink.size, ink.color)
		pyxel.circ(33, 33, 8, 9)
		pyxel.circ(33, 33, 7, 8)
		pyxel.circ(33, 33, 6, 7)
		pyxel.circ(33, 33, 5, 6)
		pyxel.circ(33, 33, 4, 5)
		pyxel.circ(33, 33, 3, 4)
		pyxel.circ(33, 33, 2, 3)
		pyxel.circ(33, 33, 1, 2)

App()