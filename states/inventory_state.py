import pygame

class InventoryState:
    def __init__(self, game):
        self.game = game

    def on_enter(self):
        # Здесь можно загрузить данные инвентаря из глобального объекта
        print("Вход в инвентарь")

    def on_exit(self):
        print("Выход из инвентаря")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")

    def draw(self, screen):
        screen.fill((30, 30, 60))  # тёмно-синий фон
        # Пока просто текст
        font = pygame.font.Font(None, 36)
        text = font.render("Инвентарь (заглушка)", True, (255, 255, 255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2))