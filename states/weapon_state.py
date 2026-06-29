import pygame
from inventory import ITEM_DATA

class WeaponState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.stats_font = None
        self.selected_weapon = None          # уникальный ID выбранного оружия
        self.equipped_weapon = None          # уникальный ID экипированного оружия
        self.show_popup = False              # показывать ли плашку выбора
        self.popup_weapons = []              # список оружия в плашке
        self.popup_selected_index = -1
        self.popup_cell_rects = []
        # Параметры кнопок навигации (как в других состояниях)
        self.field_width = 344
        self.offset = 10
        self.btn_width = self.field_width - 2 * self.offset  # 324
        self.btn_height = 120

    def on_enter(self):
        self.font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 28)
        try:
            self.bg = pygame.image.load("assets/textures/Арсений_Оружие.png").convert_alpha()
        except:
            self.bg = None
        try:
            self.popup_bg = pygame.image.load("assets/textures/Плашка.png").convert_alpha()
        except:
            self.popup_bg = None

        # Кнопки "Экипировать/Сменить" и "Улучшить" (картинки)
        try:
            self.equip_btn_img = pygame.image.load("assets/textures/buttons/Кнопка_Экипировать.png").convert_alpha()
        except:
            self.equip_btn_img = None
        try:
            self.unequip_btn_img = pygame.image.load("assets/textures/buttons/Кнопка_Сменить.png").convert_alpha()
        except:
            self.unequip_btn_img = None
        try:
            self.upgrade_btn_img = pygame.image.load("assets/textures/buttons/Кнопка_Улучшить.png").convert_alpha()
        except:
            self.upgrade_btn_img = None

        # Загрузка иконок для оружия (если есть, иначе текст)
        self.weapon_icons = {}
        # Пример: если есть иконки для меча и лука
        self.weapon_icons["sword_2"] = pygame.image.load("assets/textures/Проржавевший_меч.png").convert_alpha()
        self.weapon_icons["sword_1"] = pygame.image.load("assets/textures/Меч_из_стали.png").convert_alpha()

        # Навигационные кнопки
        self.load_navigation_buttons()

        char = self.game.player.party[0]
        self.equipped_weapon = char.weapon
        self.update_popup_list()

    def load_navigation_buttons(self):
        # Кнопки навигации (левая панель)
        self.button_images = {}
        button_names = ["Характеристика", "Оружие", "Артефакты", "Таланты", "Созвездия"]
        for name in button_names:
            filename = f"assets/textures/buttons/Кнопка_{name}.png"
            try:
                img = pygame.image.load(filename).convert_alpha()
                img = pygame.transform.scale(img, (self.btn_width, self.btn_height))
                self.button_images[name] = img
            except pygame.error:
                surf = pygame.Surface((self.btn_width, self.btn_height))
                surf.fill((80, 80, 120))
                self.button_images[name] = surf
        self.nav_buttons = []
        x0_btn = 0
        y0_btn = 40
        offset = 10
        for i, text in enumerate(button_names):
            y = y0_btn + offset + i * (self.btn_height + offset)
            rect = pygame.Rect(x0_btn + offset, y, self.btn_width, self.btn_height)
            self.nav_buttons.append({"text": text, "rect": rect})

    def update_popup_list(self):
        # Список оружия из инвентаря для плашки
        self.popup_weapons = []
        for unique_id in self.game.player.weapon_inventory:
            char = self.game.player.party[0]
            data = char.weapon_data.get(unique_id, {})
            weapon_id = data.get("weapon_id")
            if weapon_id:
                self.popup_weapons.append(unique_id)
        self.popup_selected_index = -1

    def on_exit(self):
        self.game.save_all()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_popup:
                        self.show_popup = False
                    else:
                        self.game.change_state("character")
                elif event.key == pygame.K_c:
                    self.game.change_state("character")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.show_popup:
                    self.handle_popup_click(event.pos)
                else:
                    self.handle_main_click(event.pos)

    def handle_main_click(self, pos):
        # Проверка кликов по навигационным кнопкам
        for btn in self.nav_buttons:
            if btn["rect"].collidepoint(pos):
                text = btn["text"]
                if text == "Характеристика":
                    self.game.change_state("character")
                elif text == "Оружие":
                    pass  # уже здесь
                elif text == "Артефакты":
                    self.game.change_state("artifact")
                elif text == "Таланты":
                    self.game.change_state("talents")
                elif text == "Созвездия":
                    self.game.change_state("constellations")
                return

        # Кнопка "Экипировать/Сменить"
        if hasattr(self, 'equip_btn_rect') and self.equip_btn_rect.collidepoint(pos):
            char = self.game.player.party[0]
            if self.equipped_weapon is not None:
                # Снимаем
                char.unequip_weapon(self.game.player)
                self.game.player.mark_modified()
                self.equipped_weapon = None
                self.selected_weapon = None
                print("Оружие снято")
            else:
                # Если есть выбранное, экипируем
                if self.selected_weapon is not None:
                    char.equip_weapon(self.selected_weapon, self.game.player)
                    self.game.player.mark_modified()
                    self.equipped_weapon = self.selected_weapon
                    self.selected_weapon = None
                    print(f"Экипировано оружие {self.equipped_weapon}")
                else:
                    # Открываем плашку для выбора
                    self.show_popup = True
                    self.update_popup_list()

        # Кнопка "Улучшить"
        if hasattr(self, 'upgrade_btn_rect') and self.upgrade_btn_rect.collidepoint(pos):
            if self.equipped_weapon is not None:
                char = self.game.player.party[0]
                inventory = self.game.player.inventory
                # Вызов метода upgrade_weapon (пока заглушка)
                success = char.upgrade_weapon(self.equipped_weapon, inventory)
                if success:
                    self.game.player.mark_modified()
                    print("Оружие улучшено!")
                else:
                    print("Не удалось улучшить оружие")
            else:
                print("Нет экипированного оружия для улучшения!")

    def handle_popup_click(self, pos):
        # Клик по ячейке в плашке
        if hasattr(self, 'popup_cell_rects'):
            for idx, rect in enumerate(self.popup_cell_rects):
                if rect.collidepoint(pos):
                    if idx < len(self.popup_weapons):
                        self.selected_weapon = self.popup_weapons[idx]
                        self.popup_selected_index = idx
                        self.show_popup = False
                        print(f"Выбрано оружие {self.selected_weapon}")
                    break

    def draw(self, screen):
        # Фон
        if self.bg:
            screen.blit(self.bg, (0, 0))
        else:
            screen.fill((40, 40, 60))

        # Навигационные кнопки
        for btn in self.nav_buttons:
            screen.blit(self.button_images[btn["text"]], btn["rect"])

        char = self.game.player.party[0]

        # Информация о текущем оружии
        title = self.font.render("Оружие", True, (255, 255, 255))
        screen.blit(title, (700, 30))  # координаты подберите под свой фон

        if self.equipped_weapon:
            data = char.weapon_data.get(self.equipped_weapon, {})
            weapon_id = data.get("weapon_id")
            level = data.get("level", 1)
            if weapon_id:
                template = ITEM_DATA.get(weapon_id, {})
                name = template.get("name", "Неизвестно")
                base_atk = template.get("base_atk", 0)
                sec_stat = template.get("secondary_stat", {})
                sec_name = sec_stat.get("stat", "")
                sec_value = sec_stat.get("value", 0)
                # Отображаем информацию
                equip_text = self.stats_font.render(f"Экипировано: {name} (ур. {level})", True, (220, 220, 220))
                screen.blit(equip_text, (700, 60))
                atk_text = self.stats_font.render(f"Атака: {base_atk}", True, (200, 200, 200))
                screen.blit(atk_text, (700, 90))
                if sec_name:
                    sec_text = self.stats_font.render(f"{sec_name}: +{sec_value}", True, (200, 200, 200))
                    screen.blit(sec_text, (700, 120))
        else:
            equip_text = self.stats_font.render("Оружие не экипировано", True, (200, 200, 200))
            screen.blit(equip_text, (700, 60))

        # Если выбрано оружие, показываем его информацию
        if self.selected_weapon is not None:
            data = char.weapon_data.get(self.selected_weapon, {})
            weapon_id = data.get("weapon_id")
            level = data.get("level", 1)
            if weapon_id:
                template = ITEM_DATA.get(weapon_id, {})
                name = template.get("name", "Неизвестно")
                sel_text = self.stats_font.render(f"Выбрано: {name} (ур. {level})", True, (255, 255, 0))
                screen.blit(sel_text, (700, 150))

        # Кнопки "Экипировать/Сменить" и "Улучшить"
        btn_y = 630
        btn_width = 278
        btn_height = 62

        # Кнопка "Экипировать/Сменить"
        if self.equipped_weapon is not None:
            btn_img = self.unequip_btn_img
            btn_text = "Сменить"
        else:
            btn_img = self.equip_btn_img
            btn_text = "Экипировать"

        self.equip_btn_rect = pygame.Rect(720, btn_y, btn_width, btn_height)
        if btn_img:
            screen.blit(btn_img, self.equip_btn_rect)
        else:
            pygame.draw.rect(screen, (60, 60, 80), self.equip_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), self.equip_btn_rect, 2)
            text = self.font.render(btn_text, True, (255, 255, 255))
            screen.blit(text, (self.equip_btn_rect.x + 10, self.equip_btn_rect.y + 10))

        # Кнопка "Улучшить"
        self.upgrade_btn_rect = pygame.Rect(1050, btn_y, btn_width, btn_height)
        if self.upgrade_btn_img:
            screen.blit(self.upgrade_btn_img, self.upgrade_btn_rect)
        else:
            pygame.draw.rect(screen, (60, 60, 80), self.upgrade_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), self.upgrade_btn_rect, 2)
            text = self.font.render("Улучшить", True, (255, 255, 255))
            screen.blit(text, (self.upgrade_btn_rect.x + 10, self.upgrade_btn_rect.y + 10))

        # Плашка выбора оружия
        if self.show_popup:
            self.draw_popup(screen)

    def draw_popup(self, screen):
        # Затемнение
        dark = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 150))
        screen.blit(dark, (0, 0))

        popup_rect = pygame.Rect(0, 0, 400, 768)
        if self.popup_bg:
            screen.blit(self.popup_bg, popup_rect)
        else:
            pygame.draw.rect(screen, (50, 50, 70), popup_rect)
            pygame.draw.rect(screen, (200, 200, 200), popup_rect, 2)

        title = self.font.render("Выберите оружие", True, (255, 255, 255))
        screen.blit(title, (popup_rect.x + 20, popup_rect.y + 20))

        cell_size = 32
        margin = 10
        cols = 4
        start_x = popup_rect.x + 20
        start_y = popup_rect.y + 70
        self.popup_cell_rects = []

        char = self.game.player.party[0]

        for idx, unique_id in enumerate(self.popup_weapons):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (cell_size + margin)
            y = start_y + row * (cell_size + margin)
            rect = pygame.Rect(x, y, cell_size, cell_size)
            self.popup_cell_rects.append(rect)
            color = (100, 100, 150) if idx != self.popup_selected_index else (255, 255, 100)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

            data = char.weapon_data.get(unique_id, {})
            weapon_id = data.get("weapon_id")
            if weapon_id:
                template = ITEM_DATA.get(weapon_id, {})
                name = template.get("name", "?")
                # Иконка, если есть
                icon = self.weapon_icons.get(weapon_id)
                if icon:
                    screen.blit(icon, rect)
                else:
                    text_surf = self.stats_font.render(name, True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=rect.center)
                    screen.blit(text_surf, text_rect)

        esc_text = self.stats_font.render("ESC для закрытия", True, (0, 0, 0))
        screen.blit(esc_text, (20, 675))