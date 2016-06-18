import sys, os
sys.dont_write_bytecode = True
os.environ["SDL_VIDEO_CENTERED"] = '1'
import pygame
from pygame.locals import *

import config

pygame.init()

class Main:
	def __init__(self):
		self.window = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
		pygame.display.set_caption(config.SCREEN_TITLE)

		self.fpsClock = pygame.time.Clock()

	def exit(self):
		pygame.quit()
		sys.exit()

	def run(self):
		while True:
			self.fpsClock.tick(config.FRAMERATE)
			# Event handling
			for event in pygame.event.get():
				if event.type == QUIT:
					self.exit()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self.exit()

			# Logic

			# Rendering
			self.window.fill(config.SCREEN_FILL)

			pygame.display.update()


if __name__ == "__main__":
	m = Main()
	m.run()