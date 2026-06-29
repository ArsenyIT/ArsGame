import pygame
from inventory import Inventory
from game_data import Character
import json
import os
from game_data import generate_artifact_main_stat

class Player:
    def __init__(self):
        self.inventory = Inventory()
        self.inventory.load("assets/data/inventory.json")
        self.artifact_inventory = []  # список ID артефактов (уникальных)
        self.weapon_inventory = []  # список ID оружия (уникальных)

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

        self.load_party("assets/data/party_save.json")
        self.modified = False

    def mark_modified(self):
        self.modified = True

    def save_party(self, filename):
        # Сохраняем данные персонажей
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
            }
            chars_data.append(char_data)
        # Общие данные игрока
        full_data = {
            "characters": chars_data,
            "artifact_inventory": self.artifact_inventory,
            "weapon_inventory": self.weapon_inventory,
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
            # Если данные — список (старый формат), преобразуем в новый
            if isinstance(data, list):
                chars_data = data
                full_data = {
                    "characters": chars_data,
                    "artifact_inventory": [],
                    "weapon_inventory": []
                }
            else:
                full_data = data
            # Загружаем персонажей
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
                    # Проверяем наличие основного стата
                    for art_id, data in char.artifact_data.items():
                        if "main_stat" not in data:
                            main_stat = generate_artifact_main_stat(art_id)
                            if main_stat:
                                data["main_stat"] = main_stat
            # Загружаем инвентари
            self.artifact_inventory = full_data.get("artifact_inventory", [])
            self.weapon_inventory = full_data.get("weapon_inventory", [])
            print("Прогресс партии загружен")
        else:
            print("Файл партии не найден или пуст")

    def add_artifact(self, artifact_id):
        # Создаёт новый артефакт со случайными статами и добавляет в инвентарь
        # Генерируем основной стат
        main_stat = generate_artifact_main_stat(artifact_id)
        if not main_stat:
            return False
        # Создаём запись в artifact_data (для хранения уровня и субстатов)
        # Используем hero (первого персонажа) как владельца данных
        hero = self.party[0]
        # Генерируем уникальный ключ (можно использовать время или счётчик)
        import time
        unique_id = f"{artifact_id}_{int(time.time() * 1000)}_{len(self.artifact_inventory)}"
        hero.artifact_data[unique_id] = {
            "level": 0,
            "sub_stats": [],
            "main_stat": main_stat,
            "artifact_id": artifact_id  # ссылка на шаблон
        }
        self.artifact_inventory.append(unique_id)
        print(f"Добавлен артефакт {artifact_id} с ID {unique_id}")
        return True

    def remove_artifact(self, unique_id):
        # Удаляет артефакт из инвентаря (при экипировке)
        if unique_id in self.artifact_inventory:
            self.artifact_inventory.remove(unique_id)
            return True
        return False

    def add_weapon(self, weapon_id):
        # Аналогично для оружия
        hero = self.party[0]
        import time
        unique_id = f"{weapon_id}_{int(time.time() * 1000)}_{len(self.weapon_inventory)}"
        # Для оружия пока храним только уровень (можно расширить позже)
        hero.weapon_data = hero.weapon_data or {}
        hero.weapon_data[unique_id] = {
            "level": 1,
            "weapon_id": weapon_id
        }
        self.weapon_inventory.append(unique_id)
        return True