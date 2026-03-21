from ..node import ImageButton, font
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
        x, y = self.get_handle_pos()
        screen.blit(self.handle_sprite, (x - self.handle_width//2, y - self.handle_height//2))


class StationManager:
    def __init__(self, sound_manager):
        self.stations = {
            "order": OrderStation(),
        }
        self.current_station = "order"

        self.sound_manager = sound_manager
        # Настройки
        self.settings_show = False
        self.settings_btn = ImageButton("assets/sprites/settings/settings.png", (1140, 10), 2.5)

        scale = 4
        # Кнопка музыки
        music_on_img = py.image.load("assets/sprites/settings/on_music.png").convert_alpha()
        music_off_img = py.image.load("assets/sprites/settings/off_music.png").convert_alpha()
        w = music_on_img.get_width() * scale
        h = music_on_img.get_height() * scale
        self.music_on_scaled = py.transform.scale(music_on_img, (w, h))
        self.music_off_scaled = py.transform.scale(music_off_img, (w, h))

        self.music_btn = ImageButton("assets/sprites/settings/on_music.png", (400, 280), 1)
        self.music_btn.image = self.music_on_scaled
        self.music_btn.rect = self.music_btn.image.get_rect(topleft=(400, 280))

        # Кнопка звуков
        sfx_on_img = py.image.load("assets/sprites/settings/on_volume.png").convert_alpha()
        sfx_off_img = py.image.load("assets/sprites/settings/off_volume.png").convert_alpha()
        w_sfx = sfx_on_img.get_width() * scale
        h_sfx = sfx_on_img.get_height() * scale
        self.sfx_on_scaled = py.transform.scale(sfx_on_img, (w_sfx, h_sfx))
        self.sfx_off_scaled = py.transform.scale(sfx_off_img, (w_sfx, h_sfx))

        self.sfx_btn = ImageButton("assets/sprites/settings/on_volume.png", (400, 350), 1)
        self.sfx_btn.image = self.sfx_on_scaled
        self.sfx_btn.rect = self.sfx_btn.image.get_rect(topleft=(400, 350))

        # Ползунки
        slider_handle_img = py.image.load("assets/sprites/settings/slider.png").convert_alpha()
        self.slider_handle = py.transform.scale(slider_handle_img, (20, 20))
        self.music_slider_line = py.Rect(460, 305, 350, 10)
        self.music_slider = Slider(self.music_slider_line, self.slider_handle, initial_val=self.sound_manager.music_volume)
        self.sfx_slider_line = py.Rect(460, 375, 350, 10)
        self.sfx_slider = Slider(self.sfx_slider_line, self.slider_handle, initial_val=self.sound_manager.sfx_volume)
        self.music_btn.image = self.music_on_scaled if self.sound_manager.music_enabled else self.music_off_scaled
        self.sfx_btn.image = self.sfx_on_scaled if self.sound_manager.sfx_enabled else self.sfx_off_scaled

        self.sound_manager.start_music("background")

    def settings_draw(self, screen):
        py.draw.rect(screen, SETTINGS_FON, (250, 180, 700, 400))
        py.draw.rect(screen, CONTOUR, (250, 180, 700, 400), 3)

        # Текст
        text_setting = font.text_ret(size=42, text='Настройки', color=GRAY)
        text_rect = text_setting.get_rect()
        screen.blit(text_setting, ((1200 // 2) - text_rect.centerx, 230))

        # Музыка
        self.music_btn.draw(screen)
        py.draw.rect(screen, CONTOUR, self.music_slider_line)
        self.music_slider.draw(screen)

        # Звуки
        self.sfx_btn.draw(screen)
        py.draw.rect(screen, CONTOUR, self.sfx_slider_line)
        self.sfx_slider.draw(screen)

    def handle_events(self, events):
        # Обновление состояния музыки
        self.sound_manager.update()

        if self.settings_show:
            # Обработка ползунков
            new_music_vol = self.music_slider.update(events)
            if new_music_vol != self.sound_manager.music_volume:
                self.sound_manager.set_music_volume(new_music_vol)

            new_sfx_vol = self.sfx_slider.update(events)
            if new_sfx_vol != self.sound_manager.sfx_volume:
                self.sound_manager.set_sfx_volume(new_sfx_vol)

        for event in events:
            if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                self.settings_show = not self.settings_show

            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                if self.settings_btn.signal(event.pos):
                    self.settings_show = not self.settings_show

                if self.settings_show:
                    # Кнопка музыки
                    if self.music_btn.signal(event.pos):
                        enabled = self.sound_manager.toggle_music()
                        self.music_btn.image = self.music_on_scaled if enabled else self.music_off_scaled
                        self.music_btn.rect = self.music_btn.image.get_rect(topleft=(400, 280))

                    if self.sfx_btn.signal(event.pos):
                        enabled = self.sound_manager.toggle_sfx()
                        self.sfx_btn.image = self.sfx_on_scaled if enabled else self.sfx_off_scaled
                        self.sfx_btn.rect = self.sfx_btn.image.get_rect(topleft=(400, 350))

        self.stations[self.current_station].events(events)

    def draw(self, screen):
        self.stations[self.current_station].draw(screen)
        self.settings_btn.draw(screen)
        if self.settings_show:
            self.settings_draw(screen)