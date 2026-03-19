import pygame as py, random, os, json

class SoundManager:
    def __init__(self):
        self.music_sounds = self._load_sounds("assets/sounds/music")
        self.sfx_sounds = self._load_sounds("assets/sounds/sound")

        # Текущие звуки
        self.current_music = None

        # Каналы: 0 – музыка, остальные для эффектов
        self.music_channel = py.mixer.Channel(0) if py.mixer.get_init() else None

        # Настройки
        self.music_volume = 1.0
        self.music_enabled = True
        self.sfx_volume = 1.0
        self.sfx_enabled = True

        self.load_settings()
        self._start_music()

    def _load_sounds(self, folder):
        """Загружает все звуки из указанной папки"""
        sounds = []
        if not os.path.exists(folder):
            print(f"Папка {folder} не найдена")
            return sounds
        for filename in os.listdir(folder):
            if filename.lower().endswith((".wav", ".ogg", ".mp3")):
                path = os.path.join(folder, filename)
                try:
                    sound = py.mixer.Sound(path)
                    sounds.append(sound)
                except Exception as e:
                    print(f"Ошибка загрузки {filename}: {e}")
        return sounds

    def _start_music(self):
        """Запускает случайный музыкальный трек"""
        if not self.music_sounds:
            return
        self.current_music = random.choice(self.music_sounds)
        self._play_music()

    def _play_music(self):
        """Проигрывает текущую музыку с учётом громкости"""
        if not self.current_music or not self.music_channel:
            return
        self.music_channel.play(self.current_music, loops=-1)  # зацикливаем
        self._apply_music_volume()

    def _apply_music_volume(self):
        """Устанавливает громкость музыкального канала"""
        if self.music_channel:
            vol = self.music_volume if self.music_enabled else 0.0
            self.music_channel.set_volume(vol)

    def _next_music(self):
        """Выбирает следующий трек, избегая повтора"""
        if len(self.music_sounds) > 1:
            others = [s for s in self.music_sounds if s != self.current_music]
            self.current_music = random.choice(others)
        else:
            self.current_music = self.music_sounds[1]
        self._play_music()

    def update(self):
        """Проверяет, не закончилась ли музыка, и запускает следующую"""
        if self.music_channel and not self.music_channel.get_busy():
            self._next_music()

    # Управление музыкой
    def set_music_volume(self, value):
        self.music_volume = max(0.0, min(1.0, value))
        self._apply_music_volume()
        self.save_settings()

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        self._apply_music_volume()
        self.save_settings()
        return self.music_enabled

    # Управление звуковыми эффектами
    def play_sfx(self):
        """Проигрывает случайный звуковой эффект"""
        if not self.sfx_sounds or not self.sfx_enabled:
            return
        sound = random.choice(self.sfx_sounds)
        sound.set_volume(self.sfx_volume)
        sound.play()

    def set_sfx_volume(self, value):
        self.sfx_volume = max(0.0, min(1.0, value))
        self.save_settings()

    def toggle_sfx(self):
        self.sfx_enabled = not self.sfx_enabled
        self.save_settings()
        return self.sfx_enabled

    # Сохранение/загрузка
    def save_settings(self):
        try:
            with open("settings.json", "w") as f:
                json.dump({
                    "music_volume": self.music_volume,
                    "music_enabled": self.music_enabled,
                    "sfx_volume": self.sfx_volume,
                    "sfx_enabled": self.sfx_enabled
                }, f)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    data = json.load(f)
                    self.music_volume = data.get("music_volume", 1.0)
                    self.music_enabled = data.get("music_enabled", True)
                    self.sfx_volume = data.get("sfx_volume", 1.0)
                    self.sfx_enabled = data.get("sfx_enabled", True)
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")