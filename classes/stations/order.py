from colors import *
from globals import *
from .base import Station
from ..tiled import Map
from ..character import Character
from ..db import db
from ..node import ImageButton, font
import os, random

class OrderStation(Station):
    def __init__(self):
        super().__init__("Заказы", BLACK, GREEN)
        self.map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
        self.map_loaded = False

        # Персонажи
        self.player = Character(3, (530, 60), 'assets/sprites/characters/player/Adam.png', [(530, 60)])
        self.split_player = 2

        # Nps
        self.nps = None
        self._load_random_npc()
        self.split_nps = 4

        self.interact_btn = ImageButton("assets/sprites/characters/nps/interactive/place_order.png", (545, 90), 3)
        self.interact_btn_show = False

    def _load_random_npc(self):
        """Загружает случайного NPC"""
        nps_folder = "assets/sprites/characters/nps"
        png_files = [f for f in os.listdir(nps_folder) if f.lower().endswith('.png')]

        chosen_file = random.choice(png_files)
        name = os.path.splitext(chosen_file)[0]
        sprite_path = os.path.join(nps_folder, chosen_file)

        path = [(240, 140), (530, 140), (530, 120)]

        self.npc = Character(3, (240, 0), sprite_path, path)

    def draw(self, screen):
        if not self.map_loaded:
            self.map.load_map()
            self.map_loaded = True
            # по имени слоя
            # if 'walls' in self.map.layer_names:
            #     self.split_index = self.map.layer_names.index('walls') + 1

        # Рисуем нижние слои
        for i in range(self.split_player):
            self.map.draw_layer(screen, i)

        # Рисуем игрока
        self.player.update()
        self.player.draw(screen)

        for i in range(self.split_player, self.split_nps):
            self.map.draw_layer(screen, i)

        self.npc.update()
        self.npc.draw(screen)

        # Отображение кнопки
        if self.npc.is_path_finished():
            self.interact_btn_show = True

        if self.interact_btn_show:
            self.interact_btn.draw(screen)

        # Рисуем верхние слои
        for i in range(self.split_nps, len(self.map.layers)):
            self.map.draw_layer(screen, i)

    def events(self, events):
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                if self.interact_btn.signal(event.pos):
                    self.interact_btn_show = False
                    print(f"Нажата кнопка заказа для NPC")