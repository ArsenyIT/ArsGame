import pygame
from inventory import ITEM_DATA

class LevelUpState:
    def __init__(self, game):
        self.game = game
        self.font = None

    def on_enter(self):
        print("Вход в экран Улучшение")
        self.font = pygame.font.Font(None, 36)
        self.background = pygame.image.load("assets/textures/Арсений_Улучшение.png").convert_alpha()
        self.button_img = pygame.image.load("assets/textures/buttons/Кнопка_Улучшить.png").convert_alpha()
        self.use_button_rect = pygame.Rect(900, 630, 258, 62)

    def on_exit(self):
        print("Выход из экрана Улучшение")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                    self.game.change_state("character")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game.player.party:
                    char = self.game.player.party[0]
                    book_id = "story_of_the_Almighty"
                    if self.game.player.inventory.get_count(book_id) > 0:
                        exp_gain = ITEM_DATA[book_id].get("exp_gain", 0)
                        self.game.player.inventory.remove_item(book_id, 1)
                        char.add_exp(exp_gain)
                        print(f"Добавлено {exp_gain} опыта. Уровень: {char.level}")
                    else:
                        print("Нет книг!")

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.button_img, (900, 630))

        if self.game.player.party:
            char = self.game.player.party[0]
            books = self.game.player.inventory.get_count("story_of_the_Almighty")
            # Отображение уровня
            level_text = self.font.render(f"Уровень: {char.level}", True, (255, 255, 255))
            screen.blit(level_text, (100, 100))
            # Отображение опыта
            exp_text = self.font.render(f"Опыт: {char.exp}/{char.exp_next}", True, (255, 255, 255))
            screen.blit(exp_text, (100, 150))
            # Отображение количества книг
            books_text = self.font.render(f"Книг: {books}", True, (255, 255, 255))
            screen.blit(books_text, (100, 200))
