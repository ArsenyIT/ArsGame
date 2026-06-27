import pygame
from inventory import ITEM_DATA

class ArtifactState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.field_width = 344
        self.offset = 10
        self.btn_width = self.field_width - 2 * self.offset  # 324
        self.btn_height = 120
        self.circle_positions = {
            "flower": (441, 238),
            "plume": (1017, 239),
            "sands": (439, 419),
            "goblet": (1018, 421),
        }
        self.circle_radius = 60
        self.circle_rects = {}
        for name, pos in self.circle_positions.items():
            x, y = pos
            self.circle_rects[name] = pygame.Rect(x - self.circle_radius, y - self.circle_radius,
                                                  self.circle_radius * 2, self.circle_radius * 2)
        self.active_slot = None  # хранит имя слота (flower, plume, ...) или None
        self.selected_artifact = None

    def on_enter(self):
        print("Вход в экран Артефакты")
        self.font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 28)
        self.bg = pygame.image.load("assets/textures/Арсений_Артефакты.png").convert_alpha()
        self.popup_bg = pygame.image.load("assets/textures/Плашка.png").convert_alpha()

        self.equip_btn = pygame.image.load("assets/textures/buttons/Кнопка_Экипировать.png").convert_alpha()
        self.unequip_btn = pygame.image.load("assets/textures/buttons/Кнопка_Сменить.png").convert_alpha()

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

    def on_exit(self):
        print("Выход из экрана Артефакты")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.active_slot:
                        # Если открыта плашка, закрываем её
                        self.active_slot = None
                    else:
                        pass

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.active_slot is not None:
                    # Проверка кликов по строкам артефактов
                    if hasattr(self, 'artifact_rows'):
                        for row in self.artifact_rows:
                            if row["rect"].collidepoint(event.pos):
                                self.selected_artifact = row["id"]
                                print(f"Выбран артефакт {row['id']}")
                                break

                    # Проверка клика по кнопке (Экипировать/Сменить)
                    if hasattr(self, 'current_btn_rect') and self.current_btn_rect.collidepoint(event.pos):
                        char = self.game.player.party[0]
                        current = char.artifacts.get(self.active_slot)
                        inventory = self.game.player.inventory
                        if current is None:
                            if self.selected_artifact is not None:
                                if inventory.get_count(self.selected_artifact) > 0:
                                    char.equip_artifact(self.active_slot, self.selected_artifact, inventory)
                                    self.selected_artifact = None
                                else:
                                    print("Выбранный артефакт больше не в инвентаре!")
                            else:
                                print("Сначала выберите артефакт из списка!")
                        else:
                            char.unequip_artifact(self.active_slot, inventory)
                            self.selected_artifact = None
                        self.active_slot = None

                if self.active_slot is None:
                    # Проверка кликов по кругам
                    for slot_name, rect in self.circle_rects.items():
                        if rect.collidepoint(event.pos):
                            self.active_slot = slot_name
                            print(f"Открыт слот {slot_name}")
                            break

                    # Проверка кликов по навигационным кнопкам
                    for btn in self.nav_buttons:
                        if btn["rect"].collidepoint(event.pos):
                            text = btn["text"]
                            if text == "Характеристика":
                                self.game.change_state("character")
                            elif text == "Оружие":
                                self.game.change_state("weapon")
                            elif text == "Артефакты":
                                pass
                            elif text == "Таланты":
                                self.game.change_state("talents")
                            elif text == "Созвездия":
                                self.game.change_state("constellations")
                            break

    def get_artifacts_from_inventory(self):
        all_items = self.game.player.inventory.items
        artifacts = []
        for item_id, quantity in all_items.items():
            if self.game.player.inventory.get_item_type(item_id) == "artifacts" and quantity > 0:
                artifacts.append(item_id)
        return artifacts

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        for btn in self.nav_buttons:
            screen.blit(self.button_images[btn["text"]], btn["rect"])

        for slot_name, pos in self.circle_positions.items():
            x, y = pos
            color = (200, 200, 200) if self.active_slot != slot_name else (100, 200, 100)
            pygame.draw.circle(screen, color, (x, y), self.circle_radius, 2)
            # Название слота под кругом
            text_surf = self.font.render(slot_name.capitalize(), True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(x, y + self.circle_radius + 15))
            screen.blit(text_surf, text_rect)

        if self.active_slot is not None:
            self.draw_popup(screen, self.active_slot)

    def draw_popup(self, screen, slot_name):
        dark = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 150))
        screen.blit(dark, (0, 0))

        popup_rect = pygame.Rect(0, 0, 400, 768)
        screen.blit(self.popup_bg, popup_rect)

        text = self.font.render(f"Слот: {slot_name}", True, (255, 255, 255))
        screen.blit(text, (popup_rect.x + 20, popup_rect.y + 20))

        artifacts = self.get_artifacts_from_inventory()
        self.artifact_rows = []
        y = 100
        for art_id in artifacts:
            art_data = ITEM_DATA.get(art_id, {})
            name = art_data.get("name", art_id)
            color = (255, 255, 0) if self.selected_artifact == art_id else (220, 220, 220)
            text_surf = self.stats_font.render(name, True, color)
            screen.blit(text_surf, (popup_rect.x + 20, y))
            row_rect = pygame.Rect(popup_rect.x + 20, y, text_surf.get_width(), 30)
            self.artifact_rows.append({"rect": row_rect, "id": art_id})
            y += 30

        char = self.game.player.party[0]
        current_artifact = char.artifacts.get(slot_name)

        btn_rect = pygame.Rect(popup_rect.x + 20, popup_rect.y + 650, 200, 50)
        if current_artifact is None:
            screen.blit(self.equip_btn, btn_rect)
        else:
            screen.blit(self.unequip_btn, btn_rect)
        self.current_btn_rect = btn_rect