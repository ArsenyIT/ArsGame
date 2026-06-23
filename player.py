import pygame
from inventory import Inventory
from game_data import Character

class Player:
    def __init__(self):
        self.inventory = Inventory()
        self.inventory.load("assets/data/inventory.json")

        hero = Character(
            name="Арсений",
            exp=0,
            exp_next=100,
            base_hp=670,
            base_atk=105,
            base_defense=300,
            crit_rate=5,
            crit_dmg=150,
            energy_recharge=100,
            elemental_mastery=10,
            phys_bonus=0,
            resistance=1,
            speed=10
        )
        self.party = [hero]