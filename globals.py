import pygame as py, os
from classes.db import DB

db = DB()
py.init()

WIDTH, HEIGHT = 1200, 720
screen = py.display.set_mode((1200, 720))

id_player = None
name_player = None

version = "0.1"