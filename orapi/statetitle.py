import pygame

class State_Title:

	def __init__(self, game):
		
		self.game = game
		
		self.waiting = False
		self.ending = False
		
		self.image = pygame.image.load("data/image/cctitle.png") # some sort of splash screen, like with Brandlogo
		#self.image = pygame.transform.scale(self.image, self.game.display.get_size())
		#self.game.title_select = self.game.ui.elements["titleselect"]
		#self.music = pygame.mixer.Sound("content/sound/title_music.ogg")
		
	def start(self):
		
		self.waiting = False # misnomer?
		self.ending = False
	
		self.game.title_select.start()
		self.game.fader.fade_in()
		#self.music.play()
		
	def update(self):
	
		self.game.fader.update()
		
		if self.game.fader.faded_in:
			self.waiting = True

		elif self.waiting: # waiting for the user to select either "New Game" or "Quit to Desktop"
			self.game.title_select.update()
			if self.game.title_select._returned:
				self.waiting = False
				self.ending = True
				self.game.fader.fade_out()
				#self.music.fadeout(800)

		elif self.ending:
			if self.game.fader.faded_out:
				if self.game.title_select._returned:
					if self.game.title_select.value == 0:
						#self.game.scene_painter.load_scene("data/terrain/untitled.tmx")
						#do not load the scene here; that that be defined in load_func
						self.game.player.facing = "south"
						self.game.switch_state("gameplay")
					elif self.game.title_select.value == 1:
						self.game.running = False
						
		self.render()
					
	def render(self):
	
		self.game.display.blit(self.image, (0,0))
		self.game.title_select.render()
		self.game.display.blit(self.game.fader.curtain, (0,0))
