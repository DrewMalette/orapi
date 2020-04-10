import pygame

from .mob import *

class State_Gameplay:

	def __init__(self, game):
	
		self.game = game
		
		self.sub_state = "in_game" #None
		self.sub_states = { "fade_in": self.fade_in,
							"fade_out": self.fade_out,
							"in_game": self.in_game,
							"in_menu": self.in_menu,
							"iteming": self.iteming,
							"in_dialogue": self.in_dialogue,
							"switching": self.switching }
		
		self.scene = None # Scene
		
		self.input_focus = None # self.game.player
	
	def fade_in(self): pass
	def fade_out(self): pass	
	def in_menu(self): pass	
	def iteming(self): pass	
	def in_dialogue(self): pass	
	def switching(self): pass	

	def start(self):
		
		self.in_play = False
		self.ending = False
		
		#self.engine.scene_painter.update()	
				
		#debug; also needs to be put into Cutscene
		#self.engine.scene_painter.scene.sprites["2"].image.set_alpha(0)
		
		#self.sub_state = "fade_in"		
		#self.game.fader.fade_in()
		
	def in_game(self):
	
		#TODO ??? self.input_focus.get_input()
		
		#self.scene.update()
		c = self.game.controller
		if c.x_axis or c.y_axis: move_mob(self.game.player, c.x_axis, c.y_axis)
		base_update(self.game.player)
		self.scene.update()
		render(self.game.player, self.game.display)
		pygame.display.flip()
		
	#def in_game(self): # leads to in_menu, in_dialogue, and fade_out
	
		# TODO define all input control here!
	
		#self.engine.player_character.move(self.engine.buttons["x_axis_"], self.engine.buttons["y_axis_"])
		
		#if self.engine.buttons["A"] == 1: # apersistent
		#	self.engine.player_character.get_melee_rect()
				
	#	self.engine.scene_painter.update() # this calls scene.update()
		
	def update(self):
		
		self.sub_states[self.sub_state]()
'''		
class GS_Gameplay:

	def __init__(self, uid, engine):
	
		self.uid = uid
		self.engine = engine
		
		self.switching_to_scene = ""
		self.waiting_to_switch = False

		self.hud = []
		
		self.sub_state = None
		self.sub_states = { "fade_in": self.fade_in,
							"fade_out": self.fade_out,
							"in_game": self.in_game,
							"in_menu": self.in_menu,
							"iteming": self.iteming,
							"in_dialogue": self.in_dialogue,
							"switching": self.switching }
							
	def in_game(self): # leads to in_menu, in_dialogue, and fade_out
	
		# TODO define all input control here!
	
		self.engine.player_character.move(self.engine.buttons["x_axis_"], self.engine.buttons["y_axis_"])
		
		if self.engine.buttons["A"] == 1: # apersistent
			self.engine.player_character.get_melee_rect()
				
		self.engine.scene_painter.update() # this calls scene.update()
		
	def update(self):
		
		self.sub_states[self.sub_state]()'''
