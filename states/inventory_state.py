import pygame
from inventory import PREFIX_WEAPON, PREFIX_ARTIFACT
from input_handler import InputHandler

class InventoryState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.current_section = "resources"
        self.cols = 23
        self.rows = 15
        self.cell_size = 32
        self.cell_margin = 10
        self.grid_offset_x = self.game.WIDTH * 0.01464 #20
        self.grid_offset_y = self.game.HEIGHT * 0.17 #128
        self.section_buttons = [
            {"rect": pygame.Rect(0, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15), "section": "artifacts"}, #127,116
            {"rect": pygame.Rect(self.game.WIDTH * 0.0944, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15), "section": "weapons"}, #129,127,116
            {"rect": pygame.Rect(self.game.WIDTH * 0.188, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15), "section": "food"}, #257,127,116
            {"rect": pygame.Rect(self.game.WIDTH * 0.2818, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15), "section": "potions"}, #385,127,116
            {"rect": pygame.Rect(self.game.WIDTH * 0.3755, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15), "section": "resources"}, #513,127,116
            {"rect": pygame.Rect(self.game.WIDTH * 0.46925, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15), "section": "special_tools"}, #641,127,116
            {"rect": pygame.Rect(self.game.WIDTH * 0.563, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15), "section": "rare_resources"}, #769,127,116
        ]

    def on_enter(self):
        # Загрузка данных инвентаря из глобального объекта
        print("Вход в инвентарь")
        self.font = pygame.font.Font(None, 28)
        self.quantity_font = pygame.font.Font(None, 14)
        self.inventory_menu_1 = self.game.resources.get_image("menu_inventory_1")
        self.inventory_menu_2 = self.game.resources.get_image("menu_inventory_2")

        self.weapon_icon = self.game.resources.get_image("icon_weapons")
        self.food_icon = self.game.resources.get_image("icon_foods")
        self.potion_icon = self.game.resources.get_image("icon_potions")
        self.resurs_icon = self.game.resources.get_image("icon_resources")
        self.artifact_icon = self.game.resources.get_image("icon_artifacts")
        self.rare_resources_icon = self.game.resources.get_image("icon_rare_resources")
        self.special_tools_icon = self.game.resources.get_image("icon_special_tools")

        self.empty_cell = self.game.resources.get_image("cell_inventory")
        self.oak_wood_inventory = self.game.resources.get_image("oak_wood_inventory")
        self.poppy_inventory = self.game.resources.get_image("poppy_inventory")
        self.chamomile_inventory = self.game.resources.get_image("chamomile_inventory")
        self.story_of_the_Almighty_inventory = self.game.resources.get_image("story_of_the_almighty_inventory")

        self.plume_1_inventory = self.game.resources.get_image("plume_1_inventory")
        self.plume_2_inventory = self.game.resources.get_image("plume_2_inventory")
        self.goblet_2_inventory = self.game.resources.get_image("goblet_2_inventory")
        self.sands_2_inventory = self.game.resources.get_image("sands_2_inventory")
        self.flower_2_inventory = self.game.resources.get_image("flower_2_inventory")

        self.magic_elixir_inventory = self.game.resources.get_image("magic_elixir_inventory")
        self.sword_of_steel_inventory = self.game.resources.get_image("sword_of_steel_inventory")
        self.rusted_sword_inventory = self.game.resources.get_image("rusted_sword_inventory")
        self.hero_duplicate_inventory = self.game.resources.get_image("hero_duplicate_inventory")
        self.fencing_textbook_inventory = self.game.resources.get_image("fencing_textbook_inventory")
        self.crystal_of_true_power_inventory = self.game.resources.get_image("crystal_of_true_power_inventory")

        self.item_icons = {
            "oak_wood": self.oak_wood_inventory,
            "poppy": self.poppy_inventory,
            "chamomile": self.chamomile_inventory,
            "story_of_the_Almighty": self.story_of_the_Almighty_inventory,
            "plume_1": self.plume_1_inventory,
            "plume_2": self.plume_2_inventory,
            "goblet_2": self.goblet_2_inventory,
            "sands_2": self.sands_2_inventory,
            "flower_2": self.flower_2_inventory,
            "magic_elixir": self.magic_elixir_inventory,
            "sword_of_steel": self.sword_of_steel_inventory,
            "rusted_sword": self.rusted_sword_inventory,
            "hero_duplicate": self.hero_duplicate_inventory,
            "fencing_textbook": self.fencing_textbook_inventory,
            "crystal_of_true_power": self.crystal_of_true_power_inventory
        }

    def on_exit(self):
        print("Выход из инвентаря")
        self.game.save_all()

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_b) or InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.section_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        self.current_section = btn["section"]
                        print(f"Раздел изменён на {btn['section']}")
                        break

    def get_grouped_items(self, section):
        # Возвращает словарь {шаблонный_ид: количество} для указанного раздела
        grouped = {}
        inventory = self.game.player.inventory
        for item_id, value in inventory.items.items():
            item_type = inventory.get_item_type(item_id)
            if item_type != section:
                continue
            if item_type in ["artifacts", "weapons"]:
                # value – список UID
                if isinstance(value, list):
                    count = len(value)  # уникальные: количество = число UID
                else:
                    count = value  # количество уже число
                grouped[item_id] = grouped.get(item_id, 0) + count
            else:
                # ресурсы – число
                grouped[item_id] = grouped.get(item_id, 0) + value
        return grouped

    def draw(self, screen):
        screen.blit(self.inventory_menu_1, (0, 0))
        menu_2 = pygame.Rect(0, self.game.HEIGHT * 0.155, self.game.WIDTH * 0.732, self.game.HEIGHT) #119,1000,768
        screen.blit(self.inventory_menu_2, menu_2)
        icon_1 = pygame.Rect(0, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15) #127,116
        icon_2 = pygame.Rect(self.game.WIDTH * 0.0944, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15) #129,127,116
        icon_3 = pygame.Rect(self.game.WIDTH * 0.188, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15) #257,127,116
        icon_4 = pygame.Rect(self.game.WIDTH * 0.2818, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15) #385,127,116
        icon_5 = pygame.Rect(self.game.WIDTH * 0.3755, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15) #513,127,116
        icon_6 = pygame.Rect(self.game.WIDTH * 0.46925, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15) #641,127,116
        icon_7 = pygame.Rect(self.game.WIDTH * 0.563, 0, self.game.WIDTH * 0.093, self.game.HEIGHT * 0.15) #769,127,116
        screen.blit(self.artifact_icon, icon_1)
        screen.blit(self.weapon_icon, icon_2)
        screen.blit(self.food_icon, icon_3)
        screen.blit(self.potion_icon, icon_4)
        screen.blit(self.resurs_icon, icon_5)
        screen.blit(self.special_tools_icon, icon_6)
        screen.blit(self.rare_resources_icon, icon_7)

        # Фильтруем по текущему разделу
        grouped_items = self.get_grouped_items(self.current_section)
        items_list = list(grouped_items.items())

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
                    screen.blit(text_surf, (x, y + self.game.HEIGHT * 0.026)) #20
                else:
                    screen.blit(self.empty_cell, (x, y))