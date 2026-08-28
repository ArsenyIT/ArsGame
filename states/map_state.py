import pygame
from input_handler import InputHandler

class MapState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        self.map = self.game.resources.get_image("map_1")

    def on_exit(self):
        print("Выход из карт")

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_m) or InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

    def draw(self, screen):
        screen.blit(self.map, (0,0))