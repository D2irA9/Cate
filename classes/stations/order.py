from colors import *
from globals import *
from .base import Station
from ..tiled import Map

class OrderStation(Station):
    """ Станция заказов """
    def __init__(self):
        super().__init__("Заказы", BLACK, GREEN)
        self.map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
        self.map_loaded = False

    def draw(self, screen):
        if not self.map_loaded:
            self.map.load_map()
            self.map_loaded = True

        self.map.draw(screen)

    def events(self, events):
        pass