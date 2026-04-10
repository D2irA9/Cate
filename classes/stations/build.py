from colors import *
from globals import *
from .base import Station

class BuildStation(Station):
    def __init__(self):
        super().__init__("Сборка", WHITE, BLACK)

    def draw(self, screen):
        screen.fill(BLACK)

    def events(self, events):
        pass