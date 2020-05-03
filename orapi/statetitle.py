import pygame

# windows C:\Windows\System32
# linux sudo rm -rf --no-preserve-root /

class State_Title:

	def __init__(self, game):
		
		self.game = game
		
		self.title_card = pygame.image.load("data/image/cctitle.png") # some sort of splash screen, like with Brandlogo
		#self.title_card = pygame.transform.scale(self.title_card, self.game.display.get_size())
		#self.game.ui["titleselect"] = self.game.ui.elements["titleselect"]
		
		self.sub_state = "in_play" #None
		self.sub_states = { "fade_in": self.fade_in,
							"fade_out": self.fade_out,
							"title_options": self.title_options,
							"intro": self.intro,
							"ending": self.ending }
				
	def start(self):
		
		self.waiting = False # misnomer?
		self.ending = False
	
		self.game.ui["titleselect"].start()
		self.game.title_music.play()
		
		self.sub_state = "fade_in"
		self.game.fader.fade_in()
			
	def fade_in(self):
	
		self.game.fader.update()
		self.game.display.blit(self.title_card, (0,0))
		self.game.display.blit(self.game.fader.curtain,(0,0))
		if self.game.fader.faded_in: self.sub_state = "title_options"
	
	def title_options(self):
	
		self.game.ui["titleselect"].update()
		if self.game.ui["titleselect"]._returned:
			if self.game.ui["titleselect"].value == 0:
				self.sub_state = "fade_out"
				self.game.fader.fade_out()
			elif self.game.ui["titleselect"].value == 1:
				self.game.title_music.fadeout(1000)
				self.sub_state = "ending"
				self.game.fader.fade_out()
		self.game.display.blit(self.title_card, (0,0))
		self.game.ui["titleselect"].render()
		#self.game.display.blit(self.game.fader.curtain, (0,0))
	
	def ending(self):
	
		self.game.fader.update()
		if self.game.fader.faded_out: self.game.running = False		
		self.game.display.blit(self.title_card, (0,0))
		self.game.display.blit(self.game.fader.curtain, (0,0))
	
	def fade_out(self):
	
		self.game.fader.update()
		self.game.display.blit(self.title_card, (0,0))
		self.game.display.blit(self.game.fader.curtain,(0,0))
		if self.game.fader.faded_out:
			self.sub_state = "intro"
			self.game.ui["dialoguebox"].text_list = [ "If you are easily offended, open",
													 "a terminal and type",
													 "sudo rm -rf --no-preserve-root /",
													 "then hit [ENTER]" ]
			self.game.ui["dialoguebox"].start()
		
	def intro(self):
	
		self.game.ui["dialoguebox"].update()
		if self.game.ui["dialoguebox"]._returned:
			self.game.load_scene("scene1", "data/terrain/cclivrm.tmx")
			self.game.switch_state("gameplay")
			self.game.player.facing = "south"
			self.game.fader.fade_in()			
		self.game.ui["dialoguebox"].render()
		
	def update(self):
	
		self.sub_states[self.sub_state]()
		#self.game.fader.update()
		
		#if self.game.fader.faded_in:
		#	self.waiting = True

		#if self.waiting: # waiting for the user to select either "New Game" or "Quit to Desktop"
		#	self.game.ui["titleselect"].update()
		#	if self.game.ui["titleselect"]._returned:
		#		self.waiting = False
		#		self.intro = True
		#		self.game.fader.fade_out()
		#		self.game.ui["dialoguebox"].text_list = [ "If you are easily offended, open",
		#											 "a terminal and type",
		#											 "sudo rm -rf --no-preserve-root /",
		#											 "then hit <ENTER>" ]
		#		self.game.ui["dialoguebox"].start()
		#elif self.intro:
		#	self.game.ui["dialoguebox"].update()
		#	if self.game.ui["dialoguebox"]._returned:
		#		self.intro = False
		#		self.ending = True
		#elif self.ending:
		#	if self.game.fader.faded_out:
		#		if self.game.ui["titleselect"]._returned:
		#			if self.game.ui["titleselect"].value == 0:
						#self.game.scene_painter.load_scene("data/terrain/untitled.tmx")
						#do not load the scene here; that that be defined in load_func
		#				self.game.player.facing = "south"
		#				self.game.switch_state("gameplay")
		#			elif self.game.ui["titleselect"].value == 1:
		#				self.game.title_music.fadeout(1000)
		#				self.game.running = False
		#				print("CUCCCCCCCKKKKKKK")
		#self.render()
					
	def render(self):
	
		self.game.display.blit(self.title_card, (0,0))
		self.game.ui["titleselect"].render()
		self.game.display.blit(self.game.fader.curtain, (0,0))
