from random import random as rnd

import pygame


class Breadboard: # mirrors Game at a basic level

	def __init__(self):
	
		self.tick = 0
		self.clock = pygame.time.Clock()
		
		self.sys_messages = []
		
	def update(self):
	
		self.clock.tick(60)
		self.tick = (self.tick + 1) % 4096
		# there are 5 ticks per second @ 60 ticks
		for msg in self.sys_messages:
			msg.update()

class Sys_Message:

	def __init__(self, game, message):
		
		self.font = pygame.font.Font(None, 24)
	
		self.game = game
		self.game.sys_messages.append(self)
	
		self.message = self.font.render(message, 0, (0xff,0xff,0xff))
		self.tick = int(self.game.tick)
		self.fading = True
		self.alpha = 255
		self.done = False
		
	def update(self):
	
		# this would be better done with counting ticks in the main Game class
		print(self.tick, self.game.tick)
		self.fading = (self.game.tick - self.tick) >= 160
		self.alpha -= 8 * self.fading * ((self.game.tick - self.tick) % 2 == 0)
		#print(self.alpha)
		if self.alpha <= 0:
			self.alpha = 0
			self.done = True
		self.message.set_alpha(self.alpha)

#def render_sysmsg(messages, surface):

if __name__ == "__main__":

	pygame.init()
	
	display = pygame.display.set_mode((640,480))
	
	bb = Breadboard()
	
	#clock = pygame.time.Clock()
	
	rand_msgs = ["Saved screenshot0000.png", "Player gained a level", "Friend wants to talk to you"]
	font_height = pygame.font.Font(None, 24).get_height()

	running = True
	while running:
	
		#clock.tick(60)
	
		bb.update()
		
		for event in pygame.event.get():		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					Sys_Message(bb, rand_msgs[int(rnd() * 3)])
				if event.key == pygame.K_ESCAPE:
					running = False
					pygame.quit()
					exit()
			
		for i in range(1,6): # for 5 visible lines
			try:
				y = 480 - 10 * i - font_height * i
				display.blit(bb.sys_messages[-i].message,(10,y))			
			except:
				break
				
		pygame.display.flip()
		display.fill((0,0,0))
