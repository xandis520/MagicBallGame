import pygame
from pygame.math import Vector2
import os


class Player:
    def __init__(self, game):
        self.game = game
        # Player
        self.player_image = pygame.image.load('game_assets/player.png')
        self.player_size = [self.game.width//10, self.game.width//10]
        self.player_image = pygame.transform.scale(self.player_image, (self.player_size[0], self.player_size[1]))
        self.player_location = [50, 50]
        self.player_location = Vector2(self.game.width / 2, self.game.height - self.player_size[1])

        # Rectangles
        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1],
                                       self.player_size[0], self.player_size[1])
        self.test_rect = pygame.Rect(100, 100, 200, 200)

        # Physics
        self.on_jump = False
        self.walk_speed = 1
        self.jump_speed = 50
        self.gravity = 1.5
        self.air_resistance = 0.9
        self.vel = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

        #  Moving animation
        self.walk_right = []
        self.walk_left = []
        character_directory = "game_assets"
        self.character = pygame.transform.scale(pygame.image.load(os.path.join(character_directory, "standing.png")),
                                                (self.player_size[0], self.player_size[1]))
        for i in range(1, 10):
            self.walk_right.append(
                pygame.transform.scale(pygame.image.load(os.path.join(character_directory, f"R{i}.png")),
                                       (self.player_size[0], self.player_size[1])))
            self.walk_left.append(
                pygame.transform.scale(pygame.image.load(os.path.join(character_directory, f"L{i}.png")),
                                       (self.player_size[0], self.player_size[1])))

        self.left = False
        self.right = False
        self.walk_count = 0
        # self.ball = MagicBall(self, game)

    def tick(self):
        self.move()

    def add_force(self, force):
        self.acceleration += force

    def move(self):
        # Input
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            if not self.on_jump:
                self.left = False
                self.right = True
            self.add_force(Vector2(self.walk_speed, 0))
        elif pressed[pygame.K_a]:
            if not self.on_jump:
                self.left = True
                self.right = False
            self.add_force(Vector2(-self.walk_speed, 0))
        else:
            self.right = False
            self.left = False
            self.walk_count = 0

        if not self.on_jump:
            if pressed[pygame.K_w]:
                self.on_jump = True
                self.right = False
                self.left = False
                self.walk_count = 0
                self.add_force(Vector2(0, -self.jump_speed))

        # Physics
        self.vel *= self.air_resistance  # Działanie oporu powietrza
        self.vel += Vector2(0, self.gravity)  # Działanie grawitacji
        self.vel += self.acceleration  # Działanie przyspieszenia nadanego przez gracza
        self.player_location += self.vel  # Aktualizacja pozycji gracza
        self.acceleration *= 0  # Reset przyspieszenia

        # Check if player on_jump
        if self.on_jump:
            if self.player_location[1] >= self.game.height - self.player_size[1]:
                # Zamiana na ground point lub collision check
                self.on_jump = False

        # Staying on the ground - player don't fall under the screen
        if self.player_location[1] > self.game.height - self.player_size[1]:
            self.player_location[1] = self.game.height - self.player_size[1]

        # Player hitbox position
        self.player_rect.x = self.player_location[0]
        self.player_rect.y = self.player_location[1]

    def draw(self):
        # Drawing player hitbox
        pygame.draw.rect(self.game.screen, (50, 55, 10), self.player_rect)

        # Drawing test hitbox
        if self.player_rect.colliderect(self.test_rect):
            pygame.draw.rect(self.game.screen, (255, 0, 0), self.test_rect)
        else:
            pygame.draw.rect(self.game.screen, (0, 255, 0), self.test_rect)

        # Drawing player on screen
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if self.left:
            self.game.screen.blit(self.walk_left[self.walk_count // 3],
                                  (self.player_location[0], self.player_location[1]))
            self.walk_count += 1
        elif self.right:
            self.game.screen.blit(self.walk_right[self.walk_count // 3],
                                  (self.player_location[0], self.player_location[1]))
            self.walk_count += 1
        elif self.on_jump:
            self.game.screen.blit(self.character, (self.player_location[0], self.player_location[1]))
        else:
            self.game.screen.blit(self.character, (self.player_location[0], self.player_location[1]))


class MagicBall:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        # Ball
        self.ball_min = self.player.player_size[0]//10
        self.ball_max = self.player.player_size[0]//3
        self.ball_x = int(self.player.player_location[0] + self.player.player_size[0]//2)
        self.ball_y = int(self.player.player_location[1] + self.player.player_size[1]//2)

        self.ball_load = False

    def tick(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            self.ball_load = True
        else:
            self.ball_load = False

    def draw(self):
        if self.ball_load:
            self.ball_x = int(self.player.player_location[0] + self.player.player_size[0])
            self.ball_y = int(self.player.player_location[1] + self.player.player_size[1] // 2)
            pygame.draw.circle(self.game.screen, (100, 5, 5), (self.ball_x, self.ball_y+self.ball_min//2), self.ball_min)
