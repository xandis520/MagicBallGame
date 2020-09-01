import pygame
from pygame.math import Vector2
import os
from game_map import GameMap
import math


class Player:
    def __init__(self, game):
        self.game = game
        # self.map = GameMap
        self.map = self.game.game_map
        # Player
        self.player_size = [self.game.width//10, self.game.width//10]
        self.player_image = pygame.image.load('game_assets/player.png')
        self.player_image = pygame.transform.scale(self.player_image, (self.player_size[0], self.player_size[1]))
        self.player_location = [50, 0] # Player run location
        # self.player_location = Vector2(self.game.width // 2, self.game.height - self.player_size[1])

        # Rectangles
        self.player_rect = pygame.Rect(self.player_location[0], self.player_location[1],
                                       self.player_size[0], self.player_size[1])
        self.test_rect = pygame.Rect(100, 150, 30, 30)

        # Physics
        self.on_jump = False
        self.walk_speed = 0.8
        self.jump_speed = 50
        self.gravity = 1.5
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
        self.camera_scroll = Vector2(0, 0)
        self.grass_img = pygame.image.load('game_assets/grass.png')
        self.grass_img = pygame.transform.scale(self.grass_img, (32, 32))
        self.dirt_img = pygame.image.load('game_assets/dirt.png')
        self.dirt_img = pygame.transform.scale(self.dirt_img, (32, 32))
        self.game_map = self.load_map('map')
        self.tile_rects = []
        self.scroll_x = 0

    def load_map(self, map_name):
        with open(map_name + '.txt', 'r') as map:
            data = map.read()

        data = data.split('\n')
        game_map =[]
        for row in data:
            game_map.append(list(row))
        return game_map

    def tick(self):
        self.move()
        # self.scroll_x = -self.scroll_x//1 + self.player_location[0]//1
        # self.camera_scroll = Vector2(self.scroll_x, 0)
        # Camera movement

    def tiles(self):
        self.tile_rects = []
        y = 0
        for layer in self.game_map:
            x = 0
            for tile in layer:
                if tile != '0':
                    self.tile_rects.append(pygame.Rect(x * 32 - self.camera_scroll[0], y * 32, 32, 32))
                x += 1
            y += 1

    def add_force(self, force):
        self.acceleration += force

    def map_collision(self):
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.player_location[0] += self.vel[0]
        self.player_rect.x = self.player_location[0]
        hit_list = self.collision_check()
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
        hit_list = self.collision_check()
        for tile in hit_list:
            if self.vel[1] > 0:
                #     Tu jest błąd lub nizej. Gdy kolizja jest z podłogą, a postać ma velocity nizsze od 0 to teleportuje postac ciagle  w lewa strone
                self.player_location[1] = tile.top - self.player_size[1]
                self.player_rect.y = self.player_location[1]
                self.collision_types['bottom'] = True
            elif self.vel[1] < 0:
                self.player_location[1] = tile.bottom
                self.player_rect.y = self.player_location[1]
                self.collision_types['top'] = True

    def collision_check(self):
        hit_list = []
        for tile in self.tile_rects:
            if self.player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self):
        print('1loc:', self.player_location[0])
        print('1:', self.vel[0])
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
        self.acceleration *= 0  # Reset przyspieszenia
        if not self.left and not self.right:
            if math.fabs(self.vel[0]) < 0.1:
                self.vel[0] = 0
            if self.collision_types['bottom']:
                self.vel[0] *= self.friction


        # Collision with game map tiles
        self.map_collision()

        # Check if player on_jump
        if not self.on_jump:
            if not self.collision_types['bottom']:
                self.on_jump = True
        if self.on_jump:
            if self.collision_types['bottom']:
                # Zamiana na ground point lub collision check
                self.on_jump = False

            # Postać przyspiesza po odbiciu i szybciej spada w dół
            if self.collision_types['top']:
                if self.left:
                    self.vel += Vector2(2, 0)
                if self.right:
                    self.vel += Vector2(-2, 0)
                self.vel = Vector2(0, 5)

        # Staying on the ground - player don't fall under the screen
        # if self.player_rect.y > self.game.height - self.player_size[1]:
        #     self.player_rect.y = self.game.height - self.player_size[1]
        #     self.on_jump = False

        # if self.player_location[1] > self.game.height - self.player_size[1]:
        #     self.player_location[1] = self.game.height - self.player_size[1]
        #     self.on_jump = False

        # Player hitbox position
        # self.player_rect.x = self.player_location[0]
        # self.player_rect.y = self.player_location[1]

        # Player position after collision check
        self.tiles()
        # self.player_location = Vector2(self.player_rect.x, self.player_rect.y)
        self.player_rect.x = self.player_location[0]
        self.player_rect.y = self.player_location[1]
        print('3loc:', self.player_location[0])
        print('3:', self.vel[0])

    def draw(self):
        # Drawing player hitbox
        pygame.draw.rect(self.game.screen, (50, 55, 10), self.player_rect)

        # Drawing test hitbox
        # if self.player_rect.colliderect(self.test_rect):
        #     pygame.draw.rect(self.game.screen, (255, 0, 0), self.test_rect)
        # else:
        #     pygame.draw.rect(self.game.screen, (0, 255, 0), self.test_rect)

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

        y = 0
        for layer in self.game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    self.game.screen.blit(self.dirt_img, (x*32-self.camera_scroll[0], y*32))
                if tile == '2':
                    self.game.screen.blit(self.grass_img, (x*32-self.camera_scroll[0], y*32))
                x += 1
            y += 1


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
