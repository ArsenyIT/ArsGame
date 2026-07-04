import pygame
import json
import os

PREFIX_ARTIFACT = "artifact_"
PREFIX_WEAPON = "weapon_"

ITEM_DATA = {
    "oak_wood": {
        "type": "resources",
        "name": "Дубовое бревно",
        "rarity": 1,
    },
    "story_of_the_Almighty": {
        "type": "resources",
        "name": "Сказание о Всемогущем",
        "rarity": 4,
        "exp_gain": 10000   # сколько опыта даёт книга
    },
    "talent_book_2": {
        "type": "resources",
        "name": "Книга талантов 2★",
        "rarity": 2,
    },
    "hero_duplicate": {
        "type": "resources",
        "name": "Дубликат героя",
        "rarity": 5,
    },
    "plume_1": {
    "type": "artifacts",
    "name": "Перо_1",
    "rarity": 1,
    "slot": "plume",
    "possible_main_stats": [
        {"atk": 100},
        {"atk": 110}
    ],
    "possible_sub_stats": [
            "HP",          # плоское значение HP
            "ATK",         # плоское значение ATK
            "DEF",         # плоское значение DEF
            "HP%",         # процент HP
            "ATK%",        # процент ATK
            "DEF%",        # процент DEF
            "Crit Rate%",
            "Crit DMG%",
            "Energy Recharge%",
            "Elemental Mastery"
        ]
    },
    "plume_2": {
        "type": "artifacts",
        "name": "Перо_2",
        "rarity": 1,
        "slot": "plume",
        "possible_main_stats": [
            {"atk": 105},
            {"atk": 115}
        ],
        "possible_sub_stats": [
            "HP",          # плоское значение HP
            "ATK",         # плоское значение ATK
            "DEF",         # плоское значение DEF
            "HP%",         # процент HP
            "ATK%",        # процент ATK
            "DEF%",        # процент DEF
            "Crit Rate%",
            "Crit DMG%",
            "Energy Recharge%",
            "Elemental Mastery"
        ]
    },
    "flower_1": {
        "type": "artifacts",
        "name": "Цветок_1",
        "rarity": 1,
        "slot": "flower",
        "possible_main_stats": [
            {"hp": 1000},
            {"hp": 1100}
        ],
        "possible_sub_stats": [
            "HP",          # плоское значение HP
            "ATK",         # плоское значение ATK
            "DEF",         # плоское значение DEF
            "HP%",         # процент HP
            "ATK%",        # процент ATK
            "DEF%",        # процент DEF
            "Crit Rate%",
            "Crit DMG%",
            "Energy Recharge%",
            "Elemental Mastery"
        ]
    },
    "sands_1": {
        "type": "artifacts",
        "name": "Часы_1",
        "rarity": 1,
        "slot": "sands",
        "possible_main_stats": [
            {"atk_percent": 4.0},
            {"hp_percent": 4.0},
            {"def_percent": 4.0},
            {"energy_recharge": 4.0},
            {"elemental_mastery": 20}
        ],
        "possible_sub_stats": [
            "HP",          # плоское значение HP
            "ATK",         # плоское значение ATK
            "DEF",         # плоское значение DEF
            "HP%",         # процент HP
            "ATK%",        # процент ATK
            "DEF%",        # процент DEF
            "Crit Rate%",
            "Crit DMG%",
            "Energy Recharge%",
            "Elemental Mastery"
        ]
    },
    "goblet_1": {
        "type": "artifacts",
        "name": "Кубок_1",
        "rarity": 1,
        "slot": "goblet",
        "possible_main_stats": [
            {"atk_percent": 4.0},
            {"hp_percent": 4.0},
            {"def_percent": 4.0},
            {"phys_dmg_percent": 5.0},
            {"elec_dmg_percent": 5.0},
            {"hydro_dmg_percent": 5.0},
            {"pyro_dmg_percent": 5.0},
            {"cryo_dmg_percent": 5.0},
            {"anemo_dmg_percent": 5.0},
            {"geo_dmg_percent": 5.0},
            {"dendro_dmg_percent": 5.0}
        ],
        "possible_sub_stats": [
            "HP",          # плоское значение HP
            "ATK",         # плоское значение ATK
            "DEF",         # плоское значение DEF
            "HP%",         # процент HP
            "ATK%",        # процент ATK
            "DEF%",        # процент DEF
            "Crit Rate%",
            "Crit DMG%",
            "Energy Recharge%",
            "Elemental Mastery"
        ]
    },
    "artifact_exp": {
        "type": "resources",
        "name": "Артефактный опыт",
        "rarity": 2,
    },
    "sword_of_steel": {
        "type": "weapons",
        "name": "Стальной меч",
        "weapon_type": "sword",
        "rarity": 1,
        "base_atk": 50,
        "secondary_stat": {"stat": "ATK%", "value": 10}
    },
    "rusted_sword": {
        "type": "weapons",
        "name": "Ржавый меч",
        "weapon_type": "sword",
        "rarity": 1,
        "base_atk": 40,
        "secondary_stat": {"stat": "Crit Rate%", "value": 5}
    }
    # Еда
    #"apple": "food",
    #"bread": "food",
    # Зелья
    #"health_potion": "potions",
    #"mana_potion": "potions",
    # Оружие
    #"iron_sword": "weapons",
    #"bow": "weapons",
    # Артефакты
    #"flower_of_life": "artifacts",
    #"plume_of_death": "artifacts",
    # Особые инструменты (если нужны)
    #"special_key": "special_tools",
    # Редкие ресурсы
    #"rare_crystal": "rare_resources",
}

