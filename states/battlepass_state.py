import pygame
from input_handler import InputHandler

class BattlepassState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        print("Вход в боевой пропуск")

    def on_exit(self):
        print("Выход из боевого пропуска")

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_F2) or InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

    def draw(self, screen):
        screen.fill((50, 100, 50))  # Уникальный цвет для каждого состояния
        font = pygame.font.Font(None, 48)
        text = font.render("Боевой пропуск (заглушка)", True, (255,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))