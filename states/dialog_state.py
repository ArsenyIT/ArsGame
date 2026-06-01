import pygame

class DialogState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        print("Вход в диалог")

    def on_exit(self):
        print("Выход из диалога")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Возврат в мир по той же клавише или ESC
                if event.key == pygame.K_f or event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Уникальный цвет для каждого состояния
        font = pygame.font.Font(None, 48)
        text = font.render("Диалог (заглушка)", True, (255,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))