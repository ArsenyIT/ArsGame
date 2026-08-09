import pygame

class MapState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        print("Вход в карты")
        self.map = self.game.resources.get_image("map_1")

    def on_exit(self):
        print("Выход из карт")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Возврат в мир по той же клавише или ESC
                if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")

    def draw(self, screen):
        screen.blit(self.map, (0,0))