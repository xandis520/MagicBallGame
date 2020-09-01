import pygame
import os, sys

class Game():
    def __init__(self):
        self.width = 720
        self.height = 480
        self.tps = 60
        # self.background = pygame.image.load(os.path.join("game_assets", "bg.png"))

        # Initialization
        pygame.init()
        self.resolution = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.resolution)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)

Game()
