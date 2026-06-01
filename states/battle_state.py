import pygame

class BattleState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        print("Вход в бой")
        # Здесь позже будет инициализация боя: участники, порядок ходов, интерфейс

    def on_exit(self):
        print("Выход из боя")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Временно: выход из боя по ESC (потом заменим на условия победы/поражения)
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")

    def draw(self, screen):
        screen.fill((30, 30, 30))  # тёмный фон для боя
        font = pygame.font.Font(None, 48)
        text = font.render("БОЙ (заглушка)", True, (255, 0, 0))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))