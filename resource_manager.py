import pygame
from utils import resource_path

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.fonts = {}

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
        self.load_image(resource_path("assets/textures/tiles/Grass_1.png"), "grass_1")
        self.load_image(resource_path("assets/textures/tiles/Grass_2.png"), "grass_2")
        self.load_image(resource_path("assets/textures/tiles/Forest_grass.png"), "forest_grass")
        self.load_image(resource_path("assets/textures/tiles/Border_1.png"), "border_1")
        self.load_image(resource_path("assets/textures/tiles/Border_2.png"), "border_2")
        self.load_image(resource_path("assets/textures/tiles/Border_3.png"), "border_3")
        self.load_image(resource_path("assets/textures/tiles/Border_4.png"), "border_4")
        self.load_image(resource_path("assets/textures/tiles/Border_square_1.png"), "border_square_1")
        self.load_image(resource_path("assets/textures/tiles/Border_square_2.png"), "border_square_2")
        self.load_image(resource_path("assets/textures/tiles/Border_square_3.png"), "border_square_3")
        self.load_image(resource_path("assets/textures/tiles/Border_square_4.png"), "border_square_4")
        self.load_image(resource_path("assets/textures/tiles/Border_angel_1.png"), "border_angel_1")
        self.load_image(resource_path("assets/textures/tiles/Border_angel_2.png"), "border_angel_2")
        self.load_image(resource_path("assets/textures/tiles/Border_angel_3.png"), "border_angel_3")
        self.load_image(resource_path("assets/textures/tiles/Border_angel_4.png"), "border_angel_4")
        self.load_image(resource_path("assets/textures/tiles/Border_middle.png"), "border_middle")
        self.load_image(resource_path("assets/textures/tiles/Void_1.png"), "void_1")
        self.load_image(resource_path("assets/textures/tiles/Void_2.png"), "void_2")
        self.load_image(resource_path("assets/textures/tiles/Path.png"), "path")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_1.png"), "path_with_grass_1")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_2.png"), "path_with_grass_2")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_3.png"), "path_with_grass_3")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_4.png"), "path_with_grass_4")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_angle_1.png"), "path_with_grass_angle_1")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_angle_2.png"), "path_with_grass_angle_2")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_angle_3.png"), "path_with_grass_angle_3")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_angle_4.png"), "path_with_grass_angle_4")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_rim_1.png"), "path_with_grass_rim_1")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_rim_2.png"), "path_with_grass_rim_2")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_rim_3.png"), "path_with_grass_rim_3")
        self.load_image(resource_path("assets/textures/tiles/Path_with_grass_rim_4.png"), "path_with_grass_rim_4")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_1.png"), "path_with_forest_grass_1")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_2.png"), "path_with_forest_grass_2")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_3.png"), "path_with_forest_grass_3")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_4.png"), "path_with_forest_grass_4")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_angle_1.png"), "path_with_forest_grass_angle_1")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_angle_2.png"), "path_with_forest_grass_angle_2")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_angle_3.png"), "path_with_forest_grass_angle_3")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_angle_4.png"), "path_with_forest_grass_angle_4")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_rim_1.png"), "path_with_forest_grass_rim_1")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_rim_2.png"), "path_with_forest_grass_rim_2")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_rim_3.png"), "path_with_forest_grass_rim_3")
        self.load_image(resource_path("assets/textures/tiles/Path_with_forest_grass_rim_4.png"), "path_with_forest_grass_rim_4")
        self.load_image(resource_path("assets/textures/tiles/White.png"), "white")
        self.load_image(resource_path("assets/textures/tiles/water/Water_1_level.png"), "water_1_level")
        self.load_image(resource_path("assets/textures/tiles/water/Water_2_level.png"), "water_2_level")
        self.load_image(resource_path("assets/textures/tiles/water/Water_3_level.png"), "water_3_level")
        self.load_image(resource_path("assets/textures/tiles/water/Water_4_level.png"), "water_4_level")

        # ---- Объекты коллизии ----
        self.load_image(resource_path("assets/textures/collision_objects/Oak_butt.png"), "oak_butt")
        self.load_image(resource_path("assets/textures/collision_objects/GG_house.png"), "gg_house")
        self.load_image(resource_path("assets/textures/collision_objects/Neighbour_house.png"), "neighbour_house")
        self.load_image(resource_path("assets/textures/collision_objects/fence/Fence_wall.png"), "fence_wall")
        self.load_image(resource_path("assets/textures/collision_objects/fence/Fence_left_wall.png"), "fence_left_wall")
        self.load_image(resource_path("assets/textures/collision_objects/fence/Fence_right_wall.png"), "fence_right_wall")
        self.load_image(resource_path("assets/textures/collision_objects/fence/Fence_left_angle.png"), "fence_left_angle")
        self.load_image(resource_path("assets/textures/collision_objects/fence/Fence_right_angle.png"), "fence_right_angle")
        self.load_image(resource_path("assets/textures/collision_objects/chests/Old_chest.png"), "old_chest")
        self.load_image(resource_path("assets/textures/collision_objects/chests/Chest.png"), "chest")
        self.load_image(resource_path("assets/textures/collision_objects/chests/Big_chest.png"), "big_chest")

        # ---- Объекты поверх персонажа ----
        self.load_image(resource_path("assets/textures/overlay/Oak.png"), "oak")

        # ---- Карты ----
        self.load_image(resource_path("assets/textures/maps/Map_1.png"), "map_1")

        # ---- Предметы ----
        self.load_image(resource_path("assets/textures/items/Oak_wood_item.png"), "oak_wood")

        # ---- Кнопки (ГГ) ----
        self.load_image(resource_path("assets/textures/buttons/GG/Button_activate.png"), "button_activate_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_artifacts.png"), "button_artifacts_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_change.png"), "button_change_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_change_2.png"), "button_change_2_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_characteristic.png"), "button_characteristic_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_symbolism.png"), "button_symbolism_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_elevate.png"), "button_elevate_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_elevation.png"), "button_elevation_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_equip.png"), "button_equip_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_equip_2.png"), "button_equip_2_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_improve.png"), "button_improve_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_improvement.png"), "button_improvement_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_talents.png"), "button_talents_gg")
        self.load_image(resource_path("assets/textures/buttons/GG/Button_weapon.png"), "button_weapon_gg")

        # ---- Кнопки (Заражение) ----
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_activate.png"), "button_activate_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_artifacts.png"), "button_artifacts_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_change.png"), "button_change_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_change_2.png"), "button_change_2_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_characteristic.png"), "button_characteristic_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_symbolism.png"), "button_symbolism_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_elevate.png"), "button_elevate_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_elevation.png"), "button_elevation_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_equip.png"), "button_equip_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_equip_2.png"), "button_equip_2_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_improve.png"), "button_improve_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_improvement.png"), "button_improvement_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection/Button_talents.png"), "button_talents_infection")
        self.load_image(resource_path("assets/textures/buttons/Infection//Button_weapon.png"), "button_weapon_infection")

        # ---- Артефакты ----
        self.load_image(resource_path("assets/textures/artifacts/Flower_2.png"), "flower_2")
        self.load_image(resource_path("assets/textures/artifacts/Goblet_2.png"), "goblet_2")
        self.load_image(resource_path("assets/textures/artifacts/Plume_2.png"), "plume_2")
        self.load_image(resource_path("assets/textures/artifacts/Sands_2.png"), "sands_2")

        self.load_image(resource_path("assets/textures/artifacts/Plume_1.png"), "plume_1")

        # ---- Оружия ----
        self.load_image(resource_path("assets/textures/weapons/Rusted_sword.png"), "rusted_sword")
        self.load_image(resource_path("assets/textures/weapons/Sword_of_steel.png"), "sword_of_steel")

        # ---- Меню персонажей (Портреты) ----
        self.load_image(resource_path("assets/textures/characters_menu/characters_portraits/GG.png"), "gg")
        self.load_image(resource_path("assets/textures/characters_menu/characters_portraits/Infection.png"), "infection")

        # ---- Меню персонажей (ГГ) ----
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_artifacts.png"), "gg_artifacts")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_symbolism.png"), "gg_symbolism")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_menu.png"), "gg_menu")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_talents.png"), "gg_talents")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_upgrade.png"), "gg_upgrade")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_weapon.png"), "gg_weapon")
        self.load_image(resource_path("assets/textures/characters_menu/GG/Popup.png"), "gg_popup")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_popup_weapon.png"), "gg_popup_weapon")

        # ---- Меню персонажей (Заражение) ----
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_artifacts.png"), "infection_artifacts")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_symbolism.png"), "infection_symbolism")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_menu.png"), "infection_menu")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_talents.png"), "infection_talents")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_upgrade.png"), "infection_upgrade")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_weapon.png"), "infection_weapon")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Popup.png"), "infection_popup")

        # ---- Меню персонажей (Предметы) ----
        self.load_image(resource_path("assets/textures/characters_menu/items/Oak_wood_menu_GG.png"), "oak_wood_menu_gg")
        self.load_image(resource_path("assets/textures/characters_menu/items/Story_of_the_Almighty_menu_GG.png"), "story_of_the_almighty_menu_gg")

        # ---- Меню персонажей (Иконки) ----
        self.load_image(resource_path("assets/textures/characters_menu/icons/type_damage/Phys_damage_type.png"), "phys_damage_type")
        self.load_image(resource_path("assets/textures/characters_menu/icons/type_weapon/One_handed_sword.png"), "one_handed_sword")

        # ---- Инвентарь (Артефакты) ----
        self.load_image(resource_path("assets/textures/inventory/artifact_cell/Flower_2_inventory.png"), "flower_2_inventory")
        self.load_image(resource_path("assets/textures/inventory/artifact_cell/Plume_2_inventory.png"), "plume_2_inventory")
        self.load_image(resource_path("assets/textures/inventory/artifact_cell/Sands_2_inventory.png"), "sands_2_inventory")
        self.load_image(resource_path("assets/textures/inventory/artifact_cell/Goblet_2_inventory.png"), "goblet_2_inventory")

        self.load_image(resource_path("assets/textures/inventory/artifact_cell/Plume_1_inventory.png"), "plume_1_inventory")

        # ---- Инвентарь (Иконки) ----
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_artifacts.png"), "icon_artifacts")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_foods.png"), "icon_foods")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_potions.png"), "icon_potions")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_rare_resources.png"), "icon_rare_resources")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_resources.png"), "icon_resources")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_special_tools.png"), "icon_special_tools")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_weapons.png"), "icon_weapons")

        # ---- Инвентарь (Оружия) ----
        self.load_image(resource_path("assets/textures/inventory/weapon_cell/Rusted_sword_inventory.png"), "rusted_sword_inventory")
        self.load_image(resource_path("assets/textures/inventory/weapon_cell/Sword_of_steel_inventory.png"), "sword_of_steel_inventory")

        # ---- Инвентарь (Меню) ----
        self.load_image(resource_path("assets/textures/inventory/menu_inventory/Menu_inventory_1.png"), "menu_inventory_1")
        self.load_image(resource_path("assets/textures/inventory/menu_inventory/Menu_inventory_2.png"), "menu_inventory_2")

        # ---- Инвентарь ----
        self.load_image(resource_path("assets/textures/inventory/Artifact_exp_inventory.png"), "artifact_exp_inventory")
        self.load_image(resource_path("assets/textures/inventory/Cell_inventory.png"), "cell_inventory")
        self.load_image(resource_path("assets/textures/inventory/Crystal_of_true_power_inventory.png"), "crystall_of_true_inventory")
        self.load_image(resource_path("assets/textures/inventory/Hero_duplicate_inventory.png"), "Hero_duplicate_inventory")
        self.load_image(resource_path("assets/textures/inventory/Oak_wood_inventory.png"), "oak_wood_inventory")
        self.load_image(resource_path("assets/textures/inventory/Story_of_the_Almighty_inventory.png"), "story_of_the_almighty_inventory")
        self.load_image(resource_path("assets/textures/inventory/Talent_book_2_inventory.png"), "talent_book_2_inventory")

        # ---- Персонажи (ГГ стоя) ----
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_left_1.png"), "gg_left_1")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_left_2.png"), "gg_left_2")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_back_1.png"), "gg_back_1")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_back_2.png"), "gg_back_2")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_right_1.png"), "gg_right_1")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_right_2.png"), "gg_right_2")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_straight_1.png"), "gg_straight_1")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_straight_2.png"), "gg_straight_2")

        # ---- Персонажи (ГГ ходьба) ----
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_left_1.png"), "gg_goes_left_1")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_left_2.png"), "gg_goes_left_2")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_left_3.png"), "gg_goes_left_3")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_left_4.png"), "gg_goes_left_4")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_back_1.png"), "gg_goes_back_1")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_back_2.png"), "gg_goes_back_2")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_back_3.png"), "gg_goes_back_3")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_back_4.png"), "gg_goes_back_4")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_right_1.png"), "gg_goes_right_1")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_right_2.png"), "gg_goes_right_2")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_right_3.png"), "gg_goes_right_3")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_right_4.png"), "gg_goes_right_4")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_straight_1.png"), "gg_goes_straight_1")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_straight_2.png"), "gg_goes_straight_2")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_straight_3.png"), "gg_goes_straight_3")
        self.load_image(resource_path("assets/textures/characters/GG/go/GG_goes_straight_4.png"), "gg_goes_straight_4")

        # ---- Остатки ----
        self.load_image(resource_path("assets/textures/Dialog_box.png"), "dialog_box")
        self.load_image(resource_path("assets/textures/Squad_list.png"), "squad_list")

        # ---- Иконка ----
        self.load_image(resource_path("assets/textures/icon/Icon.png"), "icon")