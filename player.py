from inventory import Inventory
from game_data import Character
import json
import os
from game_data import generate_artifact_main_stat
from inventory import PREFIX_WEAPON

class Player:
    def __init__(self):
        self.inventory = Inventory()
        self.inventory.load("assets/data/inventory.json")

        with open("assets/data/characters/GG.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        hero = Character(
            name=data["name"],
            exp=data["exp"],
            exp_next=data["exp_next"],
            base_hp=data["base_hp"],
            base_atk=data["base_atk"],
            base_defense=data["base_defense"],
            crit_rate=data["crit_rate"],
            crit_dmg=data["crit_dmg"],
            energy_recharge=data["energy_recharge"],
            elemental_mastery=data["elemental_mastery"],
            phys_bonus=data["phys_bonus"],
            resistance=data["resistance"],
            speed=data["speed"],
            talents=data["talents"],
            portrait_path=data.get("portrait_path", None)
        )
        self.party = [hero]

        # Загружаем данные персонажей
        self.load_party("assets/data/party_save.json")
        self.convert_weapons_to_unique()

        # Если инвентарь пуст, добавляем тестовые предметы
        if not self.inventory.items:
            self.add_artifact("flower_1")
            self.add_artifact("sands_1")
            self.add_artifact("goblet_1")
            self.add_artifact("plume_1")
            self.add_artifact("plume_2")
            self.add_weapon("Sword_of_steel")
            self.add_weapon("Rusted_sword")
            self.inventory.add_item("artifact_exp", 50)
            self.inventory.add_item("weapon_exp", 50)
            self.inventory.add_item("story_of_the_Almighty", 5)
            self.inventory.add_item("talent_book_2", 10)

        self.modified = False

    def mark_modified(self):
        self.modified = True

    def add_artifact(self, artifact_id):
        unique_id = self.inventory.add_item(artifact_id, 1)
        if unique_id:
            hero = self.party[0]
            main_stat = generate_artifact_main_stat(artifact_id)
            if not main_stat:
                self.inventory.remove_item(unique_id)
                return False
            hero.artifact_data[unique_id] = {
                "level": 0,
                "sub_stats": [],
                "main_stat": main_stat,
                "artifact_id": artifact_id
            }
            print(f"Добавлен артефакт {artifact_id} с ID {unique_id}")
            return True
        return False

    def add_weapon(self, weapon_id):
        unique_id = self.inventory.add_item(weapon_id, 1)
        if unique_id:
            hero = self.party[0]
            hero.weapon_data[unique_id] = {
                "level": 1,
                "weapon_id": weapon_id
            }
            print(f"Добавлено оружие {weapon_id} с ID {unique_id}")
            return True
        return False

    def save_party(self, filename):
        chars_data = []
        for char in self.party:
            char_data = {
                "name": char.name,
                "level": char.level,
                "max_level": char.max_level,
                "exp": char.exp,
                "exp_next": char.exp_next,
                "base_hp": char.base_hp,
                "base_atk": char.base_atk,
                "base_defense": char.base_defense,
                "crit_rate": char.crit_rate,
                "crit_dmg": char.crit_dmg,
                "energy_recharge": char.energy_recharge,
                "elemental_mastery": char.elemental_mastery,
                "phys_bonus": char.phys_bonus,
                "resistance": char.resistance,
                "speed": char.speed,
                "talents": char.talents,
                "constellation": char.constellation,
                "weapon": char.weapon,
                "artifacts": char.artifacts,
                "artifact_data": char.artifact_data,
                "weapon_data": char.weapon_data,
            }
            chars_data.append(char_data)
        full_data = {
            "characters": chars_data
        }
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)
        self.modified = False
        print("Партия сохранена")

    def load_party(self, filename):
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                chars_data = data
                full_data = {"characters": chars_data}
            else:
                full_data = data
            chars_data = full_data.get("characters", [])
            for i, char in enumerate(self.party):
                if i < len(chars_data):
                    saved = chars_data[i]
                    char.level = saved.get("level", char.level)
                    char.max_level = saved.get("max_level", char.max_level)
                    char.exp = saved.get("exp", char.exp)
                    char.exp_next = saved.get("exp_next", char.exp_next)
                    char.base_hp = saved.get("base_hp", char.base_hp)
                    char.base_atk = saved.get("base_atk", char.base_atk)
                    char.base_defense = saved.get("base_defense", char.base_defense)
                    char.crit_rate = saved.get("crit_rate", char.crit_rate)
                    char.crit_dmg = saved.get("crit_dmg", char.crit_dmg)
                    char.energy_recharge = saved.get("energy_recharge", char.energy_recharge)
                    char.elemental_mastery = saved.get("elemental_mastery", char.elemental_mastery)
                    char.phys_bonus = saved.get("phys_bonus", char.phys_bonus)
                    char.resistance = saved.get("resistance", char.resistance)
                    char.speed = saved.get("speed", char.speed)
                    char.talents = saved.get("talents", char.talents)
                    char.constellation = saved.get("constellation", char.constellation)
                    char.weapon = saved.get("weapon", char.weapon)
                    char.artifacts = saved.get("artifacts", char.artifacts)
                    char.artifact_data = saved.get("artifact_data", {})
                    char.weapon_data = saved.get("weapon_data", {})
                    # Проверяем наличие основного стата у артефактов
                    for art_id, data in char.artifact_data.items():
                        if "main_stat" not in data:
                            main_stat = generate_artifact_main_stat(data.get("artifact_id", ""))
                            if main_stat:
                                data["main_stat"] = main_stat

                    # Восстанавливаем weapon_data для оружия, если оно потеряно
                    inventory = self.inventory
                    for item_id in inventory.get_unique_items(PREFIX_WEAPON):
                        if item_id not in char.weapon_data:
                            # Извлекаем weapon_id из уникального ID
                            # формат: weapon_{weapon_id}_{timestamp}_{counter}
                            parts = item_id.split('_')
                            if len(parts) >= 3:
                                weapon_id = parts[1]  # второй элемент
                                char.weapon_data[item_id] = {
                                    "level": 1,
                                    "weapon_id": weapon_id
                                }
                                print(f"Восстановлена запись для {item_id} -> {weapon_id}")
            print("Прогресс партии загружен")
        else:
            print("Файл партии не найден или пуст")

    def convert_weapons_to_unique(self):
        hero = self.party[0]
        to_convert = []
        for item_id, quantity in self.inventory.items.items():
            if self.inventory.get_item_type(item_id) == "weapons" and not item_id.startswith(PREFIX_WEAPON):
                to_convert.append((item_id, quantity))
        for old_id, quantity in to_convert:
            for _ in range(quantity):
                unique_id = self.add_weapon(old_id)
                if unique_id:
                    self.inventory.remove_item(old_id, 1)