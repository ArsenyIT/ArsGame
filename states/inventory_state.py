import pygame

class InventoryState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.selected_index = 0
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
        # Здесь можно загрузить данные инвентаря из глобального объекта
        print("Вход в инвентарь")
        self.font = pygame.font.Font(None, 28)
        self.inventory_menu_1 = pygame.image.load("assets/textures/Inventory/Menu_inventory_1.png")
        self.inventory_menu_2 = pygame.image.load("assets/textures/Inventory/Menu_inventory_2.png")

        self.weapon_iсon = pygame.image.load("assets/textures/Inventory/Icons/Icon_weapons.png")
        self.food_iсon = pygame.image.load("assets/textures/Inventory/Icons/Icon_foods.png")
        self.potion_iсon = pygame.image.load("assets/textures/Inventory/Icons/Icon_potions.png")
        self.resurs_iсon = pygame.image.load("assets/textures/Inventory/Icons/Icon_resources.png")
        self.artifact_iсon = pygame.image.load("assets/textures/Inventory/Icons/Icon_artifacts.png")
        self.rare_resurse_iсon = pygame.image.load("assets/textures/Inventory/Icons/Icon_rare_resources.png")
        self.special_tools_icon = pygame.image.load("assets/textures/Inventory/Icons/Icon_special_tools.png")

        self.empty_cell = pygame.image.load("assets/textures/Inventory/Cell_inventory.png").convert_alpha()
        self.oak_item_cell = pygame.image.load("assets/textures/Inventory/Oak_wood_inventory.png").convert_alpha()
        self.story_of_the_Almighty = pygame.image.load("assets/textures/Inventory/story_of_the_Almighty_inventory.png").convert_alpha()
        self.plume_1_inventory = pygame.image.load("assets/textures/Inventory/Plume_1_inventory.png").convert_alpha()
        self.plume_2_inventory = pygame.image.load("assets/textures/Inventory/Plume_2_inventory.png").convert_alpha()

        self.item_icons = {
            "oak_wood": self.oak_item_cell,
            "story_of_the_Almighty": self.story_of_the_Almighty,
            "plume_1": self.plume_1_inventory,
            "plume_2": self.plume_2_inventory,
            # добавляй новые предметы по мере появления
        }

    def on_exit(self):
        print("Выход из инвентаря")
        self.game.save_all()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")
                #elif event.key == pygame.K_UP:
                #    self.selected_index -= 1
                #elif event.key == pygame.K_DOWN:
                #    self.selected_index += 1
                #elif event.key == pygame.K_RETURN:
                #    items = self.get_item_list()
                #    if items and 0 <= self.selected_index < len(items):
                #        item_id, amount = items[self.selected_index]
                #        print(f"Использовать {item_id} (количество {amount})")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print(f"Клик в позиции {event.pos}")
                for btn in self.section_buttons:
                    print(f"  Проверяем {btn['section']} с rect {btn['rect']}")
                    if btn["rect"].collidepoint(event.pos):
                        self.current_section = btn["section"]
                        print(f"Раздел изменён на {btn['section']}")
                        break

        items = self.get_item_list()
        if items:
            if self.selected_index < 0:
                self.selected_index = 0
            if self.selected_index >= len(items):
                self.selected_index = len(items) - 1
        else:
            self.selected_index = 0

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
                    icon = self.item_icons.get(item_id, self.oak_item_cell)  # если нет иконки, используем oak_item_cell
                    screen.blit(icon, (x, y))
                    # Текст с названием и количеством
                    #text = f"{item_id}:{quantity}"
                    #text_surf = self.font.render(text, True, (255, 255, 255))
                    #screen.blit(text_surf, (x + 5, y + 5))
                else:
                    screen.blit(self.empty_cell, (x, y))
        # Подсказка внизу
        hint = self.font.render("B/ESC - выход, Левая кнопка мыши - Выбор предмета и переход в другие разделы", True, (150, 150, 150))
        screen.blit(hint, (50, screen.get_height() - 40))