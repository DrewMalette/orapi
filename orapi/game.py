import pygame

from .stategameplay import *

class Game:

	fps = 60
	display_size = (640,480)

	def __init__(self, version, load_func):
	
		self.version = version
	
		self.display = pygame.display.set_mode(self.display_size)
	
		self.controller = Keyboard(self)
		self.state = State_Gameplay(self)
		self.states = {}
		
		self.ui = None
		
		self.clock = pygame.time.Clock()
		self.tick = 0
		
		# do some loading shit here
		load_func(self)

	def switch_state(self, state_uid): # load and start
	
		self.state = self.states[state_uid]
		self.state.start()

	def main(self):
	
		self.running = True
		
		while self.running:
		
			self.update()
			self.render()
			
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
		
		self.up = 0
		self.down = 0
		self.left = 0
		self.right = 0
		
		self.exit = 0

class Keyboard(Controller):

	def __init__(self, game):
	
		Controller.__init__(self, game)
	
	def update(self, keys):
		
		self.up = keys[pygame.K_UP]
		self.down = keys[pygame.K_DOWN]
		self.left = keys[pygame.K_LEFT]
		self.right = keys[pygame.K_RIGHT]
		
		self.exit = keys[pygame.K_ESCAPE]
		
		if self.exit == 1:
			self.game.running = False
