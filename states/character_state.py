import pygame
from game_data import Character

class CharacterState:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 36)
        # Список персонажей
        self.characters = []
        self.current_index = 0
        self.button_images = {}
        self.menu_buttons = []
        self.offset_y = self.game.HEIGHT * 0.013 #10
        self.offset_x = self.game.WIDTH * 0.0073 #10
        self.btn_width = int(self.game.WIDTH * 0.2372) #324
        self.btn_height = int(self.game.HEIGHT * 0.15625) #120
        self.level_up_rect = pygame.Rect(self.game.WIDTH * 0.8089, self.game.HEIGHT * 0.6875, self.game.WIDTH * 0.1889, self.game.HEIGHT * 0.0807) #1105,590,258,62

    def on_enter(self):
        # Загрузить актуальных персонажей из game.player.party
        self.characters = self.game.player.party
        if not self.characters:
            self.characters = [Character(
                name="Герой",
                exp=0,
                exp_next=100,
                base_hp=670,
                base_atk=105,
                base_defense=300,
                crit_rate=5,
                crit_dmg=150,
                energy_recharge=100,
                elemental_mastery=10,
                phys_bonus=0,
                resistance=1,
                speed=10,
                resource_key = "gg"
            )]
        self.update_ui()

    def on_exit(self):
        self.game.save_all()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Возврат в мир
                if event.key == pygame.K_c or event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")
                # Переключение персонажей
                if event.key == pygame.K_q:
                    self.current_index = (self.current_index - 1) % len(self.characters)
                    self.update_ui()
                if event.key == pygame.K_e:
                    self.current_index = (self.current_index + 1) % len(self.characters)
                    self.update_ui()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.level_up_rect.collidepoint(event.pos):
                    self.game.change_state("level_up")
                for btn in self.menu_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        if btn["text"] == "characteristic":
                            pass
                        elif btn["text"] == "weapon":
                            self.game.change_state("weapon")
                        elif btn["text"] == "artifacts":
                            self.game.change_state("artifact")
                        elif btn["text"] == "talents":
                            self.game.change_state("talents")
                        elif btn["text"] == "constellations":
                            self.game.change_state("constellations")
                        break

    def update_ui(self):
        char = self.characters[self.current_index]
        char_key = self.characters[self.current_index].resource_key

        self.menu = self.game.resources.get_image(f"{char_key}_menu")
        if self.menu is None:
            self.menu = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
            self.menu.fill((40, 40, 60))

        self.portrait = self.characters[self.current_index].portrait_path
        try:
            self.portrait_img = pygame.image.load(char.portrait_path).convert_alpha()
        except (pygame.error, FileNotFoundError, AttributeError):
            self.portrait_img = pygame.Surface((290, 415))
            self.portrait_img.fill((150, 150, 200))
            print(f"Портрет для {char.name} не найден, создана заглушка")

        button_names = ["characteristic", "weapon", "artifacts", "talents", "constellations"]
        for name in button_names:
            filename = f"button_{name}_{char_key}"
            img = self.game.resources.get_image(filename)
            if img is not None:
                img = pygame.transform.scale(img, (self.btn_width, self.btn_height))
                self.button_images[name] = img
            else:
                surf = pygame.Surface((self.btn_width, self.btn_height))
                surf.fill((80, 80, 120))
                self.button_images[name] = surf
                print(f"Кнопка {name} для {char_key} не найдена, создана заглушка")

        # Кнопка улучшения
        filename = f"button_improvement_{char_key}"
        img = self.game.resources.get_image(filename)
        if img is not None:
            img = pygame.transform.scale(img, (self.level_up_rect.width, self.level_up_rect.height))
            self.button_images["Улучшение"] = img
        else:
            surf = pygame.Surface((self.level_up_rect.width, self.level_up_rect.height))
            surf.fill((80, 80, 120))
            self.button_images["Улучшение"] = surf
            print(f"Кнопка улучшения для {char_key} не найдена")

        # Кнопка возвышения
        filename = f"button_elevation_{char_key}"
        img = self.game.resources.get_image(filename)
        if img is not None:
            img = pygame.transform.scale(img, (self.level_up_rect.width, self.level_up_rect.height))
            self.button_images["Возвышение"] = img
        else:
            surf = pygame.Surface((self.level_up_rect.width, self.level_up_rect.height))
            surf.fill((80, 80, 120))
            self.button_images["Возвышение"] = surf
            print(f"Кнопка возвышения для {char_key} не найдена")


    def draw(self, screen):
        if self.menu:
            screen.blit(self.menu, (0, 0))
        if self.portrait_img:
            screen.blit(self.portrait_img, (int(self.game.WIDTH * 0.41), int(self.game.HEIGHT * 0.234))) #560,180

        if not self.characters:
            return

        char = self.game.player.party[self.current_index]

        # Имя и уровень
        name_text = self.title_font.render(f"{char.name}  Lv.{char.level}", True, (255,255,200))
        screen.blit(name_text, (self.game.WIDTH * 0.8419, self.game.HEIGHT * 0.0651)) #1150,50

        x0 = self.game.WIDTH * 0.8067 #1102
        y0 = self.game.HEIGHT * 0.12 #92
        x_left = x0 + self.offset_x
        y_start = y0 + self.offset_y
        line_height = self.game.HEIGHT * 0.039 #30

        # Общий список всех характеристик (в один столбик)
        total_stats = char.calculate_total_stats()
        stats_all = [
            ("HP", f"{total_stats['hp']}/{char.base_hp}"),  # max_hp пока базовое
            ("Сила атаки", str(total_stats['atk'])),
            ("Защита", str(total_stats['def'])),
            ("Шанс крита", f"{total_stats['crit_rate']}%"),
            ("Крит. урон", f"{total_stats['crit_dmg']}%"),
            ("Восст. энергии", f"{total_stats['energy_recharge']}%"),
            ("Мастерство стихий", str(total_stats['elemental_mastery'])),
            ("Бонус физ. урона", f"{total_stats['phys_bonus']}%"),
            ("Сопротивление", f"{total_stats['resistance']}%"),
            ("Скорость", str(total_stats['speed'])),
        ]

        for i, (name, val) in enumerate(stats_all):
            text = self.font.render(f"{name}: {val}", True, (255, 255, 255))
            screen.blit(text, (x_left, y_start + i * line_height))

        # ---- Кнопки перехода ----
        # Параметры поля кнопок (левая колонка)
        x0_btn = 0
        y0_btn = self.game.HEIGHT * 0.052 #40
        btn_texts = ["characteristic", "weapon", "artifacts", "talents", "constellations"]

        # Очищаем список кнопок перед перерисовкой
        self.menu_buttons = []

        for i, text in enumerate(btn_texts):
            y = y0_btn + self.offset_y + i * (self.btn_height + self.offset_y)
            rect = pygame.Rect(x0_btn + self.offset_x, y, self.btn_width, self.btn_height)
            # Рисуем картинку кнопки
            screen.blit(self.button_images[text], rect)
            # Сохраняем для обработки кликов
            self.menu_buttons.append({"text": text, "rect": rect})

        if self.characters:
            if char.can_ascend():
                screen.blit(self.button_images["Возвышение"], self.level_up_rect)
            else:
                screen.blit(self.button_images["Улучшение"], self.level_up_rect)