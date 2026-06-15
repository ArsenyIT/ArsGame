import pygame

class InventoryState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.selected_index = 0

    def get_item_list(self):
        # Возвращает список (item_id, количество) из инвентаря
        inv_dict = self.game.player.inventory.items
        return list(inv_dict.items())

    def on_enter(self):
        # Здесь можно загрузить данные инвентаря из глобального объекта
        print("Вход в инвентарь")
        self.font = pygame.font.Font(None, 28)
        self.inventory_menu_1 = pygame.image.load("assets/textures/Инвентарь/Меню_инвентаря_1.png")
        self.inventory_menu_2 = pygame.image.load("assets/textures/Инвентарь/Меню_инвентаря_2.png")
        self.weapon_iсon = pygame.image.load("assets/textures/Инвентарь/Иконки/Иконка_оружий.png")
        self.food_iсon = pygame.image.load("assets/textures/Инвентарь/Иконки/Иконка_еды.png")
        self.potion_iсon = pygame.image.load("assets/textures/Инвентарь/Иконки/Иконка_зелий.png")
        self.resurs_iсon = pygame.image.load("assets/textures/Инвентарь/Иконки/Иконка_ресурсов.png")
        self.artifact_iсon = pygame.image.load("assets/textures/Инвентарь/Иконки/Иконка_артефактов.png")
        self.rare_resurse_iсon = pygame.image.load("assets/textures/Инвентарь/Иконки/Иконка_редких_ресурсов.png")
        self.special_tools_icon = pygame.image.load("assets/textures/Инвентарь/Иконки/Иконка_особых_инструментов.png")

    def on_exit(self):
        print("Выход из инвентаря")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")
                elif event.key == pygame.K_UP:
                    self.selected_index -= 1
                elif event.key == pygame.K_DOWN:
                    self.selected_index += 1
                elif event.key == pygame.K_RETURN:
                    items = self.get_item_list()
                    if items and 0 <= self.selected_index < len(items):
                        item_id, amount = items[self.selected_index]
                        print(f"Использовать {item_id} (количество {amount})")

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
        menu_2 = pygame.Rect(0,119,1000,768)
        screen.blit(self.inventory_menu_2, menu_2)
        icon_1 = pygame.Rect(0,0,126,116)
        icon_2 = pygame.Rect(129, 0, 255, 116)
        icon_3 = pygame.Rect(257, 0, 383, 116)
        icon_4 = pygame.Rect(385, 0, 511, 116)
        icon_5 = pygame.Rect(513, 0, 639, 116)
        icon_6 = pygame.Rect(641, 0, 767, 116)
        icon_7 = pygame.Rect(769, 0, 895, 116)
        #icon_8 = pygame.Rect(897, 0, 999, 116)
        screen.blit(self.artifact_iсon, icon_1)
        screen.blit(self.weapon_iсon, icon_2)
        screen.blit(self.food_iсon, icon_3)
        screen.blit(self.potion_iсon, icon_4)
        screen.blit(self.resurs_iсon, icon_5)
        screen.blit(self.special_tools_icon, icon_6)
        screen.blit(self.rare_resurse_iсon, icon_7)

        # Получаем список предметов
        items = self.get_item_list()
        y = 80
        for idx, (item_id, amount) in enumerate(items):
            # Цвет: белый для обычных, жёлтый для выбранного
            color = (255, 255, 200) if idx == self.selected_index else (200, 200, 200)
            text = self.font.render(f"{item_id}: {amount}", True, color)
            screen.blit(text, (50, y + idx * 30))

        # Подсказка внизу
        hint = self.font.render("B/ESC - выход, Стрелки - выбор, Enter - использовать", True, (150, 150, 150))
        screen.blit(hint, (50, screen.get_height() - 40))