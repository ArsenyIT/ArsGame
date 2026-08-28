import pygame
from input_handler import InputHandler

class GachaState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        print("Вход в Баннера")

    def on_exit(self):
        print("Выход из Баннеров")

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_F3) or InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

    def draw(self, screen):
        screen.fill((80, 40, 80))  # Уникальный цвет для каждого состояния
        font = pygame.font.Font(None, 48)
        text = font.render("Баннер (заглушка)", True, (255,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))