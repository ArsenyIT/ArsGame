import pygame
from input_handler import InputHandler

class QuestState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        print("Вход в квесты")

    def on_exit(self):
        print("Выход из квестов")

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_j) or InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

    def draw(self, screen):
        screen.fill((60, 40, 20))
        font = pygame.font.Font(None, 48)
        text = font.render("Квесты (заглушка)", True, (255,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))