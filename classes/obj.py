import random
from globals import db, id_player

class TicketsOrder:
    def __init__(self):
        self.player_level = db.get_player_level(id_player) or 1
        self.cup_sizes = []
        self.espresso_types = []
        self.milk_types = []
        self.syrups = []
        self.milk_variants = []

        self._load_data()
        self.current_order = None
        self.show_order = False
        self.order_visible = False

    def _load_data(self):
        """Загружает данные, доступные на уровне игрока"""
        # Чашки
        db.cursor.execute("SELECT id, cup, capacity FROM cup_sizes")
        self.cup_sizes = db.cursor.fetchall()

        # Эспрессо
        db.cursor.execute("SELECT id, name FROM ingredients WHERE type='espresso' AND level <= %s", (self.player_level,))
        self.espresso_types = db.cursor.fetchall()

        # Молоко
        db.cursor.execute("SELECT id, name FROM ingredients WHERE type='milk' AND level <= %s", (self.player_level,))
        self.milk_types = db.cursor.fetchall()

        # Сиропы
        db.cursor.execute("SELECT id, name FROM ingredients WHERE type='syrup' AND level <= %s", (self.player_level,))
        self.syrups = db.cursor.fetchall()

        # Варианты молока (температура) – если таблица есть
        try:
            db.cursor.execute("SELECT id, name, temperature, symbol FROM milk_variants")
            self.milk_variants = db.cursor.fetchall()
        except:
            self.milk_variants = []

    def generate_random_order(self):
        """Генерирует случайный заказ из доступных ингредиентов"""
        if not self.cup_sizes:
            return None
        cup = random.choice(self.cup_sizes)
        capacity = cup['capacity']

        # Эспрессо: 1–3 порции, но не больше ёмкости
        max_espresso = min(3, capacity - 1)
        if max_espresso < 1:
            max_espresso = 1
        esp_qty = random.randint(1, max_espresso)

        # Молоко: оставшееся место, но не больше 4
        milk_qty = capacity - esp_qty
        if milk_qty > 4:
            milk_qty = random.randint(1, 4)
            esp_qty = capacity - milk_qty
            if esp_qty > 3:
                esp_qty = 3
                milk_qty = capacity - esp_qty

        # Выбор случайных ингредиентов
        espresso = random.choice(self.espresso_types) if self.espresso_types else None
        milk = random.choice(self.milk_types) if self.milk_types else None
        milk_variant = random.choice(self.milk_variants) if self.milk_variants else None
        syrup = random.choice(self.syrups) if self.syrups else None

        self.current_order = {
            'cup': cup,
            'espresso': {
                'id': espresso['id'] if espresso else None,
                'type': espresso['name'] if espresso else 'нет',
                'portions': esp_qty
            },
            'milk': {
                'id': milk['id'] if milk else None,
                'type': milk['name'] if milk else 'нет',
                'portions': milk_qty,
                'variant': milk_variant
            },
            'syrup': {
                'id': syrup['id'] if syrup else None,
                'name': syrup['name'] if syrup else None
            }
        }

        # Вывод в консоль
        print(f"Сгенерирован заказ: размер {cup['cup']}, емкость {capacity}")
        print(f"  Эспрессо: {esp_qty} порций, тип: {espresso['name'] if espresso else 'нет'}")
        print(f"  Молоко: {milk_qty} порций, тип: {milk['name'] if milk else 'нет'}, температура: {milk_variant['name'] if milk_variant else 'обычное'}")
        print(f"  Сироп: {syrup['name'] if syrup else 'нет'}")

        return self.current_order

    def draw_order(self, screen):
        """Пока не реализовано, просто заглушка"""
        pass

    def generate_new_order(self):
        self.current_order = self.generate_random_order()