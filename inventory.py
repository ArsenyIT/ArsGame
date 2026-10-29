import json
import os
import shutil

PREFIX_ARTIFACT = "artifact_"
PREFIX_WEAPON = "weapon_"

ITEM_DATA = {
    # Ресурсы
    "oak_wood": {
        "type": "resources",
        "name": "Дубовое бревно",
        "rarity": 1,
    },
    "poppy": {
        "type": "resources",
        "name": "Мак",
        "rarity": 1,
    },
    "chamomile": {
        "type": "resources",
        "name": "Ромашка",
        "rarity": 1,
    },
    "notes_for_beginner": {
        "type": "resources",
        "name": "Записи новичка",
        "rarity": 2,
        "exp_gain": 1000   # Кол-во опыта даёт книга
    },
    "guide_for_the_experienced_traveler": {
        "type": "resources",
        "name": "Сборник опытного путешественника",
        "rarity": 3,
        "exp_gain": 5000   # Кол-во опыта даёт книга
    },
    "story_of_the_Almighty": {
        "type": "resources",
        "name": "Сказание о Всемогущем",
        "rarity": 4,
        "exp_gain": 10000   # Кол-во опыта даёт книга
    },
    "collection_fencing_exercises": {
        "type": "resources",
        "name": "Сборник упражнений по фехтованию",
        "rarity": 2,
    },
    "fencing_textbook": {
        "type": "resources",
        "name": "Учебник по фехтованию",
        "rarity": 3,
    },
    "notes_fencing_master": {
        "type": "resources",
        "name": "Записи мастера по фехтованию",
        "rarity": 4,
    },
    "hero_duplicate": {
        "type": "resources",
        "name": "Дубликат героя",
        "rarity": 5,
    },
    "magic_elixir": {
        "type": "resources",
        "name": "Магический эликсир",
        "rarity": 2,
        "exp_gain": 50   # Кол-во опыта
    },
    "concentrated_elixir_of_secret_magic": {
        "type": "resources",
        "name": "Концентрированный эликсир тайной магии",
        "rarity": 3,
        "exp_gain": 200   # Кол-во опыта
    },
    "highly_concentrated_forbidden_magic": {
        "type": "resources",
        "name": "Высококонцентрированная запретная магия",
        "rarity": 4,
        "exp_gain": 1000   # Кол-во опыта
    },
    "electrified_crystal_fragments": {
        "type": "resources",
        "name": "Наэлектризованные фрагменты кристалла",
        "rarity": 1,
        "exp_gain": 50
    },
    "charged_crystal_fragment": {
        "type": "resources",
        "name": "Заряженный фрагмент кристалла",
        "rarity": 2,
        "exp_gain": 250
    },
    "crystal_of_true_power": {
        "type": "resources",
        "name": "Кристалл истинной силы",
        "rarity": 3,
        "exp_gain": 1000
    },
    # Артефакты
    "plume_1": {
    "type": "artifacts",
    "name": "Перо_1",
    "rarity": 1,
    "slot": "plume",
    "set": "??",
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
        "set": "???",
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
    "flower_2": {
        "type": "artifacts",
        "name": "Цветок_1",
        "rarity": 1,
        "slot": "flower",
        "set": "???",
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
    "sands_2": {
        "type": "artifacts",
        "name": "Часы_1",
        "rarity": 1,
        "slot": "sands",
        "set": "???",
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
    "goblet_2": {
        "type": "artifacts",
        "name": "Кубок_1",
        "rarity": 1,
        "slot": "goblet",
        "set": "???",
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
    # Оружие
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
    # Зелья
    # Особые инструменты
    # Редкие ресурсы
}

class Inventory:
    def __init__(self):
        self.items = {} # Для ресурсов: {"id": количество}; для уникальных: {"id": [UID1, UID2]}
        self.modified = False
        self.uid_counter = 0  # Глобальный счётчик UID

    def get_item_type(self, item_id):
        if item_id in ITEM_DATA:
            return ITEM_DATA[item_id].get("type")
        elif item_id.startswith(PREFIX_WEAPON):
            return "weapons"
        elif item_id.startswith(PREFIX_ARTIFACT):
            return "artifacts"
        else:
            return None

    def add_item(self, item_id, amount=1):
        item_data = ITEM_DATA.get(item_id, {})
        item_type = item_data.get("type")
        if item_type == "resources":
            if item_id in self.items:
                self.items[item_id] += amount
            else:
                self.items[item_id] = amount
            self.modified = True
            return None
        elif item_type in ["artifacts", "weapons"]:
            # Генерируем новый UID
            self.uid_counter += 1
            uid = self.uid_counter
            if item_id not in self.items:
                self.items[item_id] = []
            self.items[item_id].append(uid)
            self.modified = True
            return uid
        else:
            print(f"Неизвестный тип предмета: {item_type}")
            return None

    def remove_item(self, item_id, uid=None):
        # Для ресурсов уменьшаем количество
        if item_id in ITEM_DATA and ITEM_DATA[item_id].get("type") == "resources":
            if item_id not in self.items:
                return False
            self.items[item_id] -= 1
            if self.items[item_id] <= 0:
                del self.items[item_id]
            self.modified = True
            return True
        # Для уникальных предметов удаляем указанный UID (если не указан, удаляем последний)
        elif item_id in ITEM_DATA and ITEM_DATA[item_id].get("type") in ["artifacts", "weapons"]:
            if item_id not in self.items:
                return False
            if uid is None:
                if self.items[item_id]:
                    uid = self.items[item_id].pop()
                else:
                    return False
            else:
                if uid in self.items[item_id]:
                    self.items[item_id].remove(uid)
                else:
                    return False
            if not self.items[item_id]:
                del self.items[item_id]
            self.modified = True
            return uid
        else:
            return False

    def get_count(self, item_id):
        if item_id in ITEM_DATA and ITEM_DATA[item_id].get("type") == "resources":
            return self.items.get(item_id, 0)
        else:
            return len(self.items.get(item_id, []))

    def get_uid_list(self, item_id):
        return self.items.get(item_id, [])

    def get_all_uids(self, item_type=None):
        # Возвращает список всех UID для заданного типа (например, 'weapons')
        result = []
        for item_id, uids in self.items.items():
            if isinstance(uids, list):
                if item_type is None or (ITEM_DATA.get(item_id, {}).get("type") == item_type):
                    result.extend(uids)
        return result

    def save(self, filename):
        if os.path.exists(filename):
            shutil.copy2(filename, filename + ".backup")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
        self.modified = False

    def load(self, filename):
        # Попытка загрузить основной файл
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if self._validate_data(data):
                self.items = data
                self.modified = False
                return
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # Если основной файл невалиден или не загрузился — пробуем бэкап
        backup_file = filename + ".backup"
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if self._validate_data(data):
                self.items = data
                self.modified = False
                print("Загружен бэкап инвентаря")
                return
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # Если ничего не вышло — пустой инвентарь
        self.items = {}
        self.modified = False
        print("Инвентарь повреждён, создан новый")

    def _validate_data(self, data):
        if not isinstance(data, dict):
            return False

        for item_id, value in data.items():
            # Проверка ключа: он должен быть в ITEM_DATA или начинаться с префикса
            if item_id not in ITEM_DATA and not item_id.startswith(PREFIX_WEAPON) and not item_id.startswith(PREFIX_ARTIFACT):
                return False

            if isinstance(value, int):
                # Ресурсы (числа) не должны быть отрицательными
                if value < 0:
                    return False
            elif isinstance(value, list):
                # Уникальные предметы — список UID
                for uid in value:
                    if not isinstance(uid, int) or uid <= 0:
                        return False
            else: # Неизвестный тип данных
                return False

        return True