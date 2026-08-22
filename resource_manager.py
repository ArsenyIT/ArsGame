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
        self.load_image("assets/textures/tiles/Grass_2.png", "grass_2")
        self.load_image("assets/textures/tiles/Border_1.png", "border_1")
        self.load_image("assets/textures/tiles/Border_2.png", "border_2")
        self.load_image("assets/textures/tiles/Border_3.png", "border_3")
        self.load_image("assets/textures/tiles/Border_4.png", "border_4")
        self.load_image("assets/textures/tiles/Border_square_1.png", "border_square_1")
        self.load_image("assets/textures/tiles/Border_square_2.png", "border_square_2")
        self.load_image("assets/textures/tiles/Border_square_3.png", "border_square_3")
        self.load_image("assets/textures/tiles/Border_square_4.png", "border_square_4")
        self.load_image("assets/textures/tiles/Border_angel_1.png", "border_angel_1")
        self.load_image("assets/textures/tiles/Border_angel_2.png", "border_angel_2")
        self.load_image("assets/textures/tiles/Border_angel_3.png", "border_angel_3")
        self.load_image("assets/textures/tiles/Border_angel_4.png", "border_angel_4")
        self.load_image("assets/textures/tiles/Border_middle.png", "border_middle")
        self.load_image("assets/textures/tiles/Void_1.png", "void_1")
        self.load_image("assets/textures/tiles/Void_2.png", "void_2")
        self.load_image("assets/textures/tiles/Path.png", "path")
        self.load_image("assets/textures/tiles/White.png", "white")

        # ---- Карты ----
        self.load_image("assets/textures/maps/Map_1.png", "map_1")

        # ---- Предметы ----
        self.load_image("assets/textures/items/Oak_wood_item.png", "oak_wood")

        # ---- Кнопки ----
        self.load_image("assets/textures/buttons/Button_activate.png", "button_activate")
        self.load_image("assets/textures/buttons/Button_artifacts.png", "button_artifacts")
        self.load_image("assets/textures/buttons/Button_change.png", "button_change")
        self.load_image("assets/textures/buttons/Button_change_2.png", "button_change_2")
        self.load_image("assets/textures/buttons/Button_characteristic.png", "button_characteristic")
        self.load_image("assets/textures/buttons/Button_constellations.png", "button_constellations")
        self.load_image("assets/textures/buttons/Button_elevate.png", "button_elevate")
        self.load_image("assets/textures/buttons/Button_elevation.png", "button_elevation")
        self.load_image("assets/textures/buttons/Button_equip.png", "button_equip")
        self.load_image("assets/textures/buttons/Button_equip_2.png", "button_equip_2")
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

        # ---- Меню персонажей (Портреты) ----
        self.load_image("assets/textures/characters_menu/characters_portraits/GG.png", "gg")

        # ---- Меню персонажей (ГГ) ----
        self.load_image("assets/textures/characters_menu/GG/GG_artifacts.png", "gg_artifacts")
        self.load_image("assets/textures/characters_menu/GG/GG_constellations.png", "gg_constellations")
        self.load_image("assets/textures/characters_menu/GG/GG_menu.png", "gg_menu")
        self.load_image("assets/textures/characters_menu/GG/GG_talents.png", "gg_talents")
        self.load_image("assets/textures/characters_menu/GG/GG_upgrade.png", "gg_upgrade")
        self.load_image("assets/textures/characters_menu/GG/GG_weapon.png", "gg_weapon")

        # ---- Меню персонажей (Предметы) ----
        self.load_image("assets/textures/characters_menu/items/Oak_wood_menu_GG.png", "oak_wood_menu_gg")
        self.load_image("assets/textures/characters_menu/items/Story_of_the_Almighty_menu_GG.png", "story_of_the_almighty_menu_gg")

        # ---- Инвентарь (Артефакты) ----
        self.load_image("assets/textures/inventory/artifact_cell/Flower_2_inventory.png", "flower_2_inventory")
        self.load_image("assets/textures/inventory/artifact_cell/Plume_2_inventory.png", "plume_2_inventory")
        self.load_image("assets/textures/inventory/artifact_cell/Sands_2_inventory.png", "sands_2_inventory")
        self.load_image("assets/textures/inventory/artifact_cell/Goblet_2_inventory.png", "goblet_2_inventory")

        self.load_image("assets/textures/inventory/artifact_cell/Plume_1_inventory.png", "plume_1_inventory")

        # ---- Инвентарь (Иконки) ----
        self.load_image("assets/textures/inventory/icons/Icon_artifacts.png", "icon_artifacts")
        self.load_image("assets/textures/inventory/icons/Icon_foods.png", "icon_foods")
        self.load_image("assets/textures/inventory/icons/Icon_potions.png", "icon_potions")
        self.load_image("assets/textures/inventory/icons/Icon_rare_resources.png", "icon_rare_resources")
        self.load_image("assets/textures/inventory/icons/Icon_resources.png", "icon_resources")
        self.load_image("assets/textures/inventory/icons/Icon_special_tools.png", "icon_special_tools")
        self.load_image("assets/textures/inventory/icons/Icon_weapons.png", "icon_weapons")

        # ---- Инвентарь (Оружия) ----
        self.load_image("assets/textures/inventory/weapon_cell/Rusted_sword_inventory.png", "rusted_sword_inventory")
        self.load_image("assets/textures/inventory/weapon_cell/Sword_of_steel_inventory.png", "sword_of_steel_inventory")

        # ---- Инвентарь (Меню) ----
        self.load_image("assets/textures/inventory/menu_inventory/Menu_inventory_1.png", "menu_inventory_1")
        self.load_image("assets/textures/inventory/menu_inventory/Menu_inventory_2.png", "menu_inventory_2")

        # ---- Инвентарь ----
        self.load_image("assets/textures/inventory/Artifact_exp_inventory.png", "artifact_exp_inventory")
        self.load_image("assets/textures/inventory/Cell_inventory.png", "cell_inventory")
        self.load_image("assets/textures/inventory/Crystal_of_true_power_inventory.png", "crystall_of_true_inventory")
        self.load_image("assets/textures/inventory/Hero_duplicate_inventory.png", "Hero_duplicate_inventory")
        self.load_image("assets/textures/inventory/Oak_wood_inventory.png", "oak_wood_inventory")
        self.load_image("assets/textures/inventory/Story_of_the_Almighty_inventory.png", "story_of_the_almighty_inventory")
        self.load_image("assets/textures/inventory/Talent_book_2_inventory.png", "talent_book_2_inventory")

        # ---- Персонажи (ГГ стоя) ----
        self.load_image("assets/textures/characters/GG/stand/GG_left_1.png", "gg_left_1")
        self.load_image("assets/textures/characters/GG/stand/GG_left_2.png", "gg_left_2")
        self.load_image("assets/textures/characters/GG/stand/GG_back_1.png", "gg_back_1")
        self.load_image("assets/textures/characters/GG/stand/GG_back_2.png", "gg_back_2")
        self.load_image("assets/textures/characters/GG/stand/GG_right_1.png", "gg_right_1")
        self.load_image("assets/textures/characters/GG/stand/GG_right_2.png", "gg_right_2")
        self.load_image("assets/textures/characters/GG/stand/GG_straight_1.png", "gg_straight_1")
        self.load_image("assets/textures/characters/GG/stand/GG_straight_2.png", "gg_straight_2")

        # ---- Персонажи (ГГ идя) ----
        self.load_image("assets/textures/characters/GG/go/GG_goes_left_1.png", "gg_goes_left_1")
        self.load_image("assets/textures/characters/GG/go/GG_goes_left_2.png", "gg_goes_left_2")
        self.load_image("assets/textures/characters/GG/go/GG_goes_left_3.png", "gg_goes_left_3")
        self.load_image("assets/textures/characters/GG/go/GG_goes_left_4.png", "gg_goes_left_4")
        self.load_image("assets/textures/characters/GG/go/GG_goes_back_1.png", "gg_goes_back_1")
        self.load_image("assets/textures/characters/GG/go/GG_goes_back_2.png", "gg_goes_back_2")
        self.load_image("assets/textures/characters/GG/go/GG_goes_back_3.png", "gg_goes_back_3")
        self.load_image("assets/textures/characters/GG/go/GG_goes_back_4.png", "gg_goes_back_4")
        self.load_image("assets/textures/characters/GG/go/GG_goes_right_1.png", "gg_goes_right_1")
        self.load_image("assets/textures/characters/GG/go/GG_goes_right_2.png", "gg_goes_right_2")
        self.load_image("assets/textures/characters/GG/go/GG_goes_right_3.png", "gg_goes_right_3")
        self.load_image("assets/textures/characters/GG/go/GG_goes_right_4.png", "gg_goes_right_4")
        self.load_image("assets/textures/characters/GG/go/GG_goes_straight_1.png", "gg_goes_straight_1")
        self.load_image("assets/textures/characters/GG/go/GG_goes_straight_2.png", "gg_goes_straight_2")
        self.load_image("assets/textures/characters/GG/go/GG_goes_straight_3.png", "gg_goes_straight_3")
        self.load_image("assets/textures/characters/GG/go/GG_goes_straight_4.png", "gg_goes_straight_4")

        # ---- Остатки ----
        self.load_image("assets/textures/Dialog_box.png", "dialog_box")
        self.load_image("assets/textures/Popup.png", "popup")
        self.load_image("assets/textures/Squad_list.png", "squad_list")

        # ---- Иконка ----
        self.load_image("assets/textures/icon/Icon.png", "icon")