from inventory import Inventory
from game_data import Character
import random
import json
import os
from game_data import generate_artifact_main_stat
from inventory import ITEM_DATA
from inventory import PREFIX_WEAPON
import shutil

class Player:
    def __init__(self):
        self.inventory = Inventory()
        self.inventory.load("assets/data/inventory.json")

        with open("assets/data/characters/GG.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        with open("assets/data/characters/Infection.json", "r", encoding="utf-8") as f:
            inf_data = json.load(f)

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
        Infection = Character(
            name=inf_data["name"],
            exp=inf_data["exp"],
            exp_next=inf_data["exp_next"],
            base_hp=inf_data["base_hp"],
            base_atk=inf_data["base_atk"],
            base_defense=inf_data["base_defense"],
            crit_rate=inf_data["crit_rate"],
            crit_dmg=inf_data["crit_dmg"],
            energy_recharge=inf_data["energy_recharge"],
            elemental_mastery=inf_data["elemental_mastery"],
            phys_bonus=inf_data["phys_bonus"],
            resistance=inf_data["resistance"],
            speed=inf_data["speed"],
            talents=inf_data["talents"],
            portrait_path=inf_data.get("portrait_path", None),
            growth_file="Infection_growth.json"
        )
        self.party = [hero, Infection]

        # Загружаем данные персонажей
        self.load_party("assets/data/party_save.json")

        hero = self.party[0]
        for uid in self.inventory.get_all_uids("weapons"):
            uid_str = str(uid)
            if uid_str not in hero.weapon_data:
                for item_id, uids in self.inventory.items.items():
                    if isinstance(uids, list) and uid in uids:
                        if self.inventory.get_item_type(item_id) == "weapons":
                            hero.weapon_data[uid_str] = {
                                "level": 1,
                                "weapon_id": item_id
                            }
                            print(f"Восстановлена запись для оружия {item_id} с UID {uid}")
                        break

        # Восстанавливаем artifact_data для существующих UID артефактов
        for uid in self.inventory.get_all_uids("artifacts"):
            uid_str = str(uid)
            if uid_str not in hero.artifact_data:
                for item_id, uids in self.inventory.items.items():
                    if isinstance(uids, list) and uid in uids:
                        if self.inventory.get_item_type(item_id) == "artifacts":
                            main_stat = generate_artifact_main_stat(item_id)
                            if not main_stat:
                                main_stat = {}
                            hero.artifact_data[uid_str] = {
                                "level": 1,
                                "exp": 0,
                                "exp_next": 100,
                                "sub_stats": [],
                                "main_stat": main_stat,
                                "artifact_id": item_id
                            }
                            print(f"Восстановлена запись для артефакта {item_id} с UID {uid}")
                        break

        # Сохраняем партию, чтобы в следующий раз данные уже были
        self.save_party("assets/data/party_save.json")

    def mark_modified(self):
        self.modified = True

    def add_artifact(self, artifact_id):
        uid = self.inventory.add_item(artifact_id, 1)
        if uid:
            hero = self.party[0]
            art_data = ITEM_DATA.get(artifact_id, {})
            slot = art_data.get("slot")
            possible_main = art_data.get("possible_main_stats", [])
            if not possible_main or not slot:
                self.inventory.remove_item(artifact_id, uid)
                return False
            chosen = random.choice(possible_main)
            stat_name = list(chosen.keys())[0]
            growth_key = f"{slot}_{stat_name}"
            hero.artifact_data[str(uid)] = {
                "level": 1,  # Начальный уровень
                "exp": 0,
                "exp_next": 100,
                "sub_stats": [],
                "growth_key": growth_key,
                "artifact_id": artifact_id
            }
            print(f"Добавлен артефакт {artifact_id} с UID {uid}")
            return True
        return False

    def add_weapon(self, weapon_id):
        uid = self.inventory.add_item(weapon_id, 1)
        if uid:
            hero = self.party[0]
            hero.weapon_data[str(uid)] = {
                "level": 1,
                "weapon_id": weapon_id,
                "exp": 0,
                "exp_next": 100
            }
            print(f"Добавлено оружие {weapon_id} с UID {uid}")
            return True
        return False

    def save_party(self, filename):
        if os.path.exists(filename):
            shutil.copy2(filename, filename + ".backup")
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
        # Вспомогательная функция для применения данных к персонажам
        def apply_data(chars_data):
            for i, char in enumerate(self.party):
                if i < len(chars_data):
                    saved = chars_data[i]
                    # Применяем все поля (как у тебя было)
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
                    # Восстановление growth_key (как у тебя)
                    for uid, data in char.artifact_data.items():
                        if "growth_key" not in data:
                            artifact_id = data.get("artifact_id")
                            main_stat = data.get("main_stat")
                            if artifact_id and main_stat:
                                slot = ITEM_DATA.get(artifact_id, {}).get("slot")
                                if slot:
                                    stat_name = list(main_stat.keys())[0]
                                    data["growth_key"] = f"{slot}_{stat_name}"
                                    print(f"Восстановлен growth_key для артефакта {artifact_id}: {data['growth_key']}")
                    char.weapon_data = saved.get("weapon_data", {})
            print("Прогресс партии загружен")

        # 1. Попытка загрузить основной файл
        try:
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if self._validate_party_data(data):
                    chars_data = self._extract_chars_data(data)
                    apply_data(chars_data)
                    self.modified = False
                    return
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # 2. Попытка загрузить бэкап
        backup_file = filename + ".backup"
        try:
            if os.path.exists(backup_file) and os.path.getsize(backup_file) > 0:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if self._validate_party_data(data):
                    chars_data = self._extract_chars_data(data)
                    apply_data(chars_data)
                    self.modified = False
                    print("Загружен бэкап партии")
                    return
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # 3. Если ничего не вышло
        print("Файл партии повреждён, используются текущие данные")

    def _validate_party_data(self, data):
        # data должен быть словарем с ключом "characters"
        if not isinstance(data, dict):
            return False
        if "characters" not in data:
            return False
        chars = data["characters"]
        if not isinstance(chars, list):
            return False
        if len(chars) == 0:
            return False

        for char_data in chars:
            if not isinstance(char_data, dict):
                return False
            # Проверяем обязательные поля (их наличие, тип)
            required_fields = ["name", "level", "max_level", "exp", "exp_next",
                               "base_hp", "base_atk", "base_defense", "crit_rate",
                               "crit_dmg", "energy_recharge", "elemental_mastery",
                               "phys_bonus", "resistance", "speed", "talents",
                               "constellation", "weapon", "artifacts", "artifact_data",
                               "weapon_data"]
            for field in required_fields:
                if field not in char_data:
                    return False
        return True

    def _extract_chars_data(self, data):
        # Извлекает список персонажей из data (поддерживает старый формат)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "characters" in data:
            return data["characters"]
        else:
            return []