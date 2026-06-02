import pygame

class InventoryState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.selected_index = 0

    def get_item_list(self):
        """Возвращает список (item_id, количество) из инвентаря"""
        inv_dict = self.game.player.inventory.items
        return list(inv_dict.items())

    def on_enter(self):
        # Здесь можно загрузить данные инвентаря из глобального объекта
        print("Вход в инвентарь")
        self.font = pygame.font.Font(None, 28)

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
        screen.fill((30, 30, 60))
        # Заголовок
        title = self.font.render("Инвентарь", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 20))

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