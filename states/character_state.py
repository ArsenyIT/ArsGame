import pygame

class CharacterState:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 36)
        # Список персонажей (позже будет браться из game.player.party)
        self.characters = []
        self.current_index = 0
        self.menu_buttons = []

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
            "speed": 10,
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

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.level_up_rect.collidepoint(event.pos):
                    print("Повышение уровня")

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

        x0 = 1102
        y0 = 92
        offset = 10
        x_left = x0 + offset
        y_start = y0 + offset
        line_height = 30

        # Общий список всех характеристик (в один столбик)
        stats_all = [
            ("HP", f"{char['hp']}/{char['max_hp']}"),
            ("Сила атаки", str(char['atk'])),
            ("Защита", str(char['defense'])),
            ("Шанс крита", f"{char['crit_rate']}%"),
            ("Крит. урон", f"{char['crit_dmg']}%"),
            ("Восст. энергии", f"{char['energy_recharge']}%"),
            ("Мастерство стихий", str(char['elemental_mastery'])),
            ("Бонус физ. урона", f"{char['phys_bonus']}%"),
            ("Сопротивление", f"{char['resistance']}%"),
            ("Скорость", str(char['speed'])),
        ]

        for i, (name, val) in enumerate(stats_all):
            text = self.font.render(f"{name}: {val}", True, (220, 220, 220))
            screen.blit(text, (x_left, y_start + i * line_height))

        # Таланты
        #talent_y = y_start + len(stats_left)*line_height + 20
        #title = self.font.render("Таланты:", True, (255,200,100))
        #screen.blit(title, (x_left, talent_y))
        #talents = [
        #    ("Обычная атака", char['talents']['normal']),
        #    ("Навык (E)", char['talents']['skill']),
        #    ("Сверхспособность (Q)", char['talents']['burst']),
        #]
        #for i, (name, lvl) in enumerate(talents):
        #    t = self.font.render(f"{name}: ур. {lvl}", True, (200,200,200))
        #    screen.blit(t, (x_left, talent_y + 25 + i*25))

        # ---- Кнопки перехода (заглушки) ----
        # Параметры поля кнопок (левая колонка)
        x0_btn = 0
        y0_btn = 162
        field_width = 344  # ширина поля (0 до 344)
        field_height = 785 - 162  # 623
        offset = 10
        btn_width = field_width - 2 * offset  # 324
        btn_height = 123  # подобрано для 4 кнопок
        btn_texts = ["Оружие", "Артефакты", "Таланты", "Созвездия"]

        # Очищаем список кнопок перед перерисовкой
        self.menu_buttons = []

        for i, text in enumerate(btn_texts):
            y = y0_btn + offset + i * (btn_height + offset)
            rect = pygame.Rect(x0_btn + offset, y, btn_width, btn_height)
            # Рисуем фон кнопки
            pygame.draw.rect(screen, (60, 60, 80), rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 2)  # рамка
            # Текст по центру
            text_surf = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
            # Сохраняем для обработки кликов
            self.menu_buttons.append({"text": text, "rect": rect})

        x0_lvl = 1105
        y0_lvl = 528
        width_lvl = 1363 - 1105
        height_lvl = 590 - 528
        # Создаём прямоугольник кнопки (можно с отступом 5, но я сделаю точно по границам поля)
        self.level_up_rect = pygame.Rect(x0_lvl, y0_lvl, width_lvl, height_lvl)
        # Рисуем фон кнопки
        pygame.draw.rect(screen, (60, 60, 80), self.level_up_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.level_up_rect, 2)  # рамка
        # Текст с отступом 10 от левого края и по вертикали по центру
        text_surf = self.font.render("Повышение уровня", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.level_up_rect.center)
        screen.blit(text_surf, text_rect)