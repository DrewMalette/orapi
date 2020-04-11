

import pygame

class Sys_Message:

	def __init__(self, message):
	
		self.font = pygame.font.Font(None, 24)
	
		self.message = self.font.render(message, 0, (0xff,0xff,0xff))
		self.tick = pygame.time.get_ticks()
		self.fading = True
		self.alpha = 255
		self.done = False
		
	def update(self):
	
		self.fading = (pygame.time.get_ticks() - self.tick) >= 3000
		self.alpha -= 1 * self.fading
		print(self.alpha)
		if self.alpha <= 0:
			self.alpha = 0
			self.done = True
		self.message.set_alpha(self.alpha)

if __name__ == "__main__":

	pygame.init()
	
	display = pygame.display.set_mode((640,480))
	
	msg = Sys_Message("Message 1") #, 0, (0xff,0xff,0xff))
	
	while not msg.done:
	
		msg.update()
	
		display.blit(msg.message, (10,10))
	
		pygame.display.flip()
		display.fill((0,0,0))
