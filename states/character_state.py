import pygame

class CharacterState:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 36)
        # Список персонажей (позже будет браться из game.player.party)
        self.characters = []
        self.current_index = 0
        self.level_up_rect = pygame.Rect(50, 500, 200, 40)

    def on_enter(self):
        # Загрузить актуальных персонажей из game.player.party
        if not self.characters:
            self.characters = [self.create_test_character()]
        print("CharacterState: on_enter")
        self.GG_menu = pygame.image.load("assets/textures/Арсений.png")

    def create_test_character(self):
        # Возвращает словарь с данными персонажа
        return {
            "name": "Герой",
            "level": 1,
            "exp": 0,
            "exp_next": 100,
            "hp": 670,
            "max_hp": 670,
            "atk": 105,
            "defense": 300,
            "crit_rate": 5,
            "crit_dmg": 150,
            "energy_recharge": 100,
            "elemental_mastery": 10,
            "phys_bonus": 0,
            "resistance": 1,
            "talents": {"normal": 1, "skill": 1, "burst": 1},
            "constellation": 0,
        }

    def on_exit(self):
        print("CharacterState: on_exit")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Возврат в мир
                if event.key == pygame.K_c or event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")
                # Переключение персонажей
                if event.key == pygame.K_q:
                    self.current_index = (self.current_index - 1) % len(self.characters)
                if event.key == pygame.K_e:
                    self.current_index = (self.current_index + 1) % len(self.characters)
                # Заглушки для кнопок
                if event.key == pygame.K_a:
                    print("Возвышение (заглушка)")
                if event.key == pygame.K_t:
                    print("Улучшить таланты (заглушка)")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.level_up_rect.collidepoint(event.pos):
                    print("Повышение уровня")
                    #self.draw_up(screen)

    def draw(self, screen):
        screen.blit(self.GG_menu, (0,0))
        char = self.characters[self.current_index]

        # Имя и уровень
        name_text = self.title_font.render(f"{char['name']}  Lv.{char['level']}", True, (255,255,200))
        screen.blit(name_text, (50, 30))

        # Полоска опыта
        #exp_ratio = char['exp'] / char['exp_next'] if char['exp_next'] > 0 else 0
        #pygame.draw.rect(screen, (80,80,80), (50, 70, 300, 15))
        #pygame.draw.rect(screen, (100,200,100), (50, 70, int(300 * exp_ratio), 15))
        #exp_text = self.font.render(f"Опыт: {char['exp']}/{char['exp_next']}", True, (200,200,200))
        #screen.blit(exp_text, (50, 90))

        # Статы (левый и правый столбцы)
        stats_left = [
            ("HP", f"{char['hp']}/{char['max_hp']}"),
            ("Сила атаки", str(char['atk'])),
            ("Защита", str(char['defense'])),
            ("Шанс крита", f"{char['crit_rate']}%"),
            ("Крит. урон", f"{char['crit_dmg']}%"),
        ]
        stats_right = [
            ("Восст. энергии", f"{char['energy_recharge']}%"),
            ("Мастерство стихий", str(char['elemental_mastery'])),
            ("Бонус физ. урона", f"{char['phys_bonus']}%"),
            ("Сопротивление", f"{char['resistance']}%"),
        ]

        y_start = 140
        x_left = 50
        x_right = 350
        line_height = 30

        for i, (name, val) in enumerate(stats_left):
            text = self.font.render(f"{name}: {val}", True, (220,220,220))
            screen.blit(text, (x_left, y_start + i*line_height))

        for i, (name, val) in enumerate(stats_right):
            text = self.font.render(f"{name}: {val}", True, (220,220,220))
            screen.blit(text, (x_right, y_start + i*line_height))

        # Таланты
        talent_y = y_start + len(stats_left)*line_height + 20
        title = self.font.render("Таланты:", True, (255,200,100))
        screen.blit(title, (x_left, talent_y))
        talents = [
            ("Обычная атака", char['talents']['normal']),
            ("Навык (E)", char['talents']['skill']),
            ("Сверхспособность (Q)", char['talents']['burst']),
        ]
        for i, (name, lvl) in enumerate(talents):
            t = self.font.render(f"{name}: ур. {lvl}", True, (200,200,200))
            screen.blit(t, (x_left, talent_y + 25 + i*25))

        # Созвездия
        const_text = self.font.render(f"Созвездия: {char['constellation']}/6", True, (200,200,200))
        screen.blit(const_text, (x_right, talent_y))

        # Кнопки-заглушки
        btn_y = screen.get_height() - 100
        screen.blit(self.font.render("A - Возвышение", True, (150,150,200)), (50, btn_y+30))
        screen.blit(self.font.render("T - Улучшить таланты", True, (150,150,200)), (50, btn_y+60))

        pygame.draw.rect(screen, (70, 70, 120), self.level_up_rect)
        text = self.font.render("Повышение уровня", True, (255, 255, 255))
        screen.blit(text, (self.level_up_rect.x + 10, self.level_up_rect.y + 10))

    #def draw_up(self, screen):
    #    screen.fill((200, 200, 240))
