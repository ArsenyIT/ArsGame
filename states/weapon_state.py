import pygame
from inventory import ITEM_DATA
from inventory import PREFIX_WEAPON

class WeaponState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.stats_font = None
        self.selected_weapon = None
        self.equipped_weapon = None
        self.show_popup = False
        self.popup_weapons = []
        self.popup_selected_index = -1
        self.popup_cell_rects = []
        self.field_width = 344
        self.offset = 10
        self.btn_width = self.field_width - 2 * self.offset
        self.btn_height = 120

    def on_enter(self):
        self.font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 28)
        try:
            self.bg = pygame.image.load("assets/textures/characters_menu/GG/GG_weapon.png").convert_alpha()
        except:
            self.bg = None
        try:
            self.popup_bg = pygame.image.load("assets/textures/Popup.png").convert_alpha()
        except:
            self.popup_bg = None

        # Кнопки
        try:
            self.equip_btn_img = pygame.image.load("assets/textures/buttons/Button_equip.png").convert_alpha()
        except:
            self.equip_btn_img = None
        try:
            self.unequip_btn_img = pygame.image.load("assets/textures/buttons/Button_change.png").convert_alpha()
        except:
            self.unequip_btn_img = None
        try:
            self.upgrade_btn_img = pygame.image.load("assets/textures/buttons/Button_improve.png").convert_alpha()
        except:
            self.upgrade_btn_img = None

        # Загрузка иконок для оружия
        self.weapon_icons = {}
        weapon_ids = ["sword_of_steel", "rusted_sword"]
        for w_id in weapon_ids:
            icon_path = f"assets/textures/inventory/weapon_cell/{w_id.capitalize()}_inventory.png"
            try:
                icon = pygame.image.load(icon_path).convert_alpha()
                icon = pygame.transform.scale(icon, (32, 32))
                self.weapon_icons[w_id] = icon
            except pygame.error:
                self.weapon_icons[w_id] = None

        self.load_navigation_buttons()

        char = self.game.player.party[0]
        self.equipped_weapon = char.weapon
        self.update_popup_list()

    def on_exit(self):
        self.game.save_all()

    def load_navigation_buttons(self):
        self.button_images = {}
        button_names = ["characteristic", "weapon", "artifacts", "talents", "constellations"]
        for name in button_names:
            filename = f"assets/textures/buttons/Button_{name}.png"
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
        self.popup_weapons = []
        all_weapon_ids = self.game.player.inventory.get_unique_items(PREFIX_WEAPON)
        print("=== weapon_state debug ===")
        print("all_weapon_ids:", all_weapon_ids)
        char = self.game.player.party[0]
        for unique_id in all_weapon_ids:
            data = char.weapon_data.get(unique_id, {})
            weapon_id = data.get("weapon_id")
            print(f"  unique_id: {unique_id}, weapon_id: {weapon_id}")
            if weapon_id:
                self.popup_weapons.append(unique_id)
        self.popup_selected_index = -1
        print("popup_weapons:", self.popup_weapons)

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
                elif btn["text"] == "constellations":
                    self.game.change_state("constellations")
                break

        # Кнопка "Экипировать/Сменить"
        if hasattr(self, 'equip_btn_rect') and self.equip_btn_rect.collidepoint(pos):
            char = self.game.player.party[0]
            inventory = self.game.player.inventory
            if self.equipped_weapon is not None:
                char.unequip_weapon(inventory)
                self.game.player.mark_modified()
                self.equipped_weapon = None
                self.selected_weapon = None
            else:
                if self.selected_weapon is not None:
                    char.equip_weapon(self.selected_weapon, inventory)
                    self.game.player.mark_modified()
                    self.equipped_weapon = self.selected_weapon
                    self.selected_weapon = None
                else:
                    self.show_popup = True
                    self.update_popup_list()

        # Кнопка "Улучшить"
        if hasattr(self, 'upgrade_btn_rect') and self.upgrade_btn_rect.collidepoint(pos):
            if self.equipped_weapon is not None:
                char = self.game.player.party[0]
                inventory = self.game.player.inventory
                success = char.upgrade_weapon(self.equipped_weapon, inventory)
                if success:
                    self.game.player.mark_modified()

    def handle_popup_click(self, pos):
        if hasattr(self, 'popup_cell_rects'):
            for idx, rect in enumerate(self.popup_cell_rects):
                if rect.collidepoint(pos):
                    if idx < len(self.popup_weapons):
                        unique_id = self.popup_weapons[idx]
                        char = self.game.player.party[0]
                        inventory = self.game.player.inventory
                        if self.equipped_weapon is not None:
                            char.unequip_weapon(inventory)
                        char.equip_weapon(unique_id, inventory)
                        self.game.player.mark_modified()
                        self.equipped_weapon = unique_id
                        self.selected_weapon = None
                        self.show_popup = False
                    break

    def draw(self, screen):
        if self.bg:
            screen.blit(self.bg, (0, 0))
        else:
            screen.fill((40, 40, 60))

        for btn in self.nav_buttons:
            screen.blit(self.button_images[btn["text"]], btn["rect"])

        char = self.game.player.party[0]

        title = self.font.render("Оружие", True, (255, 255, 255))
        screen.blit(title, (1111, 50))

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
                # Иконка экипированного оружия
                icon = self.weapon_icons.get(weapon_id)
                if icon:
                    icon_display = pygame.transform.scale(icon, (40, 40))
                    screen.blit(icon_display, (1050, 80))
                equip_text = self.stats_font.render(f"Экипировано: {name} (ур. {level})", True, (220, 220, 220))
                screen.blit(equip_text, (1111, 80))
                atk_text = self.stats_font.render(f"Атака: {base_atk}", True, (200, 200, 200))
                screen.blit(atk_text, (1111, 110))
                if sec_name:
                    sec_text = self.stats_font.render(f"{sec_name}: +{sec_value}", True, (200, 200, 200))
                    screen.blit(sec_text, (1111, 140))
        else:
            equip_text = self.stats_font.render("Оружие не экипировано", True, (200, 200, 200))
            screen.blit(equip_text, (1111, 80))

        if self.selected_weapon is not None:
            data = char.weapon_data.get(self.selected_weapon, {})
            weapon_id = data.get("weapon_id")
            level = data.get("level", 1)
            if weapon_id:
                template = ITEM_DATA.get(weapon_id, {})
                name = template.get("name", "Неизвестно")
                sel_text = self.stats_font.render(f"Выбрано: {name} (ур. {level})", True, (255, 255, 0))
                screen.blit(sel_text, (1111, 150))

        btn_y = 640
        btn_width = 278
        btn_height = 62

        if self.equipped_weapon is not None:
            btn_img = self.unequip_btn_img
            btn_text = "Сменить"
        else:
            btn_img = self.equip_btn_img
            btn_text = "Экипировать"

        self.equip_btn_rect = pygame.Rect(1105, btn_y, btn_width, btn_height)
        if btn_img:
            screen.blit(btn_img, self.equip_btn_rect)
        else:
            pygame.draw.rect(screen, (60, 60, 80), self.equip_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), self.equip_btn_rect, 2)
            text = self.font.render(btn_text, True, (255, 255, 255))
            screen.blit(text, (self.equip_btn_rect.x + 10, self.equip_btn_rect.y + 10))

        self.upgrade_btn_rect = pygame.Rect(1105, btn_y - 73, btn_width, btn_height)
        if self.upgrade_btn_img:
            screen.blit(self.upgrade_btn_img, self.upgrade_btn_rect)
        else:
            pygame.draw.rect(screen, (60, 60, 80), self.upgrade_btn_rect)
            pygame.draw.rect(screen, (200, 200, 200), self.upgrade_btn_rect, 2)
            text = self.font.render("Улучшить", True, (255, 255, 255))
            screen.blit(text, (self.upgrade_btn_rect.x + 10, self.upgrade_btn_rect.y + 10))

        if self.show_popup:
            self.draw_popup(screen)

    def draw_popup(self, screen):
        print("draw_popup called")
        print("popup_weapons length:", len(self.popup_weapons))
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
                icon = self.weapon_icons.get(weapon_id)
                if icon:
                    screen.blit(icon, rect)
                else:
                    text_surf = self.stats_font.render(name, True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=rect.center)
                    screen.blit(text_surf, text_rect)

        esc_text = self.stats_font.render("ESC для закрытия", True, (0, 0, 0))
        screen.blit(esc_text, (20, 675))