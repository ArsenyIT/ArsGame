import json
from inventory import ITEM_DATA
import random

MAX_ARTIFACT_LEVEL_BY_RARITY = {
    1: 4,
    2: 8,
    3: 12,
    4: 16,
    5: 20,
}

TALENT_BOOK_REQUIREMENTS = {
    1: (2, 2),   # с 1 на 2: 2 книги 2★
    2: (2, 3),
    3: (2, 4),
    4: (2, 6),
    5: (2, 8),
    6: (3, 2),
    7: (3, 3),
    8: (3, 4),
    9: (3, 6),
    10: (3, 8),
    11: (4, 2),
    12: (4, 4),
    13: (4, 6),
    14: (4, 8),
    15: (4, 10),
    16: (4, 12),
    17: (4, 14),
    18: (4, 16),
    19: (4, 18)}

_weapon_growth_cache = None
_artifact_main_growth_cache = None

def generate_artifact_main_stat(artifact_id):
    # Возвращает случайный основной стат для артефакта.
    # Если для артефакта нет possible_main_stats, возвращает None.
    art_data = ITEM_DATA.get(artifact_id, {})
    possible_main = art_data.get("possible_main_stats", [])
    if not possible_main:
        print(f"Для артефакта {artifact_id} не заданы возможные основные статы!")
        return None
    return random.choice(possible_main)

def load_weapon_growth():
    global _weapon_growth_cache
    if _weapon_growth_cache is None:
        try:
            with open("assets/data/weapon_growth.json", "r", encoding="utf-8") as f:
                _weapon_growth_cache = json.load(f)
        except FileNotFoundError:
            _weapon_growth_cache = {}
    return _weapon_growth_cache

def load_artifact_main_growth():
    global _artifact_main_growth_cache
    if _artifact_main_growth_cache is None:
        try:
            with open("assets/data/artifact_main_growth.json", "r", encoding="utf-8") as f:
                _artifact_main_growth_cache = json.load(f)
        except FileNotFoundError:
            _artifact_main_growth_cache = {}
    return _artifact_main_growth_cache

def get_artifact_main_stat_value(growth_key, level):
    growth = load_artifact_main_growth()
    stat_growth = growth.get(growth_key, {})
    level_str = str(level)
    if level_str in stat_growth:
        return stat_growth[level_str]
    # Если уровень не найден, ищем ближайший меньший
    keys = [int(k) for k in stat_growth.keys() if k.isdigit()]
    if not keys:
        return 0
    closest = max(k for k in keys if k <= level)
    return stat_growth[str(closest)]

def calculate_weapon_stats(weapon_id, level):
    # Возвращает словарь с итоговой атакой и вторичным статом оружия
    template = ITEM_DATA.get(weapon_id, {})
    base_atk = template.get("base_atk", 0)
    secondary = template.get("secondary_stat", {})
    sec_base = secondary.get("value", 0)
    sec_stat = secondary.get("stat", "")

    growth_data = load_weapon_growth()
    # Приводим weapon_id к формату из JSON (заглавная первая буква)
    growth_key = weapon_id.capitalize()
    growth = growth_data.get(growth_key, {}).get(str(level), {})

    atk_bonus = growth.get("atk_bonus", 0)
    sec_bonus = growth.get("secondary_bonus", 0)

    return {
        "atk": base_atk + atk_bonus,
        "secondary_value": sec_base + sec_bonus,
        "secondary_stat": sec_stat
    }

