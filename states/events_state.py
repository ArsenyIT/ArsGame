import pygame
from input_handler import InputHandler

class EventsState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        print("Вход в Ивенты")

    def on_exit(self):
        print("Выход из Ивентов")

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_F1) or InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

    def draw(self, screen):
        screen.fill((100, 50, 50))  # Уникальный цвет для каждого состояния
        font = pygame.font.Font(None, 48)
        text = font.render("Ивент (заглушка)", True, (255,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))