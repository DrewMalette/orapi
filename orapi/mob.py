
import pygame
from .mechanics import StatBlock

heading = { (0,-1): "north", (0,1): "south", (-1,0): "west", (1,0): "east",
			(-1,-1): "north", (1,1): "south", (-1,1): "west", (1,-1): "east" }

north_rect = lambda mob: (mob.x, mob.y - mob.h)
south_rect = lambda mob: (mob.x, mob.y + mob.h)
west_rect = lambda mob: (mob.x - mob.w, mob.y)
east_rect = lambda mob: (mob.x + mob.w, mob.y)

talk_rect = { "north": north_rect, "south": south_rect, "west": west_rect, "east": east_rect }
# mob.talk_rect.x, mob.talk_rect.y = talk_rect[mob.facing](mob)

get_centre = lambda mob: ((mob.x + (mob.w / 2)), (mob.y + (mob.h / 2)))

class Mob(pygame.Rect): # incarnation of the 'Sprite' concept

	pattern = [0,1,0,2]
	facings = { "south": 0, "north": 1, "east": 2, "west": 3 }

	def __init__(self, game, filename, name):
	
		self.game = game
	
		#self.data = utilities.load_sprite(filename)
		#self.name = name # within Scene.mobs, the uid is a number
		#pygame.Rect.__init__(self, (0,0, self.data["width"], self.data["height"]))
		#self.cells = self.data["cells"]
		#self.animations = self.data["animations"]
		#self.off_x = self.data["off_x"]
		#self.off_y = self.data["off_y"]
		data = load_sprite(filename)
		pygame.Rect.__init__(self, data["rect"])
		self.cols = data["cols"]
		self.rows = data["rows"]
		self.cells = data["cells"]
		self.x_offset, self.y_offset = data["offsets"]
		#	return { "cols": cols, "rows": rows, "cells": cells, "rect": rect, "offsets": offsets }
				
		self.moving = False
		self.facing = "south"
		self.frame = 0
		self.scene = None
		self.speed = 2

		self.alive = True # going to StatBlock?
		self.dying = False
		self.opacity = 255
		
		self.talk_rect = pygame.Rect(0,0,12,12)
		
		self.statblock = StatBlock(4,3,2)
		
		#
		#self.targeting = False # aiming?
		#self.attacking = False
		#self.atkstart = 0
		
	def spawn(self):
	
		self.scene.live_mobs[self.name] = self
	
	def kill(self):
	
		del self.scene.live_mobs[self.name]
		
def place(mob, col, row):
	
	mob.x = col * mob.scene.tilesize + (mob.scene.tilesize - mob.w) / 2
	mob.y = row * mob.scene.tilesize + (mob.scene.tilesize - mob.h) - 4

def collision(mob, x_axis, y_axis):

	'''for c in range(4):
		xm = ((mob.x + x_axis * mob.speed) + (c % 2) * mob.w)
		ym = ((mob.y + y_axis * mob.speed) + int(c / 2) * mob.h)

		col = int(xm / mob.scene.tilesize) # is this slow?
		row = int(ym / mob.scene.tilesize)

		if mob.scene.get_tile("collide", col, row) != "0":
			return True

	for sprite in mob.scene.sprites.values():
		if sprite is not mob:
			xm = mob.speed * x_axis + mob.x
			ym = mob.speed * y_axis + mob.y
			if sprite.colliderect((xm, ym, mob.w, mob.h)):
				return True'''
	return False
	
def move_mob(mob, x_axis, y_axis):

	x = (not collision(mob, x_axis * mob.speed, 0)) * (x_axis * mob.speed)
	y = (not collision(mob, 0, y_axis * mob.speed)) * (y_axis * mob.speed)
	mob.move_ip(x*mob.moving, y*mob.moving)
	if x_axis != 0 or y_axis != 0: mob.facing = heading[(x_axis,y_axis)]
		
def base_update(mob):

	# mob.statblock.upkeep()
	mob.moving = bool(mob.game.controller.x_axis or mob.game.controller.y_axis)	
	mob.frame += mob.moving & (mob.game.tick % 12 == 0) * 1
	mob.frame = mob.frame % len(mob.pattern) * mob.moving
	
def update(mob): # overridden by classes derived

	mob.base_update()
	
def render(mob, surface, x_offset=0, y_offset=0):

	x = (mob.x - mob.x_offset) + x_offset
	y = (mob.y - mob.y_offset) + y_offset
	frame = mob.pattern[mob.frame]
	facing = mob.facings[mob.facing]
	surface.blit(get_cell(mob, frame, facing), (x,y))

def get_cell(mob, col, row):

	if (col >= 0 and col < mob.cols) and (row >= 0 and row < mob.rows):
		return mob.cells[mob.cols*row+col]
	else:
		print("requested column or row does not match the mob's sprite dimensions")
		pygame.quit()
		exit()
	
def load_sprite(filename):

	image = pygame.image.load(filename)
	image.convert()
	image.set_colorkey((0xff,0x00,0xff), pygame.RLEACCEL)
	cell_w, cell_h = image.get_at((0, image.get_height()-1))[:2]
	rect = pygame.Rect((0,0)+image.get_at((1, image.get_height()-1))[:2])
	offsets = image.get_at((2, image.get_height()-1))[:2]
	cols = int(image.get_width() / cell_w)
	rows = int(image.get_height() / cell_h)

	cells = {}
	for row in range(rows):
		for col in range(cols):
			cells[row*cols+col] = image.subsurface((col*cell_w, row*cell_h, cell_w, cell_h))

	return { "cols": cols, "rows": rows, "cells": cells, "rect": rect, "offsets": offsets }
