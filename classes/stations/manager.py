import pygame as py
from .order import OrderStation

class StationManager:
    """ Менеджер управления станциями """
    def __init__(self):
        self.stations = {
            "order": OrderStation(),
        }
        self.current_station = "order"

    def handle_events(self, events):
        """ Обработка событий для всех станций """
        self.stations[self.current_station].events(events)

    def draw(self, screen):
        """ Отрисовка всего """
        # Рисуем текущую станцию
        current_station = self.stations[self.current_station]
        current_station.draw(screen)
