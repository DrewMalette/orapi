import pygame

from .mob import *

class State_Create_Character:

	def __init__(self, game):
	
		self.game = game

class State_Gameplay:

	def __init__(self, game):
	
		self.game = game
		
		self.sub_state = "in_play" #None
		self.sub_states = { "fade_in": self.fade_in,
							"fade_out": self.fade_out,
							"in_play": self.in_play,
							"menu": self.menu,
							"iteming": self.iteming,
							"in_dialogue": self.in_dialogue,
							"switching": self.switching }
		
		self.input_focus = None # self.game.player
	
	def start(self):
		
		self.in_play = False
		self.ending = False
		
		self.game.terrain_renderer.update()	
				
		#debug; also needs to be put into Cutscene
		#self.engine.scene_painter.scene.sprites["2"].image.set_alpha(0)
		
		self.sub_state = "fade_in"		
		self.game.fader.fade_in()
	
	def fade_in(self): # enter?
	
		self.game.fader.update()
		self.game.terrain_renderer.render()
		self.game.display.blit(self.game.fader.curtain,(0,0))
		if self.game.fader.faded_in: self.sub_state = "in_play"
		
	def fade_out(self): # exit?
	
		self.game.fader.update()
		self.game.terrain_renderer.render()
		self.game.display.blit(self.game.fader.curtain,(0,0))
		if self.game.fader.faded_out:
			self.game.title_music.fadeout(800)
			self.game.switch_state("title")

	def menu(self): pass	
	def iteming(self): pass # WTF???	
	def in_dialogue(self): pass
	def switching(self): pass	

	def in_play(self):
	
		#TODO ??? self.input_focus.get_input()
		
		self.game.scene.update()
		
		#c = self.game.controller
		
		# TODO show where move_mob comes from
		#move_mob(self.game.player, 1 * c.x_axis, 1 * c.y_axis)
		#if self.game.controller.exit == 1:
		#	self.sub_state = "fade_out"
		#	self.game.fader.fade_out()
		
		#self.game.ui["dialoguebox"].update()
		#self.game.scene.update()
		#self.game.terrain_renderer.update()
		
		#self.game.terrain_renderer.render()
		#self.game.display.blit(self.game.fader.curtain,(0,0))
		#self.game.ui["dialoguebox"].render()
		#render(self.game.player, self.game.display)
		
	#def in_play(self): # leads to in_menu, in_dialogue, and fade_out
	
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
							"in_play": self.in_play,
							"in_menu": self.in_menu,
							"iteming": self.iteming,
							"in_dialogue": self.in_dialogue,
							"switching": self.switching }
							
	def in_play(self): # leads to in_menu, in_dialogue, and fade_out
	
		# TODO define all input control here!
	
		self.engine.player_character.move(self.engine.buttons["x_axis_"], self.engine.buttons["y_axis_"])
		
		if self.engine.buttons["A"] == 1: # apersistent
			self.engine.player_character.get_melee_rect()
				
		self.engine.scene_painter.update() # this calls scene.update()
		
	def update(self):
		
		self.sub_states[self.sub_state]()'''
