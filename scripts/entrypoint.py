# entrypoint.py

import pygame
import orapi

def exposition(scene):
	
	c = scene.game.controller			
	if c.exit == 1:	scene.par_state.sub_state = "fade_out"; scene.game.fader.fade_out()
		
	scene.game.ui["dialoguebox"].update()
		
	scene.game.terrain_renderer.render()
	scene.game.ui["dialoguebox"].render()
		
def wait_for_pizza(scene):

	c = scene.game.controller		
	orapi.move_mob(scene.game.player, 1 * c.x_axis, 1 * c.y_axis)
	if c.exit == 1:	scene.par_state.sub_state = "fade_out"; scene.game.fader.fade_out()
	
	scene.game.terrain_renderer.update()	
	
	scene.game.terrain_renderer.render()
	scene.game.ui["dialoguebox"].render()

_locals = locals()

def run():

	pygame.init()

	game = orapi.Game("0.2")
	# TODO define ui components here
	game.player = orapi.Mob(game, "data/image/mob_jon.png", "Jon")
	game.load_scene("scene1", _locals, "data/terrain/cclivrm.tmx", "wait_for_pizza") # TODO does not reset
	game.switch_state("title")
	
	game.main()

