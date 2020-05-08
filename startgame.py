#!/usr/bin/env python3

import pygame

import orapi
import userscripts

def load_func(game):

	game.player = orapi.Mob(game, "data/image/mob_jon.png", "Jon")
	game.load_scene("scene1", userscripts.scene1._locals, "data/terrain/cclivrm.tmx", "wait_for_pizza") 
	game.switch_state("title")
	
pygame.init()

game = orapi.Game("0.1", load_func)

game.main()
