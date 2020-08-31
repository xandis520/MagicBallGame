import pygame
import os


class GameMap:
    def __init__(self, game):
        self.game = game
        self.grass_img = pygame.image.load('game_assets/grass.png')
        self.grass_img = pygame.transform.scale(self.grass_img, (32, 32))
        self.dirt_img = pygame.image.load('game_assets/dirt.png')
        self.dirt_img = pygame.transform.scale(self.dirt_img, (32, 32))
        self.game_map = self.load_map('map')
        self.tile_rects = []

    def load_map(self, map_name):
        with open(map_name + '.txt', 'r') as map:
            data = map.read()

        data = data.split('\n')
        game_map =[]
        for row in data:
            game_map.append(list(row))
        return game_map

    def collision_check(self, player_rect):
        hit_list = []
        for tile in self.tile_rects:
            if player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def tick(self, camera_scroll):
        self.tile_rects = []
        y = 0
        for layer in self.game_map:
            x = 0
            for tile in layer:
                if tile != '0':
                    self.tile_rects.append(pygame.Rect(x * 32 - camera_scroll[0], y * 32, 32, 32))
                x += 1
            y += 1

    def draw(self, camera_scroll):
        y = 0
        for layer in self.game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    self.game.screen.blit(self.dirt_img, (x*32-camera_scroll[0], y*32))
                if tile == '2':
                    self.game.screen.blit(self.grass_img, (x*32-camera_scroll[0], y*32))
                x += 1
            y += 1