class Character:
    def __init__(self, name, exp, exp_next,
                 base_hp, base_atk, base_defense, portrait_path,
                 crit_rate, crit_dmg, energy_recharge, elemental_mastery, phys_bonus, resistance, speed,
                 talents=None, growth_file = "GG_growth.json", resource_key="gg"):
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
        self.weapon_data = {}
        self.portrait_path = portrait_path
        self.growth_file = growth_file
        self.resource_key = resource_key
        self.load_growth_data()

    def load_growth_data(self):
        with open(f"assets/data/characters/{self.growth_file}", "r", encoding="utf-8") as f:
            self.growth_data = json.load(f)

    def calculate_total_stats(self):
        total = {
            "hp": self.base_hp,
            "atk": self.base_atk,
            "def": self.base_defense,
            "crit_rate": self.crit_rate,
            "crit_dmg": self.crit_dmg,
            "energy_recharge": self.energy_recharge,
            "elemental_mastery": self.elemental_mastery,
            "phys_bonus": self.phys_bonus,
            "resistance": self.resistance,
            "speed": self.speed,
        }

        # Бонусы от оружия
        if self.weapon is not None:
            uid_str = str(self.weapon)
            weapon_data = self.weapon_data.get(uid_str, {})
            weapon_id = weapon_data.get("weapon_id")
            level = weapon_data.get("level", 1)
            if weapon_id:
                stats = calculate_weapon_stats(weapon_id, level)
                total["atk"] += stats["atk"]
                # Вторичный стат оружия можно добавить к crit_rate, если это крит.

        # Бонусы от артефактов
        for slot, uid in self.artifacts.items():
            if uid is not None:
                uid_str = str(uid)
                data = self.artifact_data.get(uid_str, {})
                growth_key = data.get("growth_key")
                if growth_key:
                    level = data.get("level", 0)
                    value = get_artifact_main_stat_value(growth_key, level)
                    stat_name = growth_key.split('_', 1)[1]  # Тип стата
                    # Добавляем к соответствующему стату
                    if stat_name == "hp":
                        total["hp"] += int(value)
                    elif stat_name == "atk":
                        total["atk"] += int(value)
                    elif stat_name == "def":
                        total["def"] += int(value)
                    elif stat_name == "hp_percent":
                        total["hp"] += int(total["hp"] * value / 100)
                    elif stat_name == "atk_percent":
                        total["atk"] += int(total["atk"] * value / 100)
                    elif stat_name == "def_percent":
                        total["def"] += int(total["def"] * value / 100)
                    elif stat_name == "crit_rate":
                        total["crit_rate"] += value
                    elif stat_name == "crit_dmg":
                        total["crit_dmg"] += value
                    elif stat_name == "energy_recharge":
                        total["energy_recharge"] += value
                    elif stat_name == "elemental_mastery":
                        total["elemental_mastery"] += value
                    elif stat_name == "phys_bonus":
                        total["phys_bonus"] += value

                # Субстаты
                for sub in data.get("sub_stats", []):
                    sub_name = sub.get("stat")
                    sub_value = sub.get("value", 0)
                    if sub_name == "HP":
                        total["hp"] += sub_value
                    elif sub_name == "ATK":
                        total["atk"] += sub_value
                    elif sub_name == "DEF":
                        total["def"] += sub_value
                    elif sub_name == "HP%":
                        total["hp"] += int(total["hp"] * sub_value / 100)
                    elif sub_name == "ATK%":
                        total["atk"] += int(total["atk"] * sub_value / 100)
                    elif sub_name == "DEF%":
                        total["def"] += int(total["def"] * sub_value / 100)
                    elif sub_name == "Crit Rate%":
                        total["crit_rate"] += sub_value
                    elif sub_name == "Crit DMG%":
                        total["crit_dmg"] += sub_value
                    elif sub_name == "Energy Recharge%":
                        total["energy_recharge"] += sub_value
                    elif sub_name == "Elemental Mastery":
                        total["elemental_mastery"] += sub_value

        return total

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
        self.max_level += 10
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
        # Возвращает редкость и количество книг для повышения таланта
        return TALENT_BOOK_REQUIREMENTS.get(current_level, (None, 0))

    def can_upgrade_talent(self, talent_name):
        # Проверяет, можно ли улучшить талант
        current_level = self.talents.get(talent_name, 1)
        max_level = self.get_talent_max_level()
        return current_level < max_level

    #def get_passive_talents(self):
        # Возвращает список активных пассивных талантов
    #    passives = []
    #    if self.level >= 1:
    #        passives.append(("Пассивный талант 1", "Увеличивает силу атаки на 10%"))
    #    if self.level >= 50:
    #        passives.append(("Пассивный талант 2", "Увеличивает скорость передвижения на 15%"))
    #    if self.level >= 100:
    #        passives.append(("Пассивный талант 3", "При использовании сверхспособности восстанавливает 20% HP"))
    #    return passives

    def activate_constellation(self):
        if self.constellation >= 5:
            print("Максимальный уровень созвездий достигнут!")
            return False
        # Увеличиваем уровень созвездия
        self.constellation += 1
        print(f"Созвездие активировано! Текущий уровень: {self.constellation}")
        return True

        # ----- Артефакты -----
    def equip_artifact(self, slot, uid):
        # Экипирует артефакт по UID в указанный слот
        uid_str = str(uid)
        if uid_str not in self.artifact_data:
            print(f"Артефакт с UID {uid} не найден в данных!")
            return False
        if slot not in self.artifacts:
            print(f"Неверный слот: {slot}")
            return False
        # Если слот занят, снимаем старый
        if self.artifacts[slot] is not None:
            self.unequip_artifact(slot)
        self.artifacts[slot] = uid_str
        print(f"Экипирован артефакт с UID {uid} в слот {slot}")
        return True

    def unequip_artifact(self, slot):
        # Снимает артефакт из слота (не добавляет в инвентарь)
        if slot in self.artifacts and self.artifacts[slot] is not None:
            self.artifacts[slot] = None
            print(f"Снят артефакт из слота {slot}")
            return True
        return False

    def get_artifact_max_level(self, artifact_id):
        # Возвращает максимальный уровень для артефакта по его редкости
        art_data = ITEM_DATA.get(artifact_id, {})
        rarity = art_data.get("rarity", 1)  # по умолчанию 1★
        return MAX_ARTIFACT_LEVEL_BY_RARITY.get(rarity, 4)

    def upgrade_artifact(self, uid, inventory):
        uid_str = str(uid)
        if uid_str not in self.artifact_data:
            print(f"Артефакт {uid} не найден в данных!")
            return False

        data = self.artifact_data[uid_str]
        # Инициализация полей опыта, если их нет (для старых сохранений)
        if "exp" not in data:
            data["exp"] = 0
        if "exp_next" not in data:
            data["exp_next"] = 100

        # Проверка максимального уровня
        artifact_id = data.get("artifact_id")
        max_level = self.get_artifact_max_level(artifact_id)
        if data.get("level", 0) >= max_level:
            print(f"Артефакт уже достиг максимального уровня ({max_level})!")
            return False

        # Проверяем наличие опыта артефактов
        exp_gain = ITEM_DATA.get("artifact_exp", {}).get("exp_gain", 50)
        if inventory.get_count("artifact_exp") == 0:
            print("Нет опыта артефактов!")
            return False

        # Тратим один флакон опыта
        inventory.remove_item("artifact_exp", 1)
        data["exp"] += exp_gain

        # Проверяем, не достигнут ли следующий уровень
        while data["exp"] >= data["exp_next"]:
            data["exp"] -= data["exp_next"]
            data["level"] += 1
            # Пересчитываем exp_next для следующего уровня
            data["exp_next"] = int(data["exp_next"] * 1.5) + 50
            print(f"Уровень артефакта повышен до {data['level']}")

            # Добавляем субстаты на уровнях 4, 8, 12, 16, 20
            if data["level"] in [4, 8, 12, 16, 20]:
                self._add_substat(data)

        return True

    def _add_substat(self, data):
        # Вспомогательный метод для добавления субстата
        template_id = data.get("artifact_id")
        if not template_id:
            return
        art_data = ITEM_DATA.get(template_id, {})
        pool = art_data.get("possible_sub_stats", [])
        if not pool:
            return
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

    def get_initial_sub_stat_value(self, stat_name):
        # Возвращает начальное значение для нового субстата
        ranges = { # Диапазоны для разных типов статов
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
        # Возвращает величину улучшения для существующего субстата
        # Можно сделать небольшие прибавки (например, +1 или +0.5)
        if "%" in stat_name:
            return round(random.uniform(0.5, 1.5), 1)
        else:
            return round(random.uniform(1, 5))

    # ----- Оружие -----
    def equip_weapon(self, uid):
        # Экипирует оружие по UID (не удаляет из инвентаря)
        uid_str = str(uid)
        if uid_str in self.weapon_data:
            # Если уже есть оружие, снимаем его
            if self.weapon is not None:
                self.unequip_weapon()
            self.weapon = uid_str
            print(f"Экипировано оружие с UID {uid}")
            return True
        print(f"Оружие с UID {uid} не найдено в данных!")
        return False

    def unequip_weapon(self):
        # Снимает оружие (не добавляет в инвентарь, оно там и так есть)
        if self.weapon is not None:
            self.weapon = None
            print("Оружие снято")
            return True
        return False

    def upgrade_weapon(self, uid, inventory):
        uid_str = str(uid)
        if uid_str not in self.weapon_data:
            print(f"Оружие с UID {uid} не найдено!")
            return False

        data = self.weapon_data[uid_str]
        # Инициализация полей опыта, если их нет (для старых сохранений)
        if "exp" not in data:
            data["exp"] = 0
        if "exp_next" not in data:
            data["exp_next"] = 100

        # Проверяем наличие кристаллов
        exp_gain = ITEM_DATA.get("crystal_of_true_power", {}).get("exp_gain", 50)
        if inventory.get_count("crystal_of_true_power") == 0:
            print("Нет кристаллов истинной силы!")
            return False

        # Тратим один кристалл
        inventory.remove_item("crystal_of_true_power", 1)
        data["exp"] += exp_gain

        # Проверяем, не достигнут ли следующий уровень
        while data["exp"] >= data["exp_next"]:
            data["exp"] -= data["exp_next"]
            data["level"] += 1
            # Пересчитываем exp_next для следующего уровня (аналогично персонажу)
            data["exp_next"] = int(data["exp_next"] * 1.5) + 50
            print(f"Уровень оружия повышен до {data['level']}")

        return True