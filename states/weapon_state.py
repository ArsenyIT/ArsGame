import pygame
from inventory import ITEM_DATA
from game_data import calculate_weapon_stats
from input_handler import InputHandler

class WeaponState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.stats_font = None
        self.selected_uid = None  # UID выбранного оружия
        self.equipped_uid = None  # UID экипированного оружия
        self.show_popup = False
        self.popup_uids = []  # Список UID для отображения в плашке
        self.button_images = {}
        self.popup_selected_index = -1
        self.popup_cell_rects = []
        self.offset_y = self.game.HEIGHT * 0.026 #20
        self.offset_x = self.game.WIDTH * 0.0073 #10
        self.btn_width = self.game.WIDTH * 0.2372 #324
        self.btn_height = self.game.HEIGHT * 0.15625 #120

    def on_enter(self):
        self.font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 28)
        char_index = self.game.selected_character_index
        char = self.game.player.party[char_index]
        char_key = char.resource_key
        self.bg = self.game.resources.get_image(f"{char_key}_weapon")
        try:
            self.popup_bg = self.game.resources.get_image(f"{char_key}_popup_weapon")
        except:
            self.popup_bg = None
        # Кнопки
        try:
            self.equip_btn_img = self.game.resources.get_image(f"button_equip_2_{char_key}")
        except:
            self.equip_btn_img = None
        try:
            self.unequip_btn_img = self.game.resources.get_image(f"button_change_2_{char_key}")
        except:
            self.unequip_btn_img = None
        try:
            self.upgrade_btn_img = self.game.resources.get_image(f"button_improvement_{char_key}")
        except:
            self.upgrade_btn_img = None

        # Загрузка иконок для оружия (по шаблонному ID)
        self.weapon_icons = {}
        weapon_ids = ["sword_of_steel", "rusted_sword"]
        for w_id in weapon_ids:
            icon_name = f"{w_id}_inventory"
            try:
                icon = self.game.resources.get_image(icon_name)
                icon = pygame.transform.scale(icon, (32, 32))
                self.weapon_icons[w_id] = icon
            except pygame.error:
                self.weapon_icons[w_id] = None

        self.load_navigation_buttons()
        self.equipped_uid = char.weapon  # UID экипированного оружия
        self.update_popup_list()

        self.weapons = {}
        weapon_ids = ["sword_of_steel", "rusted_sword"]
        for w_id in weapon_ids:
            weapon_name = w_id
        try:
            weapon = self.game.resources.get_image(weapon_name)
            weapon = pygame.transform.scale(weapon, (self.game.WIDTH * 0.1537, self.game.HEIGHT * 0.56)) #210,430
            self.weapons[w_id] = weapon
        except pygame.error:
            self.weapons[w_id] = None

    def load_navigation_buttons(self):
        button_names = ["characteristic", "weapon", "artifacts", "talents", "symbolism"]
        char_index = self.game.selected_character_index
        char = self.game.player.party[char_index]
        char_key = char.resource_key
        for name in button_names:
            filename = f"button_{name}_{char_key}"
            try:
                img = self.game.resources.get_image(filename)
                img = pygame.transform.scale(img, (self.btn_width, self.btn_height))
                self.button_images[name] = img
            except pygame.error:
                surf = pygame.Surface((self.btn_width, self.btn_height))
                surf.fill((80, 80, 120))
                self.button_images[name] = surf
        self.nav_buttons = []
        x0_btn = 0
        y0_btn = self.game.HEIGHT * 0.058 #45
        for i, text in enumerate(button_names):
            y = y0_btn + self.offset_y + i * (self.btn_height + self.offset_y)
            rect = pygame.Rect(x0_btn + self.offset_x, y, self.btn_width, self.btn_height)
            self.nav_buttons.append({"text": text, "rect": rect})

    def update_popup_list(self):
        # Обновляет список UID оружия для плашки
        self.popup_uids = []
        inventory = self.game.player.inventory
        char = self.game.player.party[self.game.selected_character_index]
        # Получаем все UID оружия
        all_uids = inventory.get_all_uids("weapons")
        for uid in all_uids:
            # Проверяем, что запись в weapon_data существует
            data = char.weapon_data.get(str(uid), {})
            if data:  # если есть данные, значит оружие корректно
                self.popup_uids.append(uid)
        self.popup_selected_index = -1

    def on_exit(self):
        self.game.save_all()

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            if self.show_popup:
                self.show_popup = False
            else:
                self.game.change_state("world")
        if InputHandler.is_key_pressed(events, pygame.K_c):
            self.game.change_state("world")

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.show_popup:
                    self.handle_popup_click(event.pos)
                else:
                    self.handle_main_click(event.pos)

    def handle_main_click(self, pos):
        # Навигация
        for btn in self.nav_buttons:
            if btn["rect"].collidepoint(pos):
                if btn["text"] == "characteristic":
                    self.game.change_state("character")
                elif btn["text"] == "weapon":
                    pass
                elif btn["text"] == "artifacts":
                    self.game.change_state("artifact")
                elif btn["text"] == "talents":
                    self.game.change_state("talents")
                elif btn["text"] == "symbolism":
                    self.game.change_state("symbolism")
                break

        # Кнопка "Экипировать/Сменить"
        if hasattr(self, 'equip_btn_rect') and self.equip_btn_rect.collidepoint(pos):
            char = self.game.player.party[self.game.selected_character_index]
            inventory = self.game.player.inventory
            if self.equipped_uid is not None:
                # Снимаем оружие
                char.unequip_weapon()
                self.game.player.mark_modified()
                self.equipped_uid = None
                self.selected_uid = None
            else:
                if self.selected_uid is not None:
                    char.equip_weapon(self.selected_uid)
                    self.game.player.mark_modified()
                    self.equipped_uid = self.selected_uid
                    self.selected_uid = None
                else:
                    self.show_popup = True
                    self.update_popup_list()

        # Кнопка "Улучшить"
        if hasattr(self, 'upgrade_btn_rect') and self.upgrade_btn_rect.collidepoint(pos):
            if self.equipped_uid is not None:
                # Передаём UID экипированного оружия в следующее состояние
                self.game.temp_weapon_uid = self.equipped_uid
                self.game.change_state("weapon_upgrade")
            else:
                print("Нет экипированного оружия для улучшения!")

    def handle_popup_click(self, pos):
        if hasattr(self, 'popup_cell_rects'):
            for idx, rect in enumerate(self.popup_cell_rects):
                if rect.collidepoint(pos):
                    if idx < len(self.popup_uids):
                        uid = self.popup_uids[idx]
                        char = self.game.player.party[self.game.selected_character_index]
                        if self.equipped_uid is not None:
                            char.unequip_weapon()
                        char.equip_weapon(uid)
                        self.game.player.mark_modified()
                        self.equipped_uid = uid
                        self.selected_uid = None
                        self.show_popup = False
                    break

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

    def draw(self, screen):
        if self.bg:
            screen.blit(self.bg, (0, 0))
        else:
            screen.fill((40, 40, 60))

        for btn in self.nav_buttons:
            screen.blit(self.button_images[btn["text"]], btn["rect"])

        char = self.game.player.party[self.game.selected_character_index]

        if self.equipped_uid is not None:
            data = char.weapon_data.get(str(self.equipped_uid), {})
            weapon_id = data.get("weapon_id")
            level = data.get("level", 1)
            if weapon_id:
                template = ITEM_DATA.get(weapon_id, {})
                name = template.get("name", "Неизвестно")
                weapon_stats = calculate_weapon_stats(weapon_id, level)
                atk_display = weapon_stats["atk"]
                sec_display = weapon_stats["secondary_value"]
                sec_name = weapon_stats["secondary_stat"]
                icon = self.weapons.get(weapon_id)
                if icon:
                    icon_display = pygame.transform.scale(icon, (self.game.WIDTH * 0.1537, self.game.HEIGHT * 0.56)) #210,430
                    screen.blit(icon_display, (self.game.WIDTH * 0.454, self.game.HEIGHT * 0.2474)) #620,190
                # Полный текст для отображения
                full_text = f"{name} (ур. {level})"
                # Разбиваем на строки, если текст длинный
                lines = self.wrap_text(full_text, self.font, self.game.WIDTH * 0.1757) #240
                y_offset = self.game.HEIGHT * 0.065 #50
                for line in lines:
                    line_surf = self.font.render(line, True, (250, 250, 250))
                    screen.blit(line_surf, (self.game.WIDTH * 0.8133, y_offset)) #1111
                    y_offset += self.game.HEIGHT * 0.03255 #(25) отступ между строками
                atk_text = self.stats_font.render(f"Базовая АТК: {atk_display}", True, (220, 220, 220))
                screen.blit(atk_text, (self.game.WIDTH * 0.8133, self.game.HEIGHT * 0.1627)) #1111,125
                if sec_name:
                    sec_text = self.stats_font.render(f"{sec_name}: {sec_display}%", True, (220, 220, 220))
                    screen.blit(sec_text, (self.game.WIDTH * 0.8133, self.game.HEIGHT * 0.2018)) #1111,155

                effect_text = self.font.render("Бонус оружия:", True, (250, 250, 250))
                screen.blit(effect_text, (self.game.WIDTH * 0.8133, self.game.HEIGHT * 0.2539)) #1111,195
        else:
            equip_text = self.stats_font.render("Оружие не экипировано", True, (250, 250, 250))
            screen.blit(equip_text, (self.game.WIDTH * 0.8133, self.game.HEIGHT * 0.065)) #1111,50

        # Кнопки
        btn_y = self.game.HEIGHT * 0.8346 #641
        btn_width = self.game.WIDTH * 0.2035 #278
        btn_height = self.game.HEIGHT * 0.0807 #62

        if self.equipped_uid is not None:
            btn_img = self.unequip_btn_img
            btn_text = "Сменить"
        else:
            btn_img = self.equip_btn_img
            btn_text = "Экипировать"

        self.equip_btn_rect = pygame.Rect(self.game.WIDTH * 0.8089, btn_y, btn_width, btn_height) #1105
        if btn_img:
            screen.blit(btn_img, self.equip_btn_rect)
        else:
            pygame.draw.rect(screen, (60, 60, 80), self.equip_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), self.equip_btn_rect, 2)
            text = self.font.render(btn_text, True, (255, 255, 255))
            screen.blit(text, (self.equip_btn_rect.x + self.game.WIDTH * 0.0073, self.equip_btn_rect.y + self.game.HEIGHT * 0.013)) #10

        self.upgrade_btn_rect = pygame.Rect(self.game.WIDTH * 0.8089, btn_y - self.game.HEIGHT * 0.095, btn_width, btn_height) #1105,73
        if self.upgrade_btn_img:
            screen.blit(self.upgrade_btn_img, self.upgrade_btn_rect)
        else:
            pygame.draw.rect(screen, (60, 60, 80), self.upgrade_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), self.upgrade_btn_rect, 2)
            text = self.font.render("Улучшить", True, (255, 255, 255))
            screen.blit(text, (self.upgrade_btn_rect.x + self.game.WIDTH * 0.0073, self.upgrade_btn_rect.y + self.game.HEIGHT * 0.013)) #10

        if self.show_popup:
            self.draw_popup(screen)

    def draw_popup(self, screen):
        dark = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 150))
        screen.blit(dark, (0, 0))

        popup_rect = pygame.Rect(0, 0, self.game.WIDTH * 0.2928, self.game.HEIGHT) #400,768
        if self.popup_bg:
            screen.blit(self.popup_bg, popup_rect)
        else:
            pygame.draw.rect(screen, (50, 50, 70), popup_rect)
            pygame.draw.rect(screen, (200, 200, 200), popup_rect, 2)

        title = self.font.render("Выберите оружие", True, (255, 255, 255))
        screen.blit(title, (popup_rect.x + self.game.WIDTH * 0.0073, popup_rect.y + self.game.HEIGHT * 0.013)) #10

        cell_size = 32
        margin = 10
        cols = 4
        start_x = popup_rect.x + self.game.WIDTH * 0.0073 #10
        start_y = popup_rect.y + self.game.HEIGHT * 0.078 #60
        self.popup_cell_rects = []

        char = self.game.player.party[self.game.selected_character_index]

        for idx, uid in enumerate(self.popup_uids):
            row = idx // cols
            col = idx % cols
            x = start_x + col * (cell_size + margin)
            y = start_y + row * (cell_size + margin)
            rect = pygame.Rect(x, y, cell_size, cell_size)
            self.popup_cell_rects.append(rect)
            color = (100, 100, 150) if idx != self.popup_selected_index else (255, 255, 100)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

            data = char.weapon_data.get(str(uid), {})
            weapon_id = data.get("weapon_id")
            if weapon_id:
                template = ITEM_DATA.get(weapon_id, {})
                name = template.get("name", "?")
                icon = self.weapon_icons.get(weapon_id)
                if icon:
                    screen.blit(icon, rect)
                else:
                    text_surf = self.stats_font.render(name, True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=rect.center)
                    screen.blit(text_surf, text_rect)