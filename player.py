import pygame
from pygame.math import Vector2
import os
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.map = self.game.game_map
        # Player
        self.player_size = [self.game.width//10, self.game.width//10]
        self.player_size = [64, 64]
        self.player_image = pygame.image.load('game_assets/player.png')
        self.player_image = pygame.transform.scale(self.player_image, (self.player_size[0], self.player_size[1]))
        start_x = (self.game.width - self.player_size[0])//2
        # start_y = self.game.height - self.player_size[1] - 50
        start_y = 0
        self.player_location = [start_x, start_y] # Player run location

        # Rectangles
        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1],
                                       self.player_size[0], self.player_size[1])
        self.test_rect = pygame.Rect(100, 150, 30, 30)

        # Physics
        self.on_jump = False
        self.walk_speed = 0.8
        self.jump_speed = 50
        self.gravity = 1.3
        self.air_resistance = 0.9
        self.friction = 0.8
        self.vel = Vector2(0, 0) # Parametr przechowujący aktualną prędkość obiektu (składowa wszystkich sił)
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
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        # Player camera
        self.scroll_x = self.player_rect.x -self.game.width//2 + self.player_size[0]//2
        self.camera_scroll = Vector2(self.scroll_x, 0)

        # Sounds
        self.jump_sound = pygame.mixer.Sound('game_assets/sounds/jump.wav')

    def scroll(self):
        self.camera_scroll[0] += (self.player_rect.x - self.camera_scroll[0]-self.game.width//2 + self.player_size[0]//2)//8
        self.camera_scroll[1] += (self.player_rect.y - self.camera_scroll[1] - self.game.height//2 + self.player_size[1]//2)//22

    def tick(self):
        self.move()
        self.scroll()

    def add_force(self, force):
        self.acceleration += force

    def map_collision(self):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.player_location[0] += self.vel[0]
        self.player_rect.x = self.player_location[0]
        hit_list = self.map.collision_check(self.player_rect)
        for tile in hit_list:
            if self.vel[0] > 0:
                self.player_location[0] = tile.left - self.player_size[0]
                self.player_rect.x = self.player_location[0]
                self.collision_types['right'] = True
            elif self.vel[0] < 0:
                self.player_location[0] = tile.right
                self.player_rect.x = self.player_location[0]
                self.collision_types['left'] = True

        self.player_location[1] += self.vel[1]
        self.player_rect.y = self.player_location[1]
        hit_list = self.map.collision_check(self.player_rect)
        for tile in hit_list:
            if self.vel[1] > 0:
                self.player_location[1] = tile.top - self.player_size[1]
                self.player_rect.y = self.player_location[1]
                self.collision_types['bottom'] = True
            elif self.vel[1] < 0:
                self.player_location[1] = tile.bottom
                self.player_rect.y = self.player_location[1]
                self.collision_types['top'] = True

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
                self.jump_sound.play()
                self.on_jump = True
                self.right = False
                self.left = False
                self.walk_count = 0
                self.add_force(Vector2(0, -self.jump_speed))

        # Physics
        self.vel *= self.air_resistance  # Działanie oporu powietrza
        self.vel += Vector2(0, self.gravity)  # Działanie grawitacji
        self.vel += self.acceleration  # Działanie przyspieszenia nadanego przez gracza
        self.acceleration *= 0  # Reset przyspieszenia
        if not self.left and not self.right:
            if math.fabs(self.vel[0]) < 0.1:
                self.vel[0] = 0
            if self.collision_types['bottom']:
                self.vel[0] *= self.friction

        self.map_collision()

        # Check if player on_jump
        if not self.on_jump:
            if not self.collision_types['bottom']:
                self.on_jump = True
        if self.on_jump:
            if self.collision_types['bottom']:
                self.on_jump = False

            # Postać przyspiesza po odbiciu i szybciej spada w dół
            if self.collision_types['top']:
                if self.left:
                    self.vel += Vector2(2, 0)
                if self.right:
                    self.vel += Vector2(-2, 0)
                self.vel = Vector2(0, 5)

        # Rect position after collision check
        self.player_rect.x = self.player_location[0]
        self.player_rect.y = self.player_location[1]

    def draw(self):
        # Drawing player hitbox
        # pygame.draw.rect(self.game.screen, (50, 55, 10), self.player_rect)

        # Drawing player on screen
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        position_x = self.player_location[0]-self.camera_scroll[0]
        position_y = self.player_location[1]-self.camera_scroll[1]

        if self.left:
            self.game.screen.blit(self.walk_left[self.walk_count // 3], (position_x, position_y))
            self.walk_count += 1
        elif self.right:
            self.game.screen.blit(self.walk_right[self.walk_count // 3], (position_x, position_y))
            self.walk_count += 1
        elif self.on_jump:
            self.game.screen.blit(self.character, (position_x, position_y))
        else:
            self.game.screen.blit(self.character, (position_x, position_y))


class MagicBall:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        # Ball
        self.ball_min = self.player.player_size[0]//10
        self.ball_max = self.player.player_size[0]//3
        self.ball_x0 = self.player.player_location[0] + self.player.player_size[0]//2 - 10
        self.ball_y0 = self.player.player_location[1] + self.player.player_size[1]//2

        self.ball_image = pygame.image.load('game_assets/ball.png')
        self.ball_size = [20, 20]
        # self.ball_image = pygame.transform.scale(self.ball_image, (self.ball_size[0], self.ball_size[1]))
        self.ball_load = False

        self.mouse_pos = (0, 0)
        self.radius = 40
        self.aA = self.ball_x0 - self.mouse_pos[0] - self.player.camera_scroll[0]  # X axis
        self.bA = self.ball_y0 - self.mouse_pos[1] - self.player.camera_scroll[1]  # Y axis
        self.R = math.sqrt(self.aA ** 2 + self.bA ** 2)
        self.aB = self.radius * self.aA / self.R
        self.bB = self.radius * self.bA / self.R
        self.xB = self.ball_x0 - self.aB - self.ball_size[0] // 2
        self.yB = self.ball_y0 - self.bB - self.ball_size[1] // 2
        self.ball_position = [self.xB, self.yB]

        # Throw ball
        self.vector = Vector2(0, 0)
        self.vel = Vector2(0, 0)
        self.ball_throw = False
        self.existing_time = 0

        self.ball_rect = pygame.Rect(self.xB-self.ball_size[0]//2, self.yB-self.ball_size[1]//2, self.ball_size[0], self.ball_size[1])
        self.size_count = 0

    def map_collision(self):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.player_location[0] += self.vel[0]
        self.player_rect.x = self.player_location[0]
        hit_list = self.map.collision_check(self.player_rect)
        for tile in hit_list:
            if self.vel[0] > 0:
                self.player_location[0] = tile.left - self.player_size[0]
                self.player_rect.x = self.player_location[0]
                self.collision_types['right'] = True
            elif self.vel[0] < 0:
                self.player_location[0] = tile.right
                self.player_rect.x = self.player_location[0]
                self.collision_types['left'] = True

        self.player_location[1] += self.vel[1]
        self.player_rect.y = self.player_location[1]
        hit_list = self.map.collision_check(self.player_rect)
        for tile in hit_list:
            if self.vel[1] > 0:
                self.player_location[1] = tile.top - self.player_size[1]
                self.player_rect.y = self.player_location[1]
                self.collision_types['bottom'] = True
            elif self.vel[1] < 0:
                self.player_location[1] = tile.bottom
                self.player_rect.y = self.player_location[1]
                self.collision_types['top'] = True

    def ball_pos(self):
        # Ball position
        self.ball_x0 = self.player.player_location[0] + self.player.player_size[0] // 2
        self.ball_y0 = self.player.player_location[1] + self.player.player_size[1] // 2
        self.mouse_pos = pygame.mouse.get_pos()
        self.aA = self.ball_x0 - self.mouse_pos[0] - self.player.camera_scroll[0]  # X axis
        self.bA = self.ball_y0 - self.mouse_pos[1] - self.player.camera_scroll[1] # Y axis
        self.R = math.sqrt(self.aA ** 2 + self.bA ** 2)
        self.aB = self.radius * self.aA / self.R
        self.bB = self.radius * self.bA / self.R
        self.xB = self.ball_x0 - self.aB - self.ball_size[0] // 2
        self.yB = self.ball_y0 - self.bB - self.ball_size[1] // 2
        self.ball_position = [self.xB, self.yB]

    def throw(self):
        # Throw vector
        print(self.vel)
        if self.existing_time <= 60:
            self.vel[0] *= 0.98
            self.vel += Vector2(0, self.player.gravity/4)
            self.ball_position[0] += self.vel[0]
            self.ball_position[1] += self.vel[1]
            self.existing_time += 1
        else:
            self.existing_time = 0
            self.ball_throw = False
            self.ball_load = False
            self.ball_size = [20, 20]
            self.ball_position = [self.xB, self.yB]

    def size(self):
        if self.size_count >= 2:
            self.ball_size[0] += 1
            self.ball_size[1] += 1
            self.size_count = 0
            if self.ball_size[0] >= 60:
                # Throw ball
                self.ball_throw = True
                self.vel = Vector2(-self.aA / self.R, -self.bA / self.R) * 3
                self.throw()
        else:
            self.size_count += 1

    def tick(self):
        print(self.ball_load, self.ball_throw)
        pressed = pygame.key.get_pressed()
        if not self.ball_throw:
            if pressed[pygame.K_SPACE]:
                self.ball_load = True
                self.ball_pos()
                self.size()
            elif self.ball_load:
                if pressed[pygame.MOUSEBUTTONDOWN]:
                    print('Throw')
                # Throw ball
                self.ball_throw = True
                self.ball_load = False
                self.vel = Vector2(-self.aA / self.R, -self.bA / self.R) * 20
                self.throw()
        if self.ball_throw:
            self.throw()

    def draw(self):
        if self.ball_load or self.ball_throw:
            ball_copy = self.ball_image.copy()
            ball_copy = pygame.transform.scale(ball_copy, (self.ball_size[0], self.ball_size[1]))
            # pygame.draw.circle(self.game.screen, (100, 5, 5), (self.ball_x, self.ball_y+self.ball_min//2), self.ball_min)
            self.game.screen.blit(ball_copy, (self.ball_position[0]-self.player.camera_scroll[0], self.ball_position[1]-self.player.camera_scroll[1]))
            # self.ball_image = pygame.transform.scale(self.ball_image, (int(self.ball_size[0]), int(self.ball_size[1])))
