import pygame

class MapState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        print("Вход в карты")

    def on_exit(self):
        print("Выход из карт")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Возврат в мир по той же клавише или ESC
                if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")

    def draw(self, screen):
        screen.fill((20, 60, 20))  # Уникальный цвет для каждого состояния
        font = pygame.font.Font(None, 48)
        text = font.render("Карта (заглушка)", True, (255,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))