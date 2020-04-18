import pygame

from .mob import move_mob, render
from .scene import Scene
from .terrain import Terrain
from .dialogue import UI_Dialogue
from . import utilities
from .utilities import get_centre

class Game:

	fps = 60
	display_size = (640,480)

	def __init__(self, version, load_func):
	
		self.version = version
	
		self.display = pygame.display.set_mode(self.display_size)
		self.terrain_renderer = Terrain_Renderer("terrend", self)
		self.dialogue_box = UI_Dialogue("dialoguebox", self, (170,360), (300,100))
	
		self.controller = Keyboard(self)
		self.state = None
		self.states = {}
		
		#self.ui = None
		
		self.clock = pygame.time.Clock()
		self.tick = 0
		
		self.player = None
		self.scene = None
		
		self.ui_font = pygame.font.Font(None, 24)
				
		# do some loading shit here
		load_func(self)

	def switch_state(self, state_uid): # load and start
	
		self.state = self.states[state_uid]
		self.state.start()

	def load_scene(self, uid, filename): # scene?
	
		#if self.scene != None:
		#	del self.scene
		self.scene = Scene("scene1", self)
		terrain = Terrain(filename, self)
		self.terrain_renderer.scene = self.scene
		self.terrain_renderer.following = self.player

		# assumes the tile is square
		self.terrain_renderer.tilesize = self.scene.terrain.tilewidth
		self.terrain_renderer.cols = int(self.terrain_renderer.w / self.scene.terrain.tilesize + 2)
		self.terrain_renderer.rows = int(self.terrain_renderer.h / self.scene.terrain.tilesize + 2)
		self.terrain_renderer.blank = pygame.Surface((self.scene.terrain.tilesize,self.scene.terrain.tilesize)).convert()
		self.terrain_renderer.blank.fill((0,0,0))
		
		#self.engine.controller.flush()
		self.player.moving = False
		#self.sprites["player"].facing = "south" TODO put this somewhere else (like in a gamestate)
		self.terrain_renderer.update()		
	
	def main(self):
	
		self.running = True
		
		while self.running:
		
			self.update()
			#self.render() is this needed? Handling is done in state, methinks
			
		pygame.quit()
		exit()

	def update(self):
	
		self.clock.tick(self.fps)
		self.tick = (self.tick + 1) % 1024
		pygame.event.pump()
		self.controller.update(pygame.key.get_pressed())
		self.state.update()
		#self.camera.update()
		
	def render(self):
	
		#self.display.blit(self.camera.canvas,(0,0))
		#self.ui.blit(self.display)
		pass
			
class Controller:

	def __init__(self, game):
	
		self.game = game
		
		self.x_axis = self.y_axis = 0
		self.x_repeat = self.y_repeat = False
		self.x_pressed = self.y_pressed = False
		self.x_tick = self.y_tick = 0
		
		self.as_pressed = False
		self.as_button = 0 # 'A' button single pulse
		self.ar_button = 0 # 'A' button repeating pulse
		
		self.exit = 0
		
	def flush(self):
	
		self.as_button = 0

class Keyboard(Controller):

	def __init__(self, game):
	
		Controller.__init__(self, game)
			
	def update(self, keys):
		
		self.x_axis = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] 
		self.y_axis = keys[pygame.K_DOWN] - keys[pygame.K_UP]
		
		self.as_button = 0
		self.ar_button = keys[pygame.K_RCTRL]
		
		if self.x_axis != 0 and not self.x_pressed:
			self.x_tick = pygame.time.get_ticks()
			self.x_pressed = True
		elif self.x_axis == 0 and self.x_pressed:
			self.x_pressed = False
		self.x_repeat = self.x_pressed and (pygame.time.get_ticks() - self.x_tick >= 800)

		if self.y_axis != 0 and not self.y_pressed:
			self.y_tick = pygame.time.get_ticks()
			self.y_pressed = True
		elif self.y_axis == 0 and self.y_pressed:
			self.y_pressed = False
		self.y_repeat = self.y_pressed and (pygame.time.get_ticks() - self.y_tick >= 800)

		if keys[pygame.K_RCTRL] == 1 and not self.as_pressed:
			self.as_pressed = True
			self.as_button = 1
		elif keys[pygame.K_RCTRL] == 0 and self.as_pressed:
			self.as_pressed = False

		#print(self.x_repeat, self.y_repeat)

		self.game.running = (not keys[pygame.K_ESCAPE])
		
