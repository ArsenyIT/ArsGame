import pygame
from input_handler import InputHandler

class MapState:
    def __init__(self, game):
        self.game = game
        self.type_map = "World_1"

    def on_enter(self):
        self.type_map = self.game.type_map
        if self.type_map == "World_1":
            self.map = self.game.resources.get_image("map_1")
        elif self.type_map == "House":
            self.map = self.game.resources.get_image("gg_house_map_1")

    def on_exit(self):
        print("Выход из карт")

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_m) or InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

    def draw(self, screen):
        screen.blit(self.map, (0,0))