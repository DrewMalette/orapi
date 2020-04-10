#!/usr/bin/env python3

# a git test

# I'm the DJ Khaled of commits "Another one"

import pygame

import orapi

def load_func(game):

	scene1 = orapi.Scene("scene1", game)
	game.state = orapi.State_Gameplay(game)
	game.state.scene = scene1	
	game.player = orapi.Mob(game, "mob_jon.png", "Jon")
	
pygame.init()

game = orapi.Game("0.1", load_func)

game.main()
