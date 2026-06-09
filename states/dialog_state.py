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
        self.scenes_order = ["scene_1", "scene_2", "scene_3", "scene_4", "scene_5", "scene_6"]
        self.current_scene_index = 0

    def load_scene(self, scene_name):
        with open("assets/data/dialogues/Tom_1/Season_1/Chapter_1.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.dialog_lines = data.get(scene_name, [])
        self.current_line = 0
        print(f"Загружена сцена {scene_name}, реплик: {len(self.dialog_lines)}")

    def on_enter(self):
        print("Вход в диалог")
        self.dialog_window = pygame.image.load("assets/textures/Диалоговое_окно.png")
        if hasattr(self.game, "temp_scene"):
            scene_name = self.game.temp_scene
            # Если нужно, найдём индекс этой сцены в scenes_order и установим current_scene_index
            # (необязательно, для последовательного переключения потом)
        else:
            scene_name = self.scenes_order[self.current_scene_index]

        self.load_scene(scene_name)

        # Создаём шрифты (один раз, можно вынести в __init__)
        self.font = pygame.font.Font(None, 28)
        self.name_font = pygame.font.Font(None, 32)

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
                        if self.current_scene_index + 1 < len(self.scenes_order):
                            self.current_scene_index += 1
                            self.load_scene(self.scenes_order[self.current_scene_index])
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
        screen.blit(name_surf, (dialog_rect.x + 10, dialog_rect.y + 10))

        # Текст (пока одной строкой)
        text_surf = self.font.render(text, True, (255, 255, 255))
        screen.blit(text_surf, (dialog_rect.x + 10, dialog_rect.y + 50))