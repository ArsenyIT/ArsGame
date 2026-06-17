import pygame
import json
import os

class Item:
    # Теперь конструктор принимает параметры
    def __init__(self, item_id, name, max_stack=1000):
        self.id = item_id          # уникальный идентификатор (строка или число)
        self.name = name           # отображаемое имя
        self.max_stack = max_stack # максимальное количество в стопке

class Inventory:
    def __init__(self):
        self.items = {}  # словарь: ключ - item_id, значение - количество
        self.modified = False

    def add_item(self, item_id, amount):
        #Добавляет указанное количество предмета в инвентарь
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
        """Возвращает количество предмета (0 если нет)"""
        return self.items.get(item_id, 0)