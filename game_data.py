import pygame
import json
from inventory import ITEM_DATA
import random

TALENT_BOOK_REQUIREMENTS = {
    1: (2, 2),   # с 1 на 2: 2 книги 2★
    2: (2, 3),
    3: (2, 4),
    4: (2, 6),
    5: (2, 8),
    6: (3, 2),   # с 6 на 7: 2 книги 3★
    7: (3, 3),
    8: (3, 4),
    9: (3, 6),
    10: (3, 8),
    11: (4, 2),  # с 11 на 12: 2 книги 4★
    12: (4, 4),
    13: (4, 6),
    14: (4, 8),
    15: (4, 10),
    16: (4, 12),
    17: (4, 14),
    18: (4, 16),
    19: (4, 18)}

def generate_artifact_main_stat(artifact_id):
    #Возвращает случайный основной стат для артефакта.
    #Если для артефакта нет possible_main_stats, возвращает None.
    art_data = ITEM_DATA.get(artifact_id, {})
    possible_main = art_data.get("possible_main_stats", [])
    if not possible_main:
        print(f"Для артефакта {artifact_id} не заданы возможные основные статы!")
        return None
    return random.choice(possible_main)

class Weapon:
    def __init__(self, name, weapon_type, rarity, base_atk):
        self.name = name
        self.weapon_type = weapon_type
        self.rarity = rarity
        self.base_atk = base_atk
        self.secondary_stat = None
        self.level = 1
        self.max_level = 100
        self.weapon_growth_data = {}
        self.load_weapon_growth()

    def load_weapon_growth(self):
        with open("assets/data/weapon_growth.json", "r", encoding="utf-8") as f:
            self.weapon_growth_data = json.load(f)

    def get_total_atk(self):
        return self.base_atk

    def get_weapon_stats(self, weapon_id, level):
        # Возвращает словарь с итоговой атакой и вторичным статом для оружия
        weapon_template = ITEM_DATA.get(weapon_id, {})
        base_atk = weapon_template.get("base_atk", 0)
        secondary = weapon_template.get("secondary_stat", {})
        sec_stat = secondary.get("stat", "")
        sec_base = secondary.get("value", 0)

        # Получаем бонусы из роста
        growth = self.weapon_growth_data.get(weapon_id, {}).get(str(level), {})
        atk_bonus = growth.get("atk_bonus", 0)
        sec_bonus = growth.get("secondary_bonus", 0)

        total_atk = base_atk + atk_bonus
        total_sec = sec_base + sec_bonus

        return {
            "atk": total_atk,
            "secondary_stat": sec_stat,
            "secondary_value": total_sec
        }

class Artifact:
    def __init__(self, slot, set_name, rarity, main_stat):
        self.slot = slot
        self.set_name = set_name
        self.rarity = rarity
        self.level = 0
        self.main_stat = main_stat
        self.sub_stats = []

    def get_stat_bonus(self, stat_name):
        pass

