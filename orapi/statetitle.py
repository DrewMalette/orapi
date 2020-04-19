import pygame

class State_Title:

	def __init__(self, game):
		
		self.game = game
		
		self.waiting = False
		self.ending = False
		
		self.image = pygame.image.load("data/image/ccgift.png") # some sort of splash screen, like with Brandlogo
		#self.image = pygame.transform.scale(self.image, self.game.display.get_size())
		#self.selector_box = self.game.ui.elements["titleselect"]
		#self.music = pygame.mixer.Sound("content/sound/title_music.ogg")
		
	def start(self):
		
		self.waiting = False # misnomer?
		self.ending = False
	
		#self.selector_box.start()
		self.game.fader.fade_in()
		#self.music.play()
		
	def update(self):
	
		self.game.fader.update()
		
		if self.game.fader.faded_in:
			self.waiting = True

		elif self.waiting: # waiting for the user to select either "New Game" or "Quit to Desktop"
			self.selector_box.update()
			if self.selector_box._returned:
				self.waiting = False
				self.ending = True
				self.game.fader.fade_out()
				#self.music.fadeout(800)

		elif self.ending:
			if self.game.fader.faded_out:
				if self.selector_box._returned:
					if self.selector_box.value == 0:
						self.game.scene_painter.load_scene("data/terrain/untitled.tmx")
						self.game.player_character.facing = "south"
						self.game.switch_state("gameplay")
					elif self.selector_box.value == 1:
						self.game.running = False
					
	def render(self):
	
		self.game.display.blit(self.image, (0,0))
		self.selector_box.render(self.game.display)
		self.game.display.blit(self.game.fader.curtain, (0,0))
