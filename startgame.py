#!/usr/bin/env python3

# a git test

import pygame

import orapi

def load_func(game):

	game.state = orapi.State_Gameplay(game)
	
	game.player = orapi.Mob(game, "mob_jon.png", "Jon")
	
pygame.init()

game = orapi.Game("0.1", load_func)

game.main()
