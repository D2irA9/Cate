from classes.db import db
from colors import *
from classes.node import font
from globals import *
import sys, os, random, json

def game(screen):
    py.display.set_caption("Катэ")
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                db.close()
                py.quit()
                sys.exit()

        screen.fill(BLACK)
        py.display.flip()
        clock.tick(fps)