class Station:
    """ Базовый класс """
    def __init__(self, name, bg_color, button_color):
        self.name = name
        self.bg_color = bg_color
        self.button_color = button_color
        self.is_active = False

    def draw(self, screen):
        pass

    def events(self, events):
        pass

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False