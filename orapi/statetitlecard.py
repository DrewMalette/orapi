import pygame

class State_Titlecard:
	
	def __init__(self, game):
	
		self.game = game
		
		self.waiting = False
		self.ending = False
		self.tick = 0
		
		self.image = pygame.image.load("data/image/cctitle.png")
		
	def start(self):
		
		self.waiting = False
		self.ending = False
		self.tick = 0
	
		self.game.fader.fade_in()
		
	def update(self):
	
		self.game.fader.update()
		
		if self.game.fader.faded_in:
			self.waiting = True
			self.tick = pygame.time.get_ticks()
		if self.waiting:
			s = int((pygame.time.get_ticks() - self.tick) / 1000)
			if not self.ending and (s == 3) or self.game.controller.as_button == 1:
				self.waiting = False
				self.ending = True
				self.game.fader.fade_out()
		if self.ending:
			if self.game.fader.faded_out:
				self.game.switch_state("gameplay")
				
		self.game.display.blit(self.image, (0,0))
		self.game.display.blit(self.game.fader.curtain, (0,0))
