#!/usr/bin/env python3

import pygame

import orapi

def load_func(game):

	game.player = orapi.Mob(game, "data/image/mob_jon.png", "Jon")
	game.load_scene("scene1", "data/terrain/untitled.tmx")
	game.switch_state("title")
	
pygame.init()

game = orapi.Game("0.1", load_func)

game.main()
