import pygame

from .mob import move_mob

class Game:

	fps = 60
	display_size = (640,480)

	def __init__(self, version, load_func):
	
		self.version = version
	
		self.display = pygame.display.set_mode(self.display_size)
	
		self.controller = Keyboard(self)
		self.state = None
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
		
		self.x_axis = self.y_axis = 0
		self.x_repeat = self.y_repeat = False
		self.x_pressed = self.y_pressed = False
		self.x_tick = self.y_tick = 0
		
		self.exit = 0

class Keyboard(Controller):

	def __init__(self, game):
	
		Controller.__init__(self, game)
			
	def update(self, keys):
		
		self.x_axis = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] 
		self.y_axis = keys[pygame.K_DOWN] - keys[pygame.K_UP]
		
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

		print(self.x_repeat, self.y_repeat)

		self.game.running = (not keys[pygame.K_ESCAPE])
