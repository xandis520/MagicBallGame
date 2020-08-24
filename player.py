import pygame
from pygame.math import Vector2

class Player:
    def __init__(self, game):
        self.game = game
        self.player_image = pygame.image.load('game_assets/player.png')
        self.player_size = [60, 120]
        self.player_image = pygame.transform.scale(self.player_image, (self.player_size[0], self.player_size[1]))
        self.player_location = [50, 50]
        self.player_location = Vector2(self.game.width / 2, self.game.height - self.player_size[1])
        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1], self.player_size[0], self.player_size[1])
        self.test_rect = pygame.Rect(100, 100, 200, 200)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)

    def add_force(self, force):
        self.player_location += force

    def tick(self):
        # Input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            self.add_force(Vector2(20, 0))
        if pressed[pygame.K_a]:
            self.add_force(Vector2(-20, 0))
        if pressed[pygame.K_w]:
            self.add_force(Vector2(0, -20))
        if pressed[pygame.K_s]:
            self.add_force(Vector2(0, 20))

        if self.player_location[1] > self.game.height - self.player_size[1]:
            self.player_location[1] = self.game.height - self.player_size[1]

        self.player_rect.x = self.player_location[0]
        self.player_rect.y = self.player_location[1]


    def draw(self):
        pygame.draw.rect(self.game.screen, (50, 55, 10), self.player_rect)
        if self.player_rect.colliderect(self.test_rect):
            pygame.draw.rect(self.game.screen, (255, 0, 0), self.test_rect)
        else:
            pygame.draw.rect(self.game.screen, (0, 255, 0), self.test_rect)
            # if self.game.event.type == pygame.KEYDOWN:
            #     if self.game.event.key == pygame.K_SPACE:
            #         self.add_force(Vector2(0, -20))
        self.game.screen.blit(self.player_image, (self.player_location[0], self.player_location[1]))
