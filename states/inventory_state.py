import pygame

class InventoryState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.current_section = "resources"
        self.cols = 23
        self.rows = 13
        self.cell_size = 32
        self.cell_margin = 10
        self.grid_offset_x = 20
        self.grid_offset_y = 128
        self.section_buttons = [
            {"rect": pygame.Rect(0, 0, 127, 116), "section": "artifacts"},
            {"rect": pygame.Rect(129, 0, 127, 116), "section": "weapons"},
            {"rect": pygame.Rect(257, 0, 127, 116), "section": "food"},
            {"rect": pygame.Rect(385, 0, 127, 116), "section": "potions"},
            {"rect": pygame.Rect(513, 0, 127, 116), "section": "resources"},
            {"rect": pygame.Rect(641, 0, 127, 116), "section": "special_tools"},
            {"rect": pygame.Rect(769, 0, 127, 116), "section": "rare_resources"},
        ]

    def get_item_list(self):
        # Возвращает список (item_id, количество) из инвентаря
        inv_dict = self.game.player.inventory.items
        return list(inv_dict.items())

    def on_enter(self):
        # Загрузка данных инвентаря из глобального объекта
        print("Вход в инвентарь")
        self.font = pygame.font.Font(None, 28)
        self.quantity_font = pygame.font.Font(None, 14)
        self.inventory_menu_1 = pygame.image.load("assets/textures/inventory/menu_inventory/Menu_inventory_1.png")
        self.inventory_menu_2 = pygame.image.load("assets/textures/inventory/menu_inventory/Menu_inventory_2.png")

        self.weapon_iсon = pygame.image.load("assets/textures/inventory/icons/Icon_weapons.png")
        self.food_iсon = pygame.image.load("assets/textures/inventory/icons/Icon_foods.png")
        self.potion_iсon = pygame.image.load("assets/textures/inventory/icons/Icon_potions.png")
        self.resurs_iсon = pygame.image.load("assets/textures/inventory/icons/Icon_resources.png")
        self.artifact_iсon = pygame.image.load("assets/textures/inventory/icons/Icon_artifacts.png")
        self.rare_resurse_iсon = pygame.image.load("assets/textures/inventory/icons/Icon_rare_resources.png")
        self.special_tools_icon = pygame.image.load("assets/textures/inventory/icons/Icon_special_tools.png")

        self.empty_cell = pygame.image.load("assets/textures/inventory/Cell_inventory.png").convert_alpha()
        self.oak_wood_inventory = pygame.image.load("assets/textures/inventory/Oak_wood_inventory.png").convert_alpha()
        self.story_of_the_Almighty_inventory = pygame.image.load("assets/textures/inventory/Story_of_the_Almighty_inventory.png").convert_alpha()
        self.plume_1_inventory = pygame.image.load("assets/textures/inventory/artifact_cell/Plume_1_inventory.png").convert_alpha()
        self.plume_2_inventory = pygame.image.load("assets/textures/inventory/artifact_cell/Plume_2_inventory.png").convert_alpha()
        self.goblet_1_inventory = pygame.image.load("assets/textures/inventory/artifact_cell/Goblet_1_inventory.png").convert_alpha()
        self.sands_1_inventory = pygame.image.load("assets/textures/inventory/artifact_cell/Sands_1_inventory.png").convert_alpha()
        self.flower_1_inventory = pygame.image.load("assets/textures/inventory/artifact_cell/Flower_1_inventory.png").convert_alpha()
        self.artifact_exp_inventory = pygame.image.load("assets/textures/inventory/Artifact_exp_inventory.png").convert_alpha()
        self.sword_of_steel_inventory = pygame.image.load("assets/textures/inventory/weapon_cell/Sword_of_steel_inventory.png").convert_alpha()
        self.rusted_sword_inventory = pygame.image.load("assets/textures/inventory/weapon_cell/Rusted_sword_inventory.png").convert_alpha()
        self.hero_duplicate_inventory = pygame.image.load("assets/textures/inventory/Hero_duplicate_inventory.png").convert_alpha()
        self.talent_book_2_inventory = pygame.image.load("assets/textures/inventory/Talent_book_2_inventory.png").convert_alpha()

        self.item_icons = {
            "oak_wood": self.oak_wood_inventory,
            "story_of_the_Almighty": self.story_of_the_Almighty_inventory,
            "plume_1": self.plume_1_inventory,
            "plume_2": self.plume_2_inventory,
            "goblet_1": self.goblet_1_inventory,
            "sands_1": self.sands_1_inventory,
            "flower_1": self.flower_1_inventory,
            "artifact_exp": self.artifact_exp_inventory,
            "sword_of_steel": self.sword_of_steel_inventory,
            "rusted_sword": self.rusted_sword_inventory,
            "hero_duplicate": self.hero_duplicate_inventory,
            "talent_book_2": self.talent_book_2_inventory
        }

    def on_exit(self):
        print("Выход из инвентаря")
        self.game.save_all()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.section_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        self.current_section = btn["section"]
                        print(f"Раздел изменён на {btn['section']}")
                        break

    def draw(self, screen):
        screen.blit(self.inventory_menu_1, (0, 0))
        menu_2 = pygame.Rect(0, 119, 1000, 768)
        screen.blit(self.inventory_menu_2, menu_2)
        icon_1 = pygame.Rect(0, 0, 127, 116)
        icon_2 = pygame.Rect(129, 0, 127, 116)
        icon_3 = pygame.Rect(257, 0, 127, 116)
        icon_4 = pygame.Rect(385, 0, 127, 116)
        icon_5 = pygame.Rect(513, 0, 127, 116)
        icon_6 = pygame.Rect(641, 0, 127, 116)
        icon_7 = pygame.Rect(769, 0, 127, 116)
        screen.blit(self.artifact_iсon, icon_1)
        screen.blit(self.weapon_iсon, icon_2)
        screen.blit(self.food_iсon, icon_3)
        screen.blit(self.potion_iсon, icon_4)
        screen.blit(self.resurs_iсon, icon_5)
        screen.blit(self.special_tools_icon, icon_6)
        screen.blit(self.rare_resurse_iсon, icon_7)

        # Получаем список предметов
        items_dict = self.game.player.inventory.items
        items_list = list(items_dict.items())  # [(item_id, quantity), ...]

        all_items = self.game.player.inventory.items
        # Фильтруем по текущему разделу
        filtered_items = {
            item_id: amount for item_id, amount in all_items.items()
            if self.game.player.inventory.get_item_type(item_id) == self.current_section
        }
        items_list = list(filtered_items.items())

        # Рисуем сетку
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.grid_offset_x + col * (self.cell_size + self.cell_margin)
                y = self.grid_offset_y + row * (self.cell_size + self.cell_margin)
                idx = row * self.cols + col
                if idx < len(items_list):
                    item_id, quantity = items_list[idx]  # сначала получаем данные
                    icon = self.item_icons.get(item_id, self.oak_wood_inventory)  # если нет иконки, используем oak_wood_inventory
                    screen.blit(icon, (x, y))
                    # Текст с кол-вом предметов
                    text = f"х{quantity}"
                    text_surf = self.quantity_font.render(text, True, (255, 255, 255))
                    screen.blit(text_surf, (x, y + 21))
                else:
                    screen.blit(self.empty_cell, (x, y))
        # Подсказка внизу
        hint = self.font.render("B/ESC - выход, Левая кнопка мыши - Выбор предмета и переход в другие разделы", True, (150, 150, 150))
        screen.blit(hint, (50, screen.get_height() - 40))