#!/usr/bin/env python3

import pygame

import orapi

def load_func(game):

	print("Open Rhombus Action RPG engine (MMXX)")
	print(game.version)

pygame.init()

game = orapi.Game("0.1", load_func)

game.main()
