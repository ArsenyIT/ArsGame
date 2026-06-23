import pygame

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
                 base_hp, base_atk, base_defense,
                 crit_rate, crit_dmg, energy_recharge, elemental_mastery, phys_bonus, resistance, speed,
                 talents=None):
        self.name = name
        self.level = 1
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

    def calculate_total_stats(self):
        pass

    def add_exp(self, amount):
        pass

    def level_up(self):
        pass