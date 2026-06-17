import pygame
from inventory import Inventory

class Player:
    def __init__(self):
        self.inventory = Inventory()
        self.inventory.load("assets/data/inventory.json")