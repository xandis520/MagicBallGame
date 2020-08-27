import pygame
import os


class GameMap:
    def __init__(self, game):
        self.game = game
        self.grass_img = pygame.image.load('game_assets/grass.png')
        self.grass_img = pygame.transform.scale(self.grass_img, (32, 32))
        self.dirt_img = pygame.image.load('game_assets/dirt.png')
        self.dirt_img = pygame.transform.scale(self.dirt_img, (32, 32))
        self.game_map = [
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['2', '0', '0', '0', '0', '0', '0', '0', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['1', '0', '0', '0', '0', '0', '2', '2', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['1', '2', '2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '2', '2'],
            ['1', '1', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
        ]
        self.tile_rects = []

    def collision_check(self, player_rect):
        hit_list = []
        for tile in self.tile_rects:
            if player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, obj_rect, obj_location, movement):
        collision_types = {
            'top': False,
            'bottom': False,
            'right': False,
            'left': False
        }
        hit_list = self.collision_check(player_rect)
        for tile in hit_list:
            if movement[0] > 0:
                collision_types['right'] = True
            elif movement[0] < 0:
                collision_types['left'] = True
        hit_list = self.collision_check(player_rect)
        for tile in hit_list:
            if movement[1] > 0:
                collision_types['bottom'] = True
            if movement[1] < 0:
                collision_types['top'] = True
        return collision_types

    def tick(self):
        pass

    def draw(self):
        y = 0
        for layer in self.game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    self.game.screen.blit(self.dirt_img, (x*32, y*32))
                if tile == '2':
                    self.game.screen.blit(self.grass_img, (x*32, y*32))
                if tile != '0':
                    self.tile_rects.append(pygame.Rect(x*16, y*16, 16, 16))
                x += 1
            y += 1

