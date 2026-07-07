import pygame
from inventory import ITEM_DATA

class ArtifactUpgradeState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.stats_font = None
        self.slot = None
        self.selected_uid = None          # UID выбранного артефакта
        self.equipped_uid = None          # UID экипированного артефакта
        self.show_popup = False
        self.popup_uids = []              # список UID для отображения в плашке
        self.popup_selected_index = -1
        self.popup_cell_rects = []

    def on_enter(self):
        self.font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 28)
        self.slot = getattr(self.game, "temp_slot", None)
        if not self.slot:
            self.game.change_state("artifact")
            return
        if hasattr(self.game, "temp_slot"):
            del self.game.temp_slot

        try:
            self.bg = pygame.image.load("assets/textures/characters_menu/GG/GG_upgrade.png").convert_alpha()
        except:
            self.bg = None
        try:
            self.popup_bg = pygame.image.load("assets/textures/Popup.png").convert_alpha()
        except:
            self.popup_bg = None

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

        # Иконки артефактов для отображения на фоне и в плашке
        self.artifact_icons = {
            "plume_1": self.load_icon("plume_1"),
            "plume_2": self.load_icon("plume_2"),
            "flower_1": self.load_icon("flower_1"),
            "sands_1": self.load_icon("sands_1"),
            "goblet_1": self.load_icon("goblet_1"),
        }

        char = self.game.player.party[0]
        self.equipped_uid = char.artifacts.get(self.slot)  # UID или None
        self.update_popup_list()

    def load_icon(self, artifact_id):
        try:
            icon = pygame.image.load(f"assets/textures/inventory/artifact_cell/{artifact_id}_inventory.png").convert_alpha()
            return pygame.transform.scale(icon, (32, 32))
        except:
            return None

    def update_popup_list(self):
        """Обновляет список UID артефактов для плашки (фильтрует по слоту)"""
        self.popup_uids = []
        inventory = self.game.player.inventory
        char = self.game.player.party[0]
        # Получаем все UID артефактов
        all_uids = inventory.get_all_uids("artifacts")
        for uid in all_uids:
            data = char.artifact_data.get(uid, {})
            if data:
                artifact_id = data.get("artifact_id")
                # Проверяем, что артефакт подходит по слоту
                if artifact_id:
                    art_data = ITEM_DATA.get(artifact_id, {})
                    if art_data.get("slot") == self.slot:
                        self.popup_uids.append(uid)
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
                        self.game.change_state("artifact")
                elif event.key == pygame.K_c:
                    self.game.change_state("artifact")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.show_popup:
                    self.handle_popup_click(event.pos)
                else:
                    self.handle_main_click(event.pos)

    def handle_main_click(self, pos):
        # Проверка кликов по навигационным кнопкам отсутствует (как и в weapon_state) – можно добавить, если нужно
        # Кнопка "Экипировать/Сменить"
        if hasattr(self, 'equip_btn_rect') and self.equip_btn_rect.collidepoint(pos):
            char = self.game.player.party[0]
            if self.equipped_uid is not None:
                # Снимаем артефакт
                char.unequip_artifact(self.slot)
                self.game.player.mark_modified()
                self.equipped_uid = None
                self.selected_uid = None
                print("Артефакт снят")
            else:
                if self.selected_uid is not None:
                    char.equip_artifact(self.slot, self.selected_uid)
                    self.game.player.mark_modified()
                    self.equipped_uid = self.selected_uid
                    self.selected_uid = None
                    print(f"Экипирован артефакт с UID {self.equipped_uid}")
                else:
                    self.show_popup = True
                    self.update_popup_list()

        # Кнопка "Улучшить"
        if hasattr(self, 'upgrade_btn_rect') and self.upgrade_btn_rect.collidepoint(pos):
            if self.equipped_uid is not None:
                char = self.game.player.party[0]
                inventory = self.game.player.inventory
                success = char.upgrade_artifact(self.equipped_uid, inventory)
                if success:
                    self.game.player.mark_modified()
                else:
                    print("Не удалось улучшить")
            else:
                print("Нет экипированного артефакта для улучшения!")

    def handle_popup_click(self, pos):
        if hasattr(self, 'popup_cell_rects'):
            for idx, rect in enumerate(self.popup_cell_rects):
                if rect.collidepoint(pos):
                    if idx < len(self.popup_uids):
                        uid = self.popup_uids[idx]
                        char = self.game.player.party[0]
                        if self.equipped_uid is not None:
                            char.unequip_artifact(self.slot)
                        char.equip_artifact(self.slot, uid)
                        self.game.player.mark_modified()
                        self.equipped_uid = uid
                        self.selected_uid = None
                        self.show_popup = False
                        print(f"Экипирован артефакт с UID {uid}")
                    break

    def draw(self, screen):
        if self.bg:
            screen.blit(self.bg, (0, 0))
        else:
            screen.fill((40, 40, 60))

        slot_names = {"flower": "Цветок", "plume": "Перо", "sands": "Часы", "goblet": "Кубок"}
        slot_display = slot_names.get(self.slot, self.slot.capitalize())
        title = self.font.render(f"Слот: {slot_display}", True, (255, 255, 255))
        screen.blit(title, (700, 30))

        char = self.game.player.party[0]

        # ---- Отображение экипированного артефакта ----
        if self.equipped_uid is not None:
            data = char.artifact_data.get(self.equipped_uid, {})
            artifact_id = data.get("artifact_id")
            if artifact_id:
                art_data = ITEM_DATA.get(artifact_id, {})
                name = art_data.get("name", "Неизвестно")
                equip_text = self.stats_font.render(f"Экипировано: {name}", True, (220, 220, 220))
                screen.blit(equip_text, (700, 60))

                # Иконка
                icon = self.artifact_icons.get(artifact_id)
                if icon:
                    icon_rect = icon.get_rect(topleft=(700, 120))
                    screen.blit(icon, icon_rect)

                # Уровень, основной стат, субстаты
                level = data.get("level", 0)
                main_stat = data.get("main_stat", {})
                sub_stats = data.get("sub_stats", [])

                level_text = self.stats_font.render(f"Уровень: {level}", True, (220, 220, 220))
                screen.blit(level_text, (1050, 30))

                if main_stat:
                    stat_name = list(main_stat.keys())[0]
                    stat_value = list(main_stat.values())[0]
                    if "%" in stat_name:
                        main_display = f"Основной: {stat_name} +{stat_value}%"
                    else:
                        main_display = f"Основной: {stat_name} +{stat_value}"
                    main_surf = self.stats_font.render(main_display, True, (255, 255, 200))
                    screen.blit(main_surf, (1050, 60))
                else:
                    main_surf = self.stats_font.render("Основной: нет", True, (200, 200, 200))
                    screen.blit(main_surf, (1050, 60))

                y_sub = 100
                if sub_stats:
                    for sub in sub_stats:
                        stat_name = sub["stat"]
                        value = sub["value"]
                        if "%" in stat_name:
                            display = f"{stat_name} +{value}%"
                        else:
                            display = f"{stat_name} +{value}"
                        sub_surf = self.stats_font.render(display, True, (200, 200, 200))
                        screen.blit(sub_surf, (1050, y_sub))
                        y_sub += 25
                else:
                    sub_surf = self.stats_font.render("Субстаты: отсутствуют", True, (200, 200, 200))
                    screen.blit(sub_surf, (1050, y_sub))
            else:
                equip_text = self.stats_font.render("Экипировано: неизвестно", True, (200, 200, 200))
                screen.blit(equip_text, (700, 60))
        else:
            equip_text = self.stats_font.render("Слот пуст", True, (200, 200, 200))
            screen.blit(equip_text, (700, 60))

        # ---- Отображение выбранного артефакта (из инвентаря) ----
        if self.selected_uid is not None:
            data = char.artifact_data.get(self.selected_uid, {})
            artifact_id = data.get("artifact_id")
            if artifact_id:
                art_data = ITEM_DATA.get(artifact_id, {})
                name = art_data.get("name", "Неизвестно")
                sel_text = self.stats_font.render(f"Выбрано: {name}", True, (255, 255, 0))
                screen.blit(sel_text, (700, 85))

                level = data.get("level", 0)
                main_stat = data.get("main_stat", {})
                sub_stats = data.get("sub_stats", [])

                level_sel = self.stats_font.render(f"Уровень: {level}", True, (220, 220, 220))
                screen.blit(level_sel, (700, 115))

                if main_stat:
                    stat_name = list(main_stat.keys())[0]
                    stat_value = list(main_stat.values())[0]
                    if "%" in stat_name:
                        main_display = f"Основной: {stat_name} +{stat_value}%"
                    else:
                        main_display = f"Основной: {stat_name} +{stat_value}"
                    main_surf = self.stats_font.render(main_display, True, (255, 255, 200))
                    screen.blit(main_surf, (700, 145))
                else:
                    main_surf = self.stats_font.render("Основной: нет", True, (200, 200, 200))
                    screen.blit(main_surf, (700, 145))

                y_sel_sub = 175
                if sub_stats:
                    for sub in sub_stats:
                        stat_name = sub["stat"]
                        value = sub["value"]
                        if "%" in stat_name:
                            display = f"{stat_name} +{value}%"
                        else:
                            display = f"{stat_name} +{value}"
                        sub_surf = self.stats_font.render(display, True, (200, 200, 200))
                        screen.blit(sub_surf, (700, y_sel_sub))
                        y_sel_sub += 25
                else:
                    sub_surf = self.stats_font.render("Субстаты: отсутствуют", True, (200, 200, 200))
                    screen.blit(sub_surf, (700, y_sel_sub))
        else:
            sel_text = self.stats_font.render("Ничего не выбрано", True, (200, 200, 200))
            screen.blit(sel_text, (700, 85))

        # ---- Кнопки ----
        btn_y = 630
        btn_width = 278
        btn_height = 62
        if self.equipped_uid is not None:
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

        self.upgrade_btn_rect = pygame.Rect(1050, btn_y, btn_width, btn_height)
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
        dark = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 150))
        screen.blit(dark, (0, 0))

        popup_rect = pygame.Rect(0, 0, 400, 768)
        if self.popup_bg:
            screen.blit(self.popup_bg, popup_rect)
        else:
            pygame.draw.rect(screen, (50, 50, 70), popup_rect)
            pygame.draw.rect(screen, (200, 200, 200), popup_rect, 2)

        title = self.font.render("Выберите артефакт", True, (255, 255, 255))
        screen.blit(title, (popup_rect.x + 20, popup_rect.y + 20))

        cell_size = 32
        margin = 10
        cols = 4
        start_x = popup_rect.x + 20
        start_y = popup_rect.y + 70
        self.popup_cell_rects = []

        char = self.game.player.party[0]

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

            data = char.artifact_data.get(uid, {})
            artifact_id = data.get("artifact_id")
            if artifact_id:
                art_data = ITEM_DATA.get(artifact_id, {})
                name = art_data.get("name", "?")
                icon = self.artifact_icons.get(artifact_id)
                if icon:
                    screen.blit(icon, rect)
                else:
                    text_surf = self.stats_font.render(name, True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=rect.center)
                    screen.blit(text_surf, text_rect)

        esc_text = self.stats_font.render("ESC для закрытия", True, (0, 0, 0))
        screen.blit(esc_text, (20, 675))