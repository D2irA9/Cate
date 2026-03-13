import random
from ..node import ImageButton
from .order import OrderStation
from globals import *
from colors import *

class StationManager:
    """ Менеджер управления станциями """
    def __init__(self):
        self.stations = {
            "order": OrderStation(),
        }
        self.current_station = "order"
        # Настройки
        self.settings_show = False
        self.settings_btn = ImageButton("assets/sprites/settings/settings.png",(1140, 10), 2.5)
        self.volume_btn = ImageButton("assets/sprites/settings/up_volume.png", (350, 250), 4)

        # Музыка
        self.background_sounds = load_sounds_from_folder("assets/sounds/background")
        if self.background_sounds:
            self.sound = random.choice(self.background_sounds)
            self.current_channel = self.sound.play()
        else:
            self.sound = None
            self.current_channel = None

    def settings_draw(self, screen):
        """Настройки"""
        py.draw.rect(screen, SETTINGS_FON, (250, 180, 700, 400))
        py.draw.rect(screen, CONTOUR, (250, 180, 700, 400), 3)
        self.volume_btn.draw(screen)

    def update(self):
        if not self.background_sounds:
            return
        if self.current_channel is None or not self.current_channel.get_busy():
            if len(self.background_sounds) > 1:
                choices = [s for s in self.background_sounds]
                self.sound = random.choice(choices)
            else:
                self.sound = random.choice(self.background_sounds)
            self.current_channel = self.sound.play()

    def handle_events(self, events):
        """ Обработка событий для всех станций """
        self.update()
        for event in events:
            if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                self.settings_show = not self.settings_show
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                if self.settings_btn.signal(event.pos):
                    self.settings_show = not self.settings_show
        self.stations[self.current_station].events(events)

    def draw(self, screen):
        """ Отрисовка всего """
        # Рисуем текущую станцию
        current_station = self.stations[self.current_station]
        current_station.draw(screen)
        self.settings_btn.draw(screen)
        if self.settings_show:
            self.settings_draw(screen)