class Character:
    def __init__(self, name, exp, exp_next,
                 base_hp, base_atk, base_defense, portrait_path,
                 crit_rate, crit_dmg, energy_recharge, elemental_mastery, phys_bonus, resistance, speed,
                 talents=None):
        self.name = name
        self.level = 1
        self.max_level = 10
        self.exp = exp
        self.exp_next = exp_next
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_defense = base_defense
        self.crit_rate = crit_rate
        self.crit_dmg = crit_dmg
        self.energy_recharge = energy_recharge
        self.elemental_mastery = elemental_mastery
        self.phys_bonus = phys_bonus
        self.resistance = resistance
        self.speed = speed
        self.talents = talents or {"normal": 1, "skill": 1, "burst": 1}
        self.constellation = 0
        self.weapon = None
        self.artifacts = {
            "flower": None,
            "plume": None,
            "sands": None,
            "goblet": None,
            "circlet": None}
        self.artifact_data = {}
        self.portrait_path = portrait_path
        self.load_growth_data()

    def load_growth_data(self):
        with open("assets/data/characters/GG_growth.json", "r", encoding="utf-8") as f:
            self.growth_data = json.load(f)

    def calculate_total_stats(self):
        pass

    def add_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_next:
            self.exp -= self.exp_next
            self.level_up()

    def level_up(self):
        self.level += 1
        growth = self.growth_data.get(str(self.level), {})
        self.base_hp += growth.get("hp", 0)
        self.base_atk += growth.get("atk", 0)
        self.base_defense += growth.get("def", 0)
        self.elemental_mastery += growth.get("em", 0)
        self.phys_bonus += growth.get("phys_bonus", 0)
        self.exp_next = int(self.exp_next * 1.5) + 250  # пересчёт опыта
        print(f"Уровень повышен до {self.level}")

    def can_ascend(self):
        ascend_levels = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        return self.level in ascend_levels and self.level >= self.max_level

    def ascend(self):
        self.max_level += 10  # или на 20, в зависимости от уровня
        self.exp = 0
        print(f"Максимальный уровень повышен до {self.max_level}")

    def get_talent_max_level(self):
        if self.max_level <= 10:
            return 2
        elif self.max_level <= 20:
            return 4
        elif self.max_level <= 30:
            return 6
        elif self.max_level <= 40:
            return 8
        elif self.max_level <= 50:
            return 10
        elif self.max_level <= 60:
            return 12
        elif self.max_level <= 70:
            return 14
        elif self.max_level <= 80:
            return 16
        elif self.max_level <= 90:
            return 18
        else:
            return 20

    def get_talent_book_requirement(self, current_level):
        #Возвращает (редкость, количество) книг для повышения таланта
        return TALENT_BOOK_REQUIREMENTS.get(current_level, (None, 0))

    def can_upgrade_talent(self, talent_name):
        #Проверяет, можно ли улучшить талант
        current_level = self.talents.get(talent_name, 1)
        max_level = self.get_talent_max_level()
        return current_level < max_level

    #def get_passive_talents(self):
        #Возвращает список активных пассивных талантов
    #    passives = []
    #    if self.level >= 1:
    #        passives.append(("Пассивный талант 1", "Увеличивает силу атаки на 10%"))
    #    if self.level >= 50:
    #        passives.append(("Пассивный талант 2", "Увеличивает скорость передвижения на 15%"))
    #    if self.level >= 100:
    #        passives.append(("Пассивный талант 3", "При использовании сверхспособности восстанавливает 20% HP"))
    #    return passives

    def activate_constellation(self):
        if self.constellation >= 6:
            print("Максимальный уровень созвездий достигнут!")
            return False
        # Увеличиваем уровень созвездия
        self.constellation += 1
        print(f"Созвездие активировано! Текущий уровень: {self.constellation}")
        return True

    def equip_artifact(self, slot, unique_id, player):
        # Проверяем, что артефакт есть в инвентаре
        if unique_id not in player.artifact_inventory:
            print("Артефакта нет в инвентаре!")
            return False
        # Если слот занят, снимаем старый
        if self.artifacts[slot] is not None:
            self.unequip_artifact(slot, player)
        # Удаляем из инвентаря
        player.artifact_inventory.remove(unique_id)
        # Экипируем
        self.artifacts[slot] = unique_id
        print(f"Экипирован артефакт {unique_id} в слот {slot}")
        return True

    def unequip_artifact(self, slot, player):
        unique_id = self.artifacts[slot]
        if unique_id is not None:
            player.artifact_inventory.append(unique_id)
            self.artifacts[slot] = None
            print(f"Снят артефакт {unique_id} со слота {slot}")
            return True
        return False

    def upgrade_artifact(self, unique_id, inventory):
        if unique_id not in self.artifact_data:
            print(f"Артефакт {unique_id} не найден в данных!")
            return False

        data = self.artifact_data[unique_id]
        current_level = data.get("level", 0)
        max_level = 20

        if current_level >= max_level:
            print(f"Артефакт {unique_id} уже достиг максимального уровня!")
            return False

        cost = (current_level + 1) * 10
        if inventory.get_count("artifact_exp") < cost:
            print(f"Недостаточно опыта! Нужно {cost}, есть {inventory.get_count('artifact_exp')}")
            return False
        inventory.remove_item("artifact_exp", cost)

        data["level"] += 1
        new_level = data["level"]

        template_id = data.get("artifact_id")
        if not template_id:
            print("Нет template_id для артефакта!")
            return False

        art_data = ITEM_DATA.get(template_id, {})
        pool = art_data.get("possible_sub_stats", [])

        if new_level in [4, 8, 12, 16]:
            if pool:
                import random
                existing_names = {sub["stat"] for sub in data["sub_stats"]}
                available = [s for s in pool if s not in existing_names]

                if available:
                    new_stat_name = random.choice(available)
                    new_value = self.get_initial_sub_stat_value(new_stat_name)
                    data["sub_stats"].append({"stat": new_stat_name, "value": new_value})
                    print(f"Добавлен субстат: {new_stat_name} +{new_value}")
                else:
                    if data["sub_stats"]:
                        sub_to_upgrade = random.choice(data["sub_stats"])
                        upgrade_amount = self.get_sub_stat_upgrade_amount(sub_to_upgrade["stat"])
                        sub_to_upgrade["value"] += upgrade_amount
                        print(f"Улучшен субстат {sub_to_upgrade['stat']} до {sub_to_upgrade['value']}")
            else:
                print(f"Нет возможных субстатов для {template_id}")

        print(f"Артефакт {unique_id} улучшен до уровня {new_level}")
        return True

    def get_initial_sub_stat_value(self, stat_name):
        #Возвращает начальное значение для нового субстата
        import random
        # Диапазоны для разных типов статов (примерные)
        ranges = {
            "HP": (10, 50),
            "ATK": (5, 20),
            "DEF": (5, 20),
            "HP%": (2.0, 5.0),
            "ATK%": (2.0, 5.0),
            "DEF%": (2.0, 5.0),
            "Crit Rate%": (2.0, 4.0),
            "Crit DMG%": (4.0, 8.0),
            "Energy Recharge%": (2.0, 5.0),
            "Elemental Mastery": (5, 20)
        }
        low, high = ranges.get(stat_name, (1, 5))
        return round(random.uniform(low, high), 1)

    def get_sub_stat_upgrade_amount(self, stat_name):
        #Возвращает величину улучшения для существующего субстата
        import random
        # Можно сделать небольшие прибавки (например, +1 или +0.5)
        if "%" in stat_name:
            return round(random.uniform(0.5, 1.5), 1)
        else:
            return round(random.uniform(1, 5))

    def upgrade_weapon(self, unique_id, inventory):
        if unique_id not in self.weapon_data:
            print("Оружие не найдено!")
            return False

        data = self.weapon_data[unique_id]
        current_level = data["level"]
        max_level = 20  # можно определить по редкости

        if current_level >= max_level:
            print("Максимальный уровень достигнут!")
            return False

        cost = (current_level + 1) * 10  # стоимость прокачки
        if inventory.get_count("weapon_exp") < cost:
            print(f"Недостаточно опыта оружия! Нужно {cost}")
            return False
        inventory.remove_item("weapon_exp", cost)

        data["level"] += 1
        print(f"Оружие {unique_id} улучшено до уровня {data['level']}")
        return True