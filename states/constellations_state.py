import pygame

class ConstellationsState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.field_width = 344
        self.offset = 10
        self.btn_width = self.field_width - 2 * self.offset  # 324
        self.btn_height = 120
        self.circle_positions = {
            0: (300, 200),  # координаты для 1-го созвездия
            1: (300, 300),
            2: (300, 400),
            3: (300, 500),
            4: (300, 600),
        }
        self.active_circle = None  # хранит индекс активного созвездия (0–5) или None

    def get_constellation_description(self, level):
        # Описание бонусов для каждого уровня (0–6)
        descriptions = [
            "Нет бонусов",
            "Атака +10%",
            "Защита +15%",
            "Скорость +10%",
            "Крит. урон +20%",
            "Энергия +15%",
            "Все статы +20%"
        ]
        return descriptions[min(level, 6)]

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    def on_enter(self):
        print("Вход в экран Созвездия")
        self.font = pygame.font.Font(None, 36)
        self.const_font = pygame.font.Font(None, 28)
        self.popup_bg = pygame.image.load("assets/textures/Плашка.png").convert_alpha()
        self.portrait_GG = pygame.image.load("assets/textures/ГГ_меню.png")
        self.bg = pygame.image.load("assets/textures/Арсений_Созвездия.png").convert_alpha()

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
        self.nav_buttons = []
        button_names = ["Характеристика", "Оружие", "Артефакты", "Таланты", "Созвездия"]
        x0_btn = 0
        y0_btn = 40
        offset = 10
        btn_width = 324
        btn_height = 120

        for i, text in enumerate(button_names):
            y = y0_btn + offset + i * (btn_height + offset)
            rect = pygame.Rect(x0_btn + offset, y, btn_width, btn_height)
            self.nav_buttons.append({"text": text, "rect": rect})

        self.activate_btn = pygame.image.load("assets/textures/buttons/Кнопка_Активировать.png").convert_alpha()

    def on_exit(self):
        print("Выход из экрана Созвездия")
        self.game.save_all()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.active_circle is not None:
                        self.active_circle = None
                    else:
                        pass

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Обработка клика по кнопке активации (если плашка открыта)
                if hasattr(self, 'activate_btn_rect') and self.activate_btn_rect.collidepoint(event.pos):
                    char = self.game.player.party[0]
                    if char.constellation < 6:
                        if self.game.player.inventory.get_count("hero_duplicate") > 0:
                            self.game.player.inventory.remove_item("hero_duplicate", 1)
                            char.activate_constellation()
                            self.game.save_all()
                            print("Созвездие активировано!")
                        else:
                            print("Нет дубликатов персонажа!")
                # Если плашка закрыта, проверяем клики по кругам и навигации
                if self.active_circle is None:
                    # Проверка кликов по кругам
                    for idx, pos in self.circle_positions.items():
                        mouse_x, mouse_y = event.pos
                        circle_x, circle_y = pos
                        radius = 30
                        if (mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2 <= radius ** 2:
                            self.active_circle = idx
                            print(f"Открыто созвездие {idx + 1}")
                            break
                    # Проверка навигационных кнопок
                    for btn in self.nav_buttons:
                        if btn["rect"].collidepoint(event.pos):
                            text = btn["text"]
                            if text == "Характеристика":
                                self.game.change_state("character")
                            elif text == "Оружие":
                                self.game.change_state("weapon")
                            elif text == "Артефакты":
                                self.game.change_state("artifact")
                            elif text == "Таланты":
                                self.game.change_state("talents")
                            elif text == "Созвездия":
                                pass
                            break

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.portrait_GG, (560, 180))

        for btn in self.nav_buttons:
            screen.blit(self.button_images[btn["text"]], btn["rect"])

        # ---- Плашка (как в талантах) ----
        if self.active_circle is not None:
            popup_rect = pygame.Rect(0, 0, 400, 768)
            screen.blit(self.popup_bg, popup_rect)

            char = self.game.player.party[0]
            level = char.constellation
            max_level = 5

            # Заголовок
            title = self.font.render("Созвездия", True, (255, 255, 255))
            screen.blit(title, (popup_rect.x + 20, popup_rect.y + 20))

            # Уровень
            level_text = self.font.render(f"Уровень: {level} / {max_level}", True, (255, 255, 200))
            screen.blit(level_text, (popup_rect.x + 20, popup_rect.y + 70))

            # Описание бонуса
            description = self.get_constellation_description(level)
            desc_lines = self.wrap_text(description, self.const_font, popup_rect.width - 40)
            y = popup_rect.y + 130
            for line in desc_lines:
                line_surf = self.const_font.render(line, True, (220, 220, 220))
                screen.blit(line_surf, (popup_rect.x + 20, y))
                y += 25

            # Кнопка активации (если уровень < 6)
            if level < max_level:
                # Здесь используй свою картинку кнопки, если она есть
                # Или временно прямоугольник с текстом
                btn_rect = pygame.Rect(popup_rect.x + 20, y + 30, 200, 50)
                screen.blit(self.activate_btn, btn_rect)
                self.activate_btn_rect = btn_rect
            else:
                max_text = self.font.render("Максимальный уровень достигнут", True, (255, 200, 100))
                screen.blit(max_text, (popup_rect.x + 20, y + 30))
