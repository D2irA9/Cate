from ..node import ImageButton
from .order import OrderStation
from globals import *

class StationManager:
    """ Менеджер управления станциями """
    def __init__(self):
        self.stations = {
            "order": OrderStation(),
        }
        self.current_station = "order"
        self.settings_btn = ImageButton("assets/sprites/settings.png",(1140, 10), 2.5)

    def handle_events(self, events):
        """ Обработка событий для всех станций """
        for event in events:
            if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                print("ESC нажата")
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                if self.settings_btn.signal(event.pos):
                    print("Кнопка настроек нажата!")
        self.stations[self.current_station].events(events)

    def draw(self, screen):
        """ Отрисовка всего """
        # Рисуем текущую станцию
        current_station = self.stations[self.current_station]
        current_station.draw(screen)
        self.settings_btn.draw(screen)