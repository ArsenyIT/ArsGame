import pygame
from inventory import ITEM_DATA

class LevelUpState:
    def __init__(self, game):
        self.game = game
        self.font = None

    def on_enter(self):
        print("Вход в экран Улучшение")
        self.font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 28)
        self.background = pygame.image.load("assets/textures/Арсений_Улучшение.png").convert_alpha()
        self.button_img = pygame.image.load("assets/textures/buttons/Кнопка_Улучшить.png").convert_alpha()
        self.ascend_img = pygame.image.load("assets/textures/buttons/Кнопка_Возвысить.png").convert_alpha()
        self.use_button_rect = pygame.Rect(900, 630, 258, 62)
        self.portrait_GG = pygame.image.load("assets/textures/ГГ_меню.png")

    def on_exit(self):
        print("Выход из экрана Улучшение")
        self.game.save_all()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                    self.game.change_state("character")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.use_button_rect.collidepoint(event.pos):
                    if self.game.player.party:
                        char = self.game.player.party[0]
                        if char.can_ascend():
                            # Логика возвышения
                            shard_id = "oak_wood"
                            if self.game.player.inventory.get_count(shard_id) > 0:
                                self.game.player.inventory.remove_item(shard_id, 1)
                                char.ascend()
                                self.game.player.mark_modified()
                                print("Возвышение выполнено!")
                            else:
                                print("Нет материалов возвышения!")
                        else:
                            # Логика прокачки (книга опыта)
                            book_id = "story_of_the_Almighty"
                            if self.game.player.inventory.get_count(book_id) > 0:
                                exp_gain = ITEM_DATA[book_id].get("exp_gain", 0)
                                self.game.player.inventory.remove_item(book_id, 1)
                                char.add_exp(exp_gain)
                                self.game.player.mark_modified()
                                print(f"Добавлено {exp_gain} опыта. Уровень: {char.level}")
                            else:
                                print("Нет книг!")

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.portrait_GG, (180, 180))
        char = self.game.player.party[0]
        if char.can_ascend():
            screen.blit(self.ascend_img, (900, 630))
        else:
            screen.blit(self.button_img, (900, 630))

        if self.game.player.party:
            char = self.game.player.party[0]
            books = self.game.player.inventory.get_count("story_of_the_Almighty")
            # Отображение уровня
            level_text = self.font.render(f"Уровень: {char.level}", True, (255, 255, 255))
            screen.blit(level_text, (1150, 50))
            # Отображение количества книг
            books_text = self.font.render(f"Книг: {books}", True, (255, 255, 255))
            screen.blit(books_text, (1150, 125))

            exp_ratio = char.exp / char.exp_next if char.exp_next > 0 else 0
            pygame.draw.rect(screen, (80, 80, 80), (1150, 80, 200, 15))
            pygame.draw.rect(screen, (100, 200, 100), (1150, 80, int(200 * exp_ratio), 15))
            exp_text = self.font.render(f"Опыт: {char.exp}/{char.exp_next}", True, (200, 200, 200))
            screen.blit(exp_text, (1150, 100))

        # ---- Отображение статов персонажа ----
        x0 = 670
        y0 = 10
        offset = 10
        x_left = x0 + offset  # если у тебя есть self.offset, иначе задай явно
        y_start = y0 + offset
        line_height = 30

        stats_all = [
            ("HP", f"{char.base_hp}/{char.base_hp}"),
            ("Сила атаки", str(char.base_atk)),
            ("Защита", str(char.base_defense)),
            ("Шанс крита", f"{char.crit_rate}%"),
            ("Крит. урон", f"{char.crit_dmg}%"),
            ("Восст. энергии", f"{char.energy_recharge}%"),
            ("Мастерство стихий", str(char.elemental_mastery)),
            ("Бонус физ. урона", f"{char.phys_bonus}%"),
            ("Сопротивление", f"{char.resistance}%"),
            ("Скорость", str(char.speed)),
        ]

        for i, (name, val) in enumerate(stats_all):
            text = self.stats_font.render(f"{name}: {val}", True, (255, 255, 255))
            screen.blit(text, (x_left, y_start + i * line_height))
