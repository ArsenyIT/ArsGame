import pygame
from input_handler import InputHandler

class PartyState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        print("Вход в настройки отряда")

    def on_exit(self):
        print("Выход из настроек отряда")

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_t) or InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

    def draw(self, screen):
        screen.fill((70, 70, 30))
        font = pygame.font.Font(None, 48)
        text = font.render("Отряд (заглушка)", True, (255,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))