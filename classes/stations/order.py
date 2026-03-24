from colors import *
from globals import *
from .base import Station
from ..tiled import Map
from ..character import Character
from ..db import db

class OrderStation(Station):
    def __init__(self):
        super().__init__("Заказы", BLACK, GREEN)
        self.map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
        self.map_loaded = False

        # Персонажи
        self.player = Character(3, (530, 60), 'assets/sprites/characters/player/Adam_16x16.png', [(530, 60)])
        self.split_index = None

    def draw(self, screen):
        if not self.map_loaded:
            self.map.load_map()
            self.map_loaded = True
            # по имени слоя
            # if 'walls' in self.map.layer_names:
            #     self.split_index = self.map.layer_names.index('walls') + 1
            self.split_index = 2

        # Рисуем нижние слои
        for i in range(self.split_index):
            self.map.draw_layer(screen, i)

        # Рисуем игрока
        self.player.update()
        self.player.draw(screen)

        # Рисуем верхние слои
        for i in range(self.split_index, len(self.map.layers)):
            self.map.draw_layer(screen, i)

    def events(self, events):
        pass