import pygame

class TalentsState:
    def __init__(self, game):
        self.game = game
        self.font = None

    def on_enter(self):
        print("Вход в экран Таланты")   # меняй текст
        self.font = pygame.font.Font(None, 36)

    def on_exit(self):
        print("Выход из экрана Таланты")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                    self.game.change_state("character")

    def draw(self, screen):
        screen.fill((40, 40, 60))
        text = self.font.render("Экран Таланты (заглушка)", True, (255,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))