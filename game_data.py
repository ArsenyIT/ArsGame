import pygame
import json

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

class Weapon:
    def __init__(self, name, weapon_type, rarity, base_atk):
        self.name = name
        self.weapon_type = weapon_type
        self.rarity = rarity
        self.base_atk = base_atk
        self.secondary_stat = None
        self.level = 1
        self.max_level = 100

    def get_total_atk(self):
        return self.base_atk

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