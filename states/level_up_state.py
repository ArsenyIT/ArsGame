import pygame
from inventory import ITEM_DATA
from input_handler import InputHandler

class LevelUpState:
    def __init__(self, game):
        self.game = game
        self.font = None

    def on_enter(self):
        self.font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 28)
        char_index = self.game.selected_character_index
        char = self.game.player.party[char_index]
        char_key = char.resource_key
        self.bg = self.game.resources.get_image(f"{char_key}_artifacts")
        if self.bg is None:
            self.bg = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
            self.bg.fill((40, 40, 60))

        try:
            self.portrait_img = pygame.image.load(char.portrait_path).convert_alpha()
        except (pygame.error, FileNotFoundError, AttributeError):
            self.portrait_img = pygame.Surface((290, 415))
            self.portrait_img.fill((150, 150, 200))
            print(f"Портрет для {char.name} не найден, создана заглушка")

        self.button_img = self.game.resources.get_image(f"button_improve_{char_key}")
        self.ascend_img = self.game.resources.get_image(f"button_elevate_{char_key}")
        self.use_button_rect = pygame.Rect(self.game.WIDTH * 0.66, self.game.HEIGHT * 0.82, self.game.WIDTH * 0.1889, self.game.HEIGHT * 0.0807) #900,630,258,62

    def on_exit(self):
        self.game.save_all()

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_c) or InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.use_button_rect.collidepoint(event.pos):
                    if self.game.player.party:
                        char = self.game.player.party[self.game.selected_character_index]
                        if char.can_ascend():
                            # Логика возвышения
                            shard_id = "oak_wood"
                            if self.game.player.inventory.get_count(shard_id) > 0:
                                self.game.player.inventory.remove_item(shard_id, 1)
                                char.ascend()
                                self.game.player.mark_modified()
                        else:
                            # Логика прокачки (книга опыта)
                            book_id = "story_of_the_Almighty"
                            if self.game.player.inventory.get_count(book_id) > 0:
                                exp_gain = ITEM_DATA[book_id].get("exp_gain", 0)
                                self.game.player.inventory.remove_item(book_id, 1)
                                char.add_exp(exp_gain)
                                self.game.player.mark_modified()

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.portrait_img, (self.game.WIDTH * 0.132, self.game.HEIGHT * 0.2344)) #180
        char = self.game.player.party[self.game.selected_character_index]
        if char.can_ascend():
            screen.blit(self.ascend_img, (self.game.WIDTH * 0.66, self.game.HEIGHT * 0.82)) #900,630
        else:
            screen.blit(self.button_img, (self.game.WIDTH * 0.66, self.game.HEIGHT * 0.82)) #900,630

        if self.game.player.party:
            char = self.game.player.party[self.game.selected_character_index]
            books = self.game.player.inventory.get_count("story_of_the_Almighty")
            # Отображение уровня
            level_text = self.font.render(f"Уровень: {char.level}", True, (255, 255, 255))
            screen.blit(level_text, (self.game.WIDTH * 0.842, self.game.HEIGHT * 0.065)) #1150,50
            # Отображение количества книг
            books_text = self.font.render(f"Книг: {books}", True, (255, 255, 255))
            screen.blit(books_text, (self.game.WIDTH * 0.842, self.game.HEIGHT * 0.1627)) #1150,125

            exp_ratio = char.exp / char.exp_next if char.exp_next > 0 else 0
            pygame.draw.rect(screen, (80, 80, 80), (self.game.WIDTH * 0.842, self.game.HEIGHT * 0.1042, self.game.WIDTH * 0.1464, self.game.HEIGHT * 0.0195)) #1150,80,200,15
            pygame.draw.rect(screen, (100, 200, 100), (self.game.WIDTH * 0.842, self.game.HEIGHT * 0.1042, int(self.game.WIDTH * 0.1464 * exp_ratio), self.game.HEIGHT * 0.0195)) #1150,80,200,15
            exp_text = self.font.render(f"Опыт: {char.exp}/{char.exp_next}", True, (200, 200, 200))
            screen.blit(exp_text, (self.game.WIDTH * 0.842, self.game.HEIGHT * 0.13)) #1150,100

        # ---- Отображение статов персонажа ----
        x0 = self.game.WIDTH * 0.49 #670
        y0 = self.game.HEIGHT * 0.013 #10
        offset_x = self.game.WIDTH * 0.0073 #10
        offset_y = self.game.HEIGHT * 0.013 #10
        x_left = x0 + offset_x
        y_start = y0 + offset_y
        line_height = self.game.HEIGHT * 0.039 #30

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
