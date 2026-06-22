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
        self.field_width = 344
        self.offset = 10
        self.btn_width = self.field_width - 2 * self.offset  # 324
        self.btn_height = 123
        self.level_up_rect = pygame.Rect(1105, 528, 1363 - 1105, 590 - 528)

    def on_enter(self):
        # Загрузить актуальных персонажей из game.player.party
        if not self.characters:
            self.characters = [self.create_test_character()]
        print("CharacterState: on_enter")
        self.GG_menu = pygame.image.load("assets/textures/Арсений.png")
        self.button_images = {}
        button_names = ["Характеристика", "Оружие", "Артефакты", "Таланты", "Созвездия"]
        for name in button_names:
            filename = f"assets/textures/buttons/Кнопка_{name}.png"
            try:
                img = pygame.image.load(filename).convert_alpha()
                # Масштабируем под размер кнопки (btn_width, btn_height)
                img = pygame.transform.scale(img, (self.btn_width, self.btn_height))
                self.button_images[name] = img
            except pygame.error:
                print(f"Не удалось загрузить картинку для кнопки {name}, используется заглушка")
                # Можно создать цветной прямоугольник как запасной вариант
                surf = pygame.Surface((self.btn_width, self.btn_height))
                surf.fill((80, 80, 120))
                self.button_images[name] = surf
        filename = "assets/textures/buttons/Кнопка_Улучшение.png"
        try:
            img = pygame.image.load(filename).convert_alpha()
            img = pygame.transform.scale(img, (self.level_up_rect.width, self.level_up_rect.height))
            self.button_images["Повышение уровня"] = img
        except pygame.error:
            print("Не удалось загрузить картинку для кнопки Повышение уровня, используется заглушка")
            surf = pygame.Surface((self.level_up_rect.width, self.level_up_rect.height))
            surf.fill((80, 80, 120))
            self.button_images["Повышение уровня"] = surf

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
                    self.game.change_state("level_up")
                for btn in self.menu_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        if btn["text"] == "Характеристика":
                            pass
                        elif btn["text"] == "Оружие":
                            self.game.change_state("weapon")
                        elif btn["text"] == "Артефакты":
                            self.game.change_state("artifact")
                        elif btn["text"] == "Таланты":
                            self.game.change_state("talents")
                        elif btn["text"] == "Созвездия":
                            self.game.change_state("constellations")
                        break

    def draw(self, screen):
        screen.blit(self.GG_menu, (0,0))
        char = self.characters[self.current_index]

        # Имя и уровень
        name_text = self.title_font.render(f"{char['name']}  Lv.{char['level']}", True, (255,255,200))
        screen.blit(name_text, (1150, 50))

        # Полоска опыта
        #exp_ratio = char['exp'] / char['exp_next'] if char['exp_next'] > 0 else 0
        #pygame.draw.rect(screen, (80,80,80), (50, 70, 300, 15))
        #pygame.draw.rect(screen, (100,200,100), (50, 70, int(300 * exp_ratio), 15))
        #exp_text = self.font.render(f"Опыт: {char['exp']}/{char['exp_next']}", True, (200,200,200))
        #screen.blit(exp_text, (50, 90))

        x0 = 1102
        y0 = 92
        x_left = x0 + self.offset
        y_start = y0 + self.offset
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
            text = self.font.render(f"{name}: {val}", True, (255, 255, 255))
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
        y0_btn = 30
        field_height = 785 - 162  # 623
        btn_texts = ["Характеристика", "Оружие", "Артефакты", "Таланты", "Созвездия"]

        # Очищаем список кнопок перед перерисовкой
        self.menu_buttons = []

        for i, text in enumerate(btn_texts):
            y = y0_btn + self.offset + i * (self.btn_height + self.offset)
            rect = pygame.Rect(x0_btn + self.offset, y, self.btn_width, self.btn_height)
            # Рисуем картинку кнопки
            screen.blit(self.button_images[text], rect)
            # Сохраняем для обработки кликов
            self.menu_buttons.append({"text": text, "rect": rect})

        screen.blit(self.button_images["Повышение уровня"], self.level_up_rect)