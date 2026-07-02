import pygame
import json
import os

class DialogState:
    def __init__(self, game):
        self.game = game
        self.font = None  # шрифт для текста
        self.name_font = None  # шрифт для имени говорящего
        self.dialog_lines = []  # список реплик (каждая реплика = dict с ключами speaker, text)
        self.current_line = 0  # индекс текущей реплики
        self.scene = None  # имя сцены (будет передано перед входом)
        self.chapter_files = [
            "Tom_1/Season_1/Preface.json",
            "Tom_1/Season_1/Chapter_1.json",
            "Tom_1/Season_1/Chapter_2.json",
            "Tom_1/Season_1/Chapter_3.json",
            "Tom_1/Season_1/Chapter_4.json"
        ]
        self.current_chapter_index = 0

    def load_scene(self, filename="Tom_1/Season_1/Preface"):
        full_path = os.path.join("assets/data/dialogues", filename)
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Если data — список, то это массив реплик
        if isinstance(data, list):
            self.dialog_lines = data
        else:
            # Если data — словарь, нужно извлечь первую сцену или использовать переданный ключ
            print(f"Ошибка: файл {full_path} не является массивом реплик")
            self.dialog_lines = []
        self.current_line = 0
        print(f"Загружена глава {filename}, реплик: {len(self.dialog_lines)}")

    def on_enter(self):
        print("Вход в диалог")
        self.dialog_window = pygame.image.load("assets/textures/Dialog_box.png")
        if hasattr(self.game, "temp_scene"):
            filename = self.game.temp_scene
        else:
            filename = self.chapter_files[self.current_chapter_index]

        self.load_scene(filename)

        # Создаём шрифты (один раз, можно вынести в __init__)
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
        print("Выход из диалога")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Если есть следующая реплика
                    if self.current_line + 1 < len(self.dialog_lines):
                        self.current_line += 1
                    else:
                        # Диалог закончен – возврат в мир
                        if self.current_chapter_index + 1 < len(self.chapter_files):
                            self.current_chapter_index += 1
                            self.load_scene(self.chapter_files[self.current_chapter_index])
                        else:
                            self.game.change_state("world")
                elif event.key == pygame.K_ESCAPE:
                    # Прервать диалог
                    self.game.change_state("world")

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Уникальный цвет для каждого состояния
        dialog_rect = pygame.Rect(50, screen.get_height() - 150, screen.get_width() - 100, 120)
        screen.blit(self.dialog_window, dialog_rect)

        if not self.dialog_lines or self.current_line >= len(self.dialog_lines):
            return

        line = self.dialog_lines[self.current_line]
        speaker = line.get("speaker", "")
        text = line.get("text", "")

        # Имя говорящего
        name_surf = self.name_font.render(speaker, True, (255, 255, 100))
        screen.blit(name_surf, (dialog_rect.x + 30, dialog_rect.y + 10))

        # Текст
        lines = self.wrap_text(text, dialog_rect.width - 20)

        for i, line_text in enumerate(lines):
            line_surf = self.font.render(line_text, True, (255, 255, 255))
            screen.blit(line_surf, (dialog_rect.x + 10, dialog_rect.y + 50 + i * 30))