import random
from ..node import ImageButton
from .order import OrderStation
from globals import *
from colors import *

class Slider:
    def __init__(self, line_rect, handle_sprite, initial_val=1.0):
        self.line_rect = line_rect
        self.handle_sprite = handle_sprite
        self.handle_width = handle_sprite.get_width()
        self.handle_height = handle_sprite.get_height()
        self.min_val = 0.0
        self.max_val = 1.0
        self.val = initial_val
        self.grabbed = False

    def get_handle_pos(self):
        """Возвращает позицию центра ручки"""
        x = self.line_rect.x + self.val * self.line_rect.width
        y = self.line_rect.centery
        return (x, y)

    def handle_rect(self):
        """Прямоугольник для проверки попадания мыши в ручку"""
        x, y = self.get_handle_pos()
        return py.Rect(x - self.handle_width//2, y - self.handle_height//2,
                       self.handle_width, self.handle_height)

    def update(self, events):
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                if self.handle_rect().collidepoint(event.pos):
                    self.grabbed = True
                elif self.line_rect.collidepoint(event.pos):
                    # Клик на линии – сразу перемещаем ручку
                    rel_x = event.pos[0] - self.line_rect.x
                    self.val = rel_x / self.line_rect.width
                    self.val = max(self.min_val, min(self.max_val, self.val))
                    self.grabbed = True
            elif event.type == py.MOUSEBUTTONUP and event.button == 1:
                self.grabbed = False
            elif event.type == py.MOUSEMOTION and self.grabbed:
                rel_x = event.pos[0] - self.line_rect.x
                self.val = rel_x / self.line_rect.width
                self.val = max(self.min_val, min(self.max_val, self.val))
        return self.val

    def draw(self, screen):
        """Рисует только ручку (линия уже нарисована отдельно)"""
        x, y = self.get_handle_pos()
        screen.blit(self.handle_sprite, (x - self.handle_width//2, y - self.handle_height//2))


class StationManager:
    def __init__(self):
        self.stations = {
            "order": OrderStation(),
        }
        self.current_station = "order"
        # Настройки
        self.settings_show = False
        self.settings_btn = ImageButton("assets/sprites/settings/settings.png", (1140, 10), 2.5)

        # Звук – кнопка вкл/выкл
        scale = 4
        vol_on_img = py.image.load("assets/sprites/settings/up_volume.png").convert_alpha()
        vol_off_img = py.image.load("assets/sprites/settings/off_volume.png").convert_alpha()
        w = vol_on_img.get_width() * scale
        h = vol_on_img.get_height() * scale
        self.vol_on_scaled = py.transform.scale(vol_on_img, (w, h))
        self.vol_off_scaled = py.transform.scale(vol_off_img, (w, h))

        self.volume_btn = ImageButton("assets/sprites/settings/up_volume.png", (350, 250), 1)
        self.volume_btn.image = self.vol_on_scaled
        self.volume_btn.rect = self.volume_btn.image.get_rect(topleft=(350, 250))
        self.sound_enabled = True
        self.volume_level = 1.0

        # Ползунок – загружаем спрайт ручки
        slider_handle_img = py.image.load("assets/sprites/settings/slider.png").convert_alpha()
        # Масштабируем ручку до удобного размера (например, 20x20)
        self.slider_handle = py.transform.scale(slider_handle_img, (20, 20))
        # Прямоугольник линии (такой же, как будет нарисован в settings_draw)
        self.slider_line_rect = py.Rect(460, 275, 350, 10)
        self.slider = Slider(self.slider_line_rect, self.slider_handle, initial_val=self.volume_level)

        # Музыка
        self.background_sounds = load_sounds_from_folder("assets/sounds/music/background")
        if self.background_sounds:
            self.sound = random.choice(self.background_sounds)
            self.current_channel = self.sound.play()
            self.set_volume()
        else:
            self.sound = None
            self.current_channel = None

    def set_volume(self):
        if self.current_channel:
            vol = self.volume_level if self.sound_enabled else 0.0
            self.current_channel.set_volume(vol)

    def settings_draw(self, screen):
        py.draw.rect(screen, SETTINGS_FON, (250, 180, 700, 400))
        py.draw.rect(screen, CONTOUR, (250, 180, 700, 400), 3)
        self.volume_btn.draw(screen)
        # Рисуем линию
        py.draw.rect(screen, CONTOUR, self.slider_line_rect)
        # Рисуем ручку ползунка
        self.slider.draw(screen)

    def update(self):
        if not self.background_sounds:
            return
        if self.current_channel is None or not self.current_channel.get_busy():
            if len(self.background_sounds) > 1:
                choices = [s for s in self.background_sounds if s != self.sound]
                self.sound = random.choice(choices) if choices else random.choice(self.background_sounds)
            else:
                self.sound = random.choice(self.background_sounds)
            self.current_channel = self.sound.play()
            self.set_volume()

    def handle_events(self, events):
        self.update()

        if self.settings_show:
            new_vol = self.slider.update(events)
            if new_vol != self.volume_level:
                self.volume_level = new_vol
                self.set_volume()

        for event in events:
            if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                self.settings_show = not self.settings_show
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                if self.settings_btn.signal(event.pos):
                    self.settings_show = not self.settings_show
                if self.settings_show and self.volume_btn.signal(event.pos):
                    self.sound_enabled = not self.sound_enabled
                    if self.sound_enabled:
                        self.volume_btn.image = self.vol_on_scaled
                    else:
                        self.volume_btn.image = self.vol_off_scaled
                    self.set_volume()
        self.stations[self.current_station].events(events)

    def draw(self, screen):
        current_station = self.stations[self.current_station]
        current_station.draw(screen)
        self.settings_btn.draw(screen)
        if self.settings_show:
            self.settings_draw(screen)