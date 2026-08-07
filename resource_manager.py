import pygame

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.fonts = {}
        #self.sounds = {}

    def load_image(self, path, key):
        try:
            self.images[key] = pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            surf = pygame.Surface((100, 100))
            surf.fill((255, 0, 255))
            self.images[key] = surf

    def get_image(self, key):
        return self.images.get(key, None)

    def load_font(self, path, size, key):
        try:
            self.fonts[key] = pygame.font.Font(path, size)
        except (pygame.error, FileNotFoundError):
            self.fonts[key] = None

    def get_font(self, key):
        return self.fonts.get(key, None)

    def load_all(self):
        # ---- Тайлы ----
        self.load_image("assets/textures/tiles/Grass_1.png", "grass_1")

        # ---- Предметы ----
        self.load_image("assets/textures/items/Oak_wood_item.png", "oak_wood")

        # ---- Кнопки ----
        self.load_image("assets/textures/buttons/Button_activate.png", "button_activate")
        self.load_image("assets/textures/buttons/Button_artifacts.png", "button_artifacts")
        self.load_image("assets/textures/buttons/Button_change.png", "button_change")
        self.load_image("assets/textures/buttons/Button_characteristic.png", "button_characteristic")
        self.load_image("assets/textures/buttons/Button_constellations.png", "button_constellations")
        self.load_image("assets/textures/buttons/Button_elevate.png", "button_elevate")
        self.load_image("assets/textures/buttons/Button_elevation.png", "button_elevation")
        self.load_image("assets/textures/buttons/Button_equip.png", "button_equip")
        self.load_image("assets/textures/buttons/Button_improve.png", "button_improve")
        self.load_image("assets/textures/buttons/Button_improvement.png", "button_improvement")
        self.load_image("assets/textures/buttons/Button_talents.png", "button_talents")
        self.load_image("assets/textures/buttons/Button_weapon.png", "button_weapon")

        # ---- Артефакты ----
        self.load_image("assets/textures/artifacts/Flower_2.png", "flower_2")
        self.load_image("assets/textures/artifacts/Goblet_2.png", "goblet_2")
        self.load_image("assets/textures/artifacts/Plume_2.png", "plume_2")
        self.load_image("assets/textures/artifacts/Sands_2.png", "sands_2")

        self.load_image("assets/textures/artifacts/Plume_1.png", "plume_1")

        # ---- Оружия ----
        self.load_image("assets/textures/weapons/Rusted_sword.png", "rusted_sword")
        self.load_image("assets/textures/weapons/Sword_of_steel.png", "sword_of_steel")

        # ---- Меню персонажей (портреты) ----
        self.load_image("assets/textures/characters_menu/characters_portraits/GG.png", "gg")

        # ---- Меню персонажей (ГГ) ----
        self.load_image("assets/textures/characters_menu/GG/GG_artifacts.png", "gg_artifacts")