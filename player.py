import pygame
from inventory import Inventory
from game_data import Character
import json
import os

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
        self.load_party("assets/data/party_save.json")
        self.modified = False

    def mark_modified(self):
        self.modified = True


    def save_party(self, filename):
        #Сохраняет данные всех персонажей в JSON
        data = []
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
                # weapon и artifacts пока не реализованы, сохраняем как None
                "weapon": None,
                "artifacts": char.artifacts,
                "artifact_data": char.artifact_data
            }
            data.append(char_data)
        # Создаём папку, если её нет
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.modified = False
        print("Партия сохранена")

    def load_party(self, filename):
        # Загружает сохранённые данные и обновляет персонажей
        if os.path.exists(filename):
            # Проверяем, что файл не пустой
            if os.path.getsize(filename) > 0:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for i, char in enumerate(self.party):
                    if i < len(data):
                        saved = data[i]
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
                        char.artifacts = saved.get("artifacts", char.artifacts)
                        char.artifact_data = saved.get("artifact_data", {})
                    # weapon пока пропускаем
                print("Прогресс партии загружен")
            else:
                print("Файл партии пуст, создаю новый")
                # Можно создать пустой список или ничего не делать
        else:
            print("Файл партии не найден, создаю новый")