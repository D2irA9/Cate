from globals import *
from classes.stations import StationManager
from classes.db import db
import sys

def game(screen, events, station_manager):
    py.display.set_caption("Катэ")
    for event in events:
        if event.type == py.QUIT:
            db.close()
            py.quit()
            sys.exit()

    station_manager.handle_events(events)
    station_manager.draw(screen)