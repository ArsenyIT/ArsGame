import pygame
import json
import os

class Item:
    # Теперь конструктор принимает параметры
    def __init__(self, item_id, name, max_stack=1000):
        self.id = item_id          # уникальный идентификатор (строка или число)
        self.name = name           # отображаемое имя
        self.max_stack = max_stack # максимальное количество в стопке

ITEM_TYPES = {
    # Ресурсы
    "oak_wood": "resources",
    "stone": "resources",
    "iron_ore": "resources",
    "gold_ore": "resources",
    # Еда
    "apple": "food",
    "bread": "food",
    # Зелья
    "health_potion": "potions",
    "mana_potion": "potions",
    # Оружие
    "iron_sword": "weapons",
    "bow": "weapons",
    # Артефакты
    "flower_of_life": "artifacts",
    "plume_of_death": "artifacts",
    # Особые инструменты (если нужны)
    "special_key": "special_tools",
    # Редкие ресурсы
    "rare_crystal": "rare_resources",
}

class Inventory:
    def __init__(self):
        self.items = {}  # словарь: ключ - item_id, значение - количество
        self.modified = False

    def get_item_type(self, item_id):
        #Возвращает раздел предмета или None, если неизвестен
        return ITEM_TYPES.get(item_id)

    def add_item(self, item_id, amount):
        #Добавляет указанное количество предмета в инвентарь
        if item_id not in ITEM_TYPES:
            print(f"Предмет {item_id} не имеет типа! Добавьте его в ITEM_TYPES.")
            return
        if item_id in self.items:
            self.items[item_id] += amount
            self.modified = True
        else:
            self.items[item_id] = amount

    def remove_item(self, item_id, amount):
        #Удаляет указанное количество предмета (если достаточно)
        if item_id in self.items:
            self.items[item_id] -= amount
            self.modified = True
            if self.items[item_id] <= 0:
                del self.items[item_id]
            return True
        return False

    def get_count(self, item_id):
        #Возвращает количество предмета (0 если нет)
        return self.items.get(item_id, 0)

    def save(self, filename):
        #Сохраняет инвентарь в JSON-файл
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
        self.modified = False

    def load(self, filename):
        if os.path.exists(filename):
            # Проверяем, что файл не пустой
            if os.path.getsize(filename) > 0:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.items = json.load(f)
            else:
                self.items = {}
        else:
            self.items = {}
        self.modified = False