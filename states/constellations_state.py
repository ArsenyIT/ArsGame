import pygame

class ConstellationsState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.offset_y = self.game.HEIGHT * 0.013  # 10
        self.offset_x = self.game.WIDTH * 0.0073  # 10
        self.btn_width = int(self.game.WIDTH * 0.2372)  # 324
        self.btn_height = int(self.game.HEIGHT * 0.15625)  # 120
        self.circle_positions = {
            0: (1164, 117),  # координаты для 1-го созвездия
            1: (1260, 253),
            2: (1264, 397),
            3: (1264, 541),
            4: (1158, 669),
        }
        self.active_circle = None  # хранит индекс активного созвездия (0–4) или None

    def get_constellation_description(self, level):
        # Описание бонусов для каждого созвездия (индексы 0–4)
        descriptions = [
            "Атака +10%",
            "Защита +15%",
            "Скорость +10%",
            "Крит. урон +20%",
            "Энергия +15%",
        ]
        # Если уровень вне диапазона, возвращаем "Нет бонусов"
        if level < 0 or level >= len(descriptions):
            return "Нет бонусов"
        return descriptions[level]

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
        self.font = pygame.font.Font(None, 36)
        self.const_font = pygame.font.Font(None, 28)
        self.popup_bg = self.game.resources.get_image("popup")
        self.portrait_GG = self.game.resources.get_image("gg")
        self.bg = self.game.resources.get_image("gg_constellations")

        self.button_images = {}
        button_names = ["characteristic", "weapon", "artifacts", "talents", "constellations"]
        for name in button_names:
            filename = f"button_{name}"
            try:
                img = self.game.resources.get_image(filename)
                # Масштабируем под размер кнопки (btn_width, btn_height)
                img = pygame.transform.scale(img, (self.btn_width, self.btn_height))
                self.button_images[name] = img
            except pygame.error:
                # Можно создать цветной прямоугольник как запасной вариант
                surf = pygame.Surface((self.btn_width, self.btn_height))
                surf.fill((80, 80, 120))
                self.button_images[name] = surf
        self.nav_buttons = []
        button_names = ["characteristic", "weapon", "artifacts", "talents", "constellations"]
        x0_btn = 0
        y0_btn = self.game.HEIGHT * 0.052 #40

        for i, text in enumerate(button_names):
            y = y0_btn + self.offset_y + i * (self.btn_height + self.offset_y)
            rect = pygame.Rect(x0_btn + self.offset_x, y, self.btn_width, self.btn_height)
            self.nav_buttons.append({"text": text, "rect": rect})

        self.activate_btn = self.game.resources.get_image("button_activate")

    def on_exit(self):
        self.game.save_all()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.active_circle is not None:
                        self.active_circle = None
                    else:
                        self.game.change_state("world")
                elif event.key == pygame.K_c:
                    self.game.change_state("world")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Обработка клика по кнопке активации (если плашка открыта)
                if hasattr(self, 'activate_btn_rect') and self.activate_btn_rect.collidepoint(event.pos):
                    char = self.game.player.party[0]
                    if self.active_circle is not None:
                        i = self.active_circle
                        if char.constellation == i:  # только если это следующее по порядку
                            if char.constellation < 5:  # максимум 5
                                if self.game.player.inventory.get_count("hero_duplicate") > 0:
                                    self.game.player.inventory.remove_item("hero_duplicate", 1)
                                    char.activate_constellation()
                                    self.game.player.mark_modified()
                                    self.game.save_all()

                # Если плашка закрыта, проверяем клики по кругам и навигации
                if self.active_circle is None:
                    # Проверка кликов по кругам
                    for idx, pos in self.circle_positions.items():
                        mouse_x, mouse_y = event.pos
                        circle_x, circle_y = pos
                        radius = 62
                        if (mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2 <= radius ** 2:
                            self.active_circle = idx
                            break
                    # Проверка навигационных кнопок
                    for btn in self.nav_buttons:
                        if btn["rect"].collidepoint(event.pos):
                            text = btn["text"]
                            if text == "characteristic":
                                self.game.change_state("character")
                            elif text == "weapon":
                                self.game.change_state("weapon")
                            elif text == "artifacts":
                                self.game.change_state("artifact")
                            elif text == "talents":
                                self.game.change_state("talents")
                            elif text == "constellations":
                                pass
                            break

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.portrait_GG, (self.game.WIDTH * 0.41, self.game.HEIGHT * 0.234)) #560,180

        for btn in self.nav_buttons:
            screen.blit(self.button_images[btn["text"]], btn["rect"])

        # ---- Плашка ----
        if self.active_circle is not None:
            popup_rect = pygame.Rect(0, 0, self.game.WIDTH * 0.2928, self.game.HEIGHT) #400,768
            screen.blit(self.popup_bg, popup_rect)

            char = self.game.player.party[0]
            i = self.active_circle
            display_level = i + 1
            max_level = 5

            # ---- Заголовок ----
            title = self.font.render("Созвездия", True, (255, 255, 255))
            screen.blit(title, (popup_rect.x + self.game.WIDTH * 0.01464, popup_rect.y + self.game.HEIGHT * 0.026)) #20

            # ---- Статус (с переносом) ----
            if char.constellation > i:
                status_text = "Активировано"
                show_button = False
            elif char.constellation == i:
                status_text = "Доступно для активации"
                show_button = True
            else:
                status_text = "Заблокировано (требуется предыдущее)"
                show_button = False

            status_full = f"Созвездие {display_level}: {status_text}"
            status_lines = self.wrap_text(status_full, self.const_font, popup_rect.width - self.game.WIDTH * 0.0293) #40
            y = popup_rect.y + self.game.HEIGHT * 0.0911 #70
            for line in status_lines:
                line_surf = self.const_font.render(line, True, (255, 255, 200))
                screen.blit(line_surf, (popup_rect.x + self.game.WIDTH * 0.01464, y)) #20
                y += self.game.HEIGHT * 0.03255 #25

            # ---- Описание бонуса ----
            description = self.get_constellation_description(i)
            desc_lines = self.wrap_text(description, self.const_font, popup_rect.width - self.game.WIDTH * 0.0293) #40
            y += self.game.HEIGHT * 0.013 #10
            for line in desc_lines:
                line_surf = self.const_font.render(line, True, (220, 220, 220))
                screen.blit(line_surf, (popup_rect.x + self.game.WIDTH * 0.01464, y)) #20
                y += self.game.HEIGHT * 0.03255 #25

            # ---- Кнопка активации или сообщение ----
            if show_button:
                btn_rect = pygame.Rect(popup_rect.x + self.game.WIDTH * 0.01464, y + self.game.HEIGHT * 0.039, self.game.WIDTH * 0.1464, self.game.HEIGHT * 0.065) #20,30,200,50
                screen.blit(self.activate_btn, btn_rect)
                self.activate_btn_rect = btn_rect
            elif char.constellation > i:
                max_text = self.font.render("Уже активировано", True, (255, 200, 100))
                screen.blit(max_text, (popup_rect.x + self.game.WIDTH * 0.01464, y + self.game.HEIGHT * 0.039)) #20,30
            else:
                locked_lines = self.wrap_text("Требуется активировать предыдущее", self.const_font, popup_rect.width - self.game.WIDTH * 0.0293) #40
                y_locked = y + self.game.HEIGHT * 0.039 #30
                for line in locked_lines:
                    line_surf = self.const_font.render(line, True, (200, 200, 200))
                    screen.blit(line_surf, (popup_rect.x + self.game.WIDTH * 0.01464, y_locked)) #20
                    y_locked += self.game.HEIGHT * 0.03255 #25