class Terrain_Renderer(pygame.Rect):

	def __init__(self, uid, engine, x=0, y=0):
	
		self.uid = uid
		self.engine = engine
		w,h = self.engine.display.get_size()
		pygame.Rect.__init__(self, (x,y,w,h))
		
		self.tilesize = 0 # TODO where does this get set?
		self.cols = 0
		self.rows = 0
		self.blank = None
		self.following = None
		self.scene = None
		
	def tile_prep(self, layer, col, row):

		x_offset = self.x % self.tilesize
		y_offset = self.y % self.tilesize

		c_index = int(self.x / self.tilesize + col)
		r_index = int(self.y / self.tilesize + row)
	
		index = self.scene.terrain.get_tile(layer, c_index, r_index)

		x = col * self.tilesize - x_offset
		y = row * self.tilesize - y_offset
		
		if index != "0":
			tile = self.scene.tileset[index]
			return (tile, x, y)
		else:			
			return ("0", x, y)
			
	def update(self):
	
		#self.scene.update()
	
		x,y = get_centre(self.following)
		
		if x > self.w / 2:
			self.x = x - self.w / 2
		elif x <= self.w / 2:
			self.x = 0
		
		if y > self.h / 2:
			self.y = y - self.h / 2
		elif y <= self.h / 2:
			self.y = 0
	
		if self.x + self.w > self.scene.terrain.cols * self.tilesize:
			self.x = self.scene.terrain.cols * self.tilesize - self.w
		elif self.x < 0:
			self.x = 0
			
		if self.y + self.h > self.scene.terrain.rows * self.tilesize:
			self.y = self.scene.terrain.rows * self.tilesize - self.h
		elif self.y < 0:
			self.y = 0
				
	def render(self):
	
		for row in range(self.rows): # draw the bottom and middle tile layers
			for col in range(self.cols):
				x_offset = self.x % self.tilesize
				y_offset = self.y % self.tilesize

				c_index = int(self.x / self.tilesize + col)
				r_index = int(self.y / self.tilesize + row)
		
				bottom_i = self.scene.terrain.get_tile("bottom", c_index, r_index)
				middle_i = self.scene.terrain.get_tile("middle", c_index, r_index)

				c = col * self.tilesize - x_offset
				r = row * self.tilesize - y_offset
				
				if bottom_i != "0":
					bottom_t = self.scene.terrain.tileset[bottom_i]
					self.engine.display.blit(bottom_t, (c,r))
				elif bottom_i == "0":
					self.engine.display.blit(self.blank, (c,r))

				if middle_i != "0":
					middle_t = self.scene.terrain.tileset[middle_i]
					self.engine.display.blit(middle_t, (c,r))

		#if self.scene.loot: # TODO merge this with sprites for the y_sort
		#	for loot in self.scene.loot.values():
		#		loot.render(self.engine.display, x_offset = -self.x, y_offset = -self.y)

		if self.scene.live_mobs: # draw the sprites
			#for sprite in self.scene.sprites.values():
			for sprite in utilities.y_sort(self.scene.live_mobs.values()):
				render(sprite, self.engine.display, x_offset = -self.x, y_offset = -self.y)
		
		for row in range(self.rows): # draw the top layer
			for col in range(self.cols):
				tile, x, y = self.tile_prep("top", col, row)
				if tile != "0": self.engine.display.blit(tile, (x, y))
