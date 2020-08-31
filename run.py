import configparser
from config import create_config
import pygame
import os
import sys
from player import Player, MagicBall
from game_map import GameMap


class Game(object):
    def __init__(self):
        # Configfile
        try:
            config = configparser.ConfigParser()
            config.read('config.cfg')
            default = config['DEFAULT']
            self.name = default['name']
            self.width = int(default['width'])
            self.height = int(default['height'])
            self.tps = int(default['tps'])
            filenames = config['FILENAMES']
            self.background = pygame.image.load(os.path.join("game_assets", filenames['background']))
        except KeyError:
            create_config()
            Game()

        # Initialization
        pygame.init()
        self.resolution = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.resolution)
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0
        self.game_map = GameMap(self)
        self.player = Player(self)
        self.magic_ball = MagicBall(self)

        # Run main loop
        self.run()

    def run(self):
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)

            # Ticking
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1 / self.tps:
                self.tick()
                self.tps_delta -= 1 / self.tps

                # Drawing
                self.draw()

    def tick(self):
        # self.game_map.tick(self.player.camera_scroll)
        self.player.tick()
        self.magic_ball.tick()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # self.game_map.draw(self.player.camera_scroll) # tutaj trzeba przekazac wartosc self.player.camera_scroll
        self.player.draw()
        self.magic_ball.draw()
        pygame.display.flip()


Game()
