#!/usr/bin/env python3

import pygame

import orapi

def load_func(game):

	game.player = orapi.Mob(game, "mob_jon.png", "Jon")
	game.load_scene("scene1", "untitled.tmx")
	game.state = orapi.State_Gameplay(game)
	
pygame.init()

game = orapi.Game("0.1", load_func)

game.main()
