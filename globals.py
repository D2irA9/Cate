#globals.py
import pygame as py, os

py.init()

WIDTH, HEIGHT = 1200, 720
screen = py.display.set_mode((1200, 720))

id_player = None
name_player = None

def load_sounds_from_folder(folder):
    sounds = []
    if not os.path.exists(folder):
        print(f"Папка {folder} не найдена!")
        return sounds
    for filename in os.listdir(folder):
        if filename.lower().endswith((".wav", ".ogg", ".mp3")):
            path = os.path.join(folder, filename)
            try:
                sound = py.mixer.Sound(path)
                sounds.append(sound)
                print(f"Загружен звук: {filename}")
            except Exception as e:
                print(f"Ошибка загрузки {filename}: {e}")
    return sounds