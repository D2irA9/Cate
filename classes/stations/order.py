from colors import *
from .base import Station

class OrderStation(Station):
    """ Станция заказов """
    def __init__(self):
        super().__init__("Заказы", BLACK, GREEN)

    def draw(self, screen):
        screen.fill(WHITE)

    def events(self, events):
        pass