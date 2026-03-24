import pygame as py
from pytmx import load_pygame

class Tile(py.sprite.Sprite):
    """ Класс Плиток карты """
    def __init__(self, pos, surf, groups, scale, tile_size):
        super().__init__(groups)
        self.tile_size = tile_size
        self.image = py.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

class Map:
    """ Класс Карты """
    def __init__(self, tmx_path, tile_size, scale):
        self.tile_size = tile_size
        self.scale = scale
        self.tile_group = py.sprite.Group()
        self.object_group = py.sprite.Group()
        self.tmx_path = tmx_path

    def load_map(self):
        """ Загрузка карты """
        map = load_pygame(self.tmx_path)

        # Загрузка Тайлов
        for layer in map.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * self.tile_size * self.scale, y * self.tile_size * self.scale)
                    Tile(pos=pos, surf = surf, groups=self.tile_group, scale=self.scale, tile_size=self.tile_size)
        # Загрузка объектов
        for obj in map.objects:
            pos = (obj.x * self.scale, obj.y * self.scale)
            if obj.image:
                    Tile(pos=pos, surf = obj.image, groups=self.object_group, scale=self.scale, tile_size=self.tile_size)

    def draw(self, screen):
        """ Отрисовка всей карты """

        # Tайлы
        for tile in self.tile_group:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y))
        # Объекты
        for obj in self.object_group:
            screen.blit(obj.image, (obj.rect.x, obj.rect.y))