class Item:
    # Теперь конструктор принимает параметры
    def __init__(self, item_id, name, max_stack=1000):
        self.id = item_id          # уникальный идентификатор (строка или число)
        self.data = ITEM_DATA.get(item_id, {})
        self.max_stack = max_stack # максимальное количество в стопке
        self.items = {}
        self.modified = False
        self.counter = 0  # для генерации уникальных ID

class Inventory:
    def __init__(self):
        self.items = {}  # словарь: ключ - item_id, значение - количество
        self.modified = False

    def get_item_type(self, item_id):
        #Возвращает раздел предмета или None, если неизвестен
        return ITEM_DATA.get(item_id, {}).get("type")

    def add_item(self, item_id, amount=1):
        item_data = ITEM_DATA.get(item_id, {})
        item_type = item_data.get("type")
        if item_type == "resources":
            if item_id in self.items:
                self.items[item_id] += amount
            else:
                self.items[item_id] = amount
            self.modified = True
            return None  # ресурсы не имеют уникального ID
        elif item_type in ["artifacts", "weapons"]:
            # Генерируем уникальный ID с префиксом
            if item_type == "artifacts":
                prefix = PREFIX_ARTIFACT
            else:
                prefix = PREFIX_WEAPON
            self.counter += 1
            import time
            unique_id = f"{prefix}{item_id}_{int(time.time() * 1000)}_{self.counter}"
            self.items[unique_id] = 1
            self.modified = True
            return unique_id
        else:
            print(f"Неизвестный тип предмета: {item_type}")
            return None

    def remove_item(self, item_id, amount=1):
        if item_id not in self.items:
            return False
        if item_id.startswith(PREFIX_ARTIFACT) or item_id.startswith(PREFIX_WEAPON):
            del self.items[item_id]
            self.modified = True
            return True
        else:
            self.items[item_id] -= amount
            if self.items[item_id] <= 0:
                del self.items[item_id]
            self.modified = True
            return True

    def get_unique_items(self, prefix):
        # Возвращает список уникальных ID, начинающихся с указанного префикса
        result = []
        for key in self.items:
            if key.startswith(prefix):
                result.append(key)
        return result

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