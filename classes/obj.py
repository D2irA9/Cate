import random
import pygame as py
from colors import *
from globals import *
from db import db

class TableCoin():
    """Класс отображение монет"""
    def __init__(self, id_player):
        self.num_coin = db.get_coins_player(id_player)
        self.sprite_sheet = py.image.load("../assets/sprites/coins/coins.png").convert_alpha()


