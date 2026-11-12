import pygame
import json
import os
from input_handler import  InputHandler
from utils import resource_path

class DialogState:
    def __init__(self, game):
        self.game = game
        self.dialog_lines = []  # список реплик (каждая реплика = dict с ключами speaker, text)
        self.current_line = 0  # индекс текущей реплики
        self.chapter_files = [
            "Tom_1/Season_1/Preface.json",
            "Tom_1/Season_1/Chapter_1.json",
            #"Tom_1/Season_1/Chapter_2.json",
            #"Tom_1/Season_1/Chapter_3.json",
            #"Tom_1/Season_1/Chapter_4.json"
        ]
        self.current_chapter_index = 0
        self.set_flag = None

    def load_scene(self, filename="tom_1/season_1/preface"):
        full_path = os.path.join(resource_path("assets/data/dialogues"), filename)
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Если data — список, то это массив реплик
        if isinstance(data, list):
            self.dialog_lines = data
            self.get_flags(self.dialog_lines)
        else:
            # Если data — словарь, нужно извлечь первую сцену или использовать переданный ключ
            self.dialog_lines = []
        self.current_line = 0

    def get_flags(self, dialog_lines):
        flags = dialog_lines[self.current_line]
        self.set_flag = flags.get("set_flag")

    def on_enter(self):
        self.dialog_window = self.game.resources.get_image("dialog_box")

        # Выбираем filename
        if hasattr(self.game, "temp_scene"):
            filename = self.game.temp_scene
        else:
            filename = self.chapter_files[self.current_chapter_index]

        self.load_scene(filename)

        # Создаём шрифты
        self.font = pygame.font.Font(None, 28)
        self.name_font = pygame.font.Font(None, 32)

    def wrap_text(self, text, max_width):
        # Используем существующий self.font
        words = text.split(' ')  # разбиваем на слова
        lines = []  # список готовых строк
        current_line = ""  # текущая собираемая строка

        for word in words:
            # Проверяем, поместится ли слово в текущую строку
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                # Если не помещается, сохраняем текущую строку и начинаем новую
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "

        # Добавляем последнюю строку
        if current_line:
            lines.append(current_line.strip())

        return lines

    def on_exit(self):
        if hasattr(self.game, "temp_scene"):
            del self.game.temp_scene

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_SPACE) or InputHandler.is_key_pressed(events, pygame.K_RETURN):
            # Если есть следующая реплика
            if self.set_flag != None:
                self.game.change_state("world")
                self.set_flag = None
            elif self.current_line + 1 < len(self.dialog_lines):
                self.current_line += 1
                self.get_flags(self.dialog_lines)
            else:
                if self.current_chapter_index + 1 < len(self.chapter_files):
                    self.current_chapter_index += 1
                    self.load_scene(self.chapter_files[self.current_chapter_index])
                else:
                    self.game.change_state("world")
        if InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

    def draw(self, screen):
        screen.fill((0, 0, 0))
        dialog_rect = pygame.Rect(self.game.WIDTH * 0.0366, self.game.HEIGHT - self.game.HEIGHT * 0.26, self.game.WIDTH - self.game.WIDTH * 0.073, self.game.HEIGHT * 0.15625) #50,200,100,120
        screen.blit(self.dialog_window, dialog_rect)

        if not self.dialog_lines or self.current_line >= len(self.dialog_lines):
            return

        line = self.dialog_lines[self.current_line]
        speaker = line.get("speaker", "")
        text = line.get("text", "")

        # Имя говорящего
        name_surf = self.name_font.render(speaker, True, (255, 255, 150))
        screen.blit(name_surf, (dialog_rect.x + int(self.game.WIDTH * 0.022), dialog_rect.y + int(self.game.HEIGHT * 0.013))) #30,10

        # Текст
        lines = self.wrap_text(text, dialog_rect.width - self.game.WIDTH * 0.01464) #20

        for i, line_text in enumerate(lines):
            line_surf = self.font.render(line_text, True, (255, 255, 255))
            screen.blit(line_surf, (dialog_rect.x + self.game.WIDTH * 0.0073, dialog_rect.y + self.game.HEIGHT * 0.065 + i * int(self.game.HEIGHT * 0.039))) #10,50,30