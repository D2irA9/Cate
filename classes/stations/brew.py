from colors import *
from globals import *
from .base import Station

class BrewStation(Station):
    def __init__(self):
        super().__init__("Приготовление", BLACK, WHITE)

    def draw(self, screen):
        screen.fill(WHITE)

    def events(self, events):
        pass