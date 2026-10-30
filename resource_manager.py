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
        self.load_image(resource_path("assets/textures/tiles/White.png"), "white")
            # ---- Трава ----
        self.load_image(resource_path("assets/textures/tiles/grass/Grass_1.png"), "grass_1")
        self.load_image(resource_path("assets/textures/tiles/grass/Grass_2.png"), "grass_2")
        self.load_image(resource_path("assets/textures/tiles/grass/Forest_grass.png"), "forest_grass")
        self.load_image(resource_path("assets/textures/tiles/grass/Grass_with_flowers.png"), "grass_with_flowers")
            # ---- Граница ----
        self.load_image(resource_path("assets/textures/tiles/border/Border_1.png"), "border_1")
        self.load_image(resource_path("assets/textures/tiles/border/Border_2.png"), "border_2")
        self.load_image(resource_path("assets/textures/tiles/border/Border_3.png"), "border_3")
        self.load_image(resource_path("assets/textures/tiles/border/Border_4.png"), "border_4")
        self.load_image(resource_path("assets/textures/tiles/border/Border_square_1.png"), "border_square_1")
        self.load_image(resource_path("assets/textures/tiles/border/Border_square_2.png"), "border_square_2")
        self.load_image(resource_path("assets/textures/tiles/border/Border_square_3.png"), "border_square_3")
        self.load_image(resource_path("assets/textures/tiles/border/Border_square_4.png"), "border_square_4")
        self.load_image(resource_path("assets/textures/tiles/border/Border_angel_1.png"), "border_angel_1")
        self.load_image(resource_path("assets/textures/tiles/border/Border_angel_2.png"), "border_angel_2")
        self.load_image(resource_path("assets/textures/tiles/border/Border_angel_3.png"), "border_angel_3")
        self.load_image(resource_path("assets/textures/tiles/border/Border_angel_4.png"), "border_angel_4")
        self.load_image(resource_path("assets/textures/tiles/border/Border_middle.png"), "border_middle")
            # ---- Пустота ----
        self.load_image(resource_path("assets/textures/tiles/void/Void_1.png"), "void_1")
        self.load_image(resource_path("assets/textures/tiles/void/Void_2.png"), "void_2")
            # ---- Тропинка ----
        self.load_image(resource_path("assets/textures/tiles/path/Path.png"), "path")
                # ---- С обычной травой ----
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_1.png"), "path_with_grass_1")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_2.png"), "path_with_grass_2")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_3.png"), "path_with_grass_3")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_4.png"), "path_with_grass_4")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_angle_1.png"), "path_with_grass_angle_1")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_angle_2.png"), "path_with_grass_angle_2")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_angle_3.png"), "path_with_grass_angle_3")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_angle_4.png"), "path_with_grass_angle_4")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_rim_1.png"), "path_with_grass_rim_1")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_rim_2.png"), "path_with_grass_rim_2")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_rim_3.png"), "path_with_grass_rim_3")
        self.load_image(resource_path("assets/textures/tiles/path/grass/Path_with_grass_rim_4.png"), "path_with_grass_rim_4")
                # ---- С лесной травой ----
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_1.png"), "path_with_forest_grass_1")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_2.png"), "path_with_forest_grass_2")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_3.png"), "path_with_forest_grass_3")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_4.png"), "path_with_forest_grass_4")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_angle_1.png"), "path_with_forest_grass_angle_1")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_angle_2.png"), "path_with_forest_grass_angle_2")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_angle_3.png"), "path_with_forest_grass_angle_3")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_angle_4.png"), "path_with_forest_grass_angle_4")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_rim_1.png"), "path_with_forest_grass_rim_1")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_rim_2.png"), "path_with_forest_grass_rim_2")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_rim_3.png"), "path_with_forest_grass_rim_3")
        self.load_image(resource_path("assets/textures/tiles/path/forest_grass/Path_with_forest_grass_rim_4.png"), "path_with_forest_grass_rim_4")
            # ---- Вода ----
        self.load_image(resource_path("assets/textures/tiles/water/Water_1_level.png"), "water_1_level")
        self.load_image(resource_path("assets/textures/tiles/water/Water_2_level.png"), "water_2_level")
        self.load_image(resource_path("assets/textures/tiles/water/Water_3_level.png"), "water_3_level")
        self.load_image(resource_path("assets/textures/tiles/water/Water_4_level.png"), "water_4_level")

        # ---- Объекты коллизии ----
        self.load_image(resource_path("assets/textures/collision_objects/Oak_butt.png"), "oak_butt")
            # ---- Дом ----
        self.load_image(resource_path("assets/textures/collision_objects/GG_house.png"), "gg_house")
        self.load_image(resource_path("assets/textures/collision_objects/Neighbour_house.png"), "neighbour_house")
            # ---- Забор ----
        self.load_image(resource_path("assets/textures/collision_objects/fence/GG_fence_wall.png"), "gg_fence_wall")
        self.load_image(resource_path("assets/textures/collision_objects/fence/GG_fence_left_wall.png"), "gg_fence_left_wall")
        self.load_image(resource_path("assets/textures/collision_objects/fence/GG_fence_right_wall.png"), "gg_fence_right_wall")
        self.load_image(resource_path("assets/textures/collision_objects/fence/GG_fence_left_angle.png"), "gg_fence_left_angle")
        self.load_image(resource_path("assets/textures/collision_objects/fence/GG_fence_right_angle.png"), "gg_fence_right_angle")
            # ---- Сундуки ----
        self.load_image(resource_path("assets/textures/collision_objects/chests/Old_chest.png"), "old_chest")
        self.load_image(resource_path("assets/textures/collision_objects/chests/Chest.png"), "chest")
        self.load_image(resource_path("assets/textures/collision_objects/chests/Big_chest.png"), "big_chest")

        # ---- Объекты поверх персонажа ----
        self.load_image(resource_path("assets/textures/overlay/Oak.png"), "oak")

        # ---- Карты ----
        self.load_image(resource_path("assets/textures/maps/Map_1.png"), "map_1")

        # ---- Предметы ----
        self.load_image(resource_path("assets/textures/items/Oak_wood.png"), "oak_wood")
        self.load_image(resource_path("assets/textures/items/Poppy.png"), "poppy")
        self.load_image(resource_path("assets/textures/items/Chamomile.png"), "chamomile")

        # ---- Кнопки ----
            # ---- Мир ----
        self.load_image(resource_path("assets/textures/buttons/world/World_button_collect.png"), "world_button_collect")
            # ---- ГГ ----
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
            # ---- Заражение ----
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
        self.load_image(resource_path("assets/textures/artifacts/Plume_1.png"), "plume_1")
            # ---- Бархатное господство ----
        self.load_image(resource_path("assets/textures/artifacts/velvety_dominance/Flower_2.png"), "flower_2")
        self.load_image(resource_path("assets/textures/artifacts/velvety_dominance/Goblet_2.png"), "goblet_2")
        self.load_image(resource_path("assets/textures/artifacts/velvety_dominance/Plume_2.png"), "plume_2")
        self.load_image(resource_path("assets/textures/artifacts/velvety_dominance/Sands_2.png"), "sands_2")

        # ---- Оружия ----
        self.load_image(resource_path("assets/textures/weapons/Rusted_sword.png"), "rusted_sword")
        self.load_image(resource_path("assets/textures/weapons/Sword_of_steel.png"), "sword_of_steel")

        # ---- Меню персонажей ----
            # ---- Портреты ----
        self.load_image(resource_path("assets/textures/characters_menu/characters_portraits/GG.png"), "gg")
        self.load_image(resource_path("assets/textures/characters_menu/characters_portraits/Infection.png"), "infection")
            # ---- ГГ ----
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_artifacts.png"), "gg_artifacts")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_symbolism.png"), "gg_symbolism")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_menu.png"), "gg_menu")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_talents.png"), "gg_talents")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_upgrade.png"), "gg_upgrade")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_weapon.png"), "gg_weapon")
        self.load_image(resource_path("assets/textures/characters_menu/GG/Popup.png"), "gg_popup")
        self.load_image(resource_path("assets/textures/characters_menu/GG/GG_popup_weapon.png"), "gg_popup_weapon")
            # ---- Заражение ----
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_artifacts.png"), "infection_artifacts")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_symbolism.png"), "infection_symbolism")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_menu.png"), "infection_menu")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_talents.png"), "infection_talents")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_upgrade.png"), "infection_upgrade")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Infection_weapon.png"), "infection_weapon")
        self.load_image(resource_path("assets/textures/characters_menu/Infection/Popup.png"), "infection_popup")
            # ---- Предметы ----
        self.load_image(resource_path("assets/textures/characters_menu/items/Oak_wood_menu_GG.png"), "oak_wood_menu_gg")
        self.load_image(resource_path("assets/textures/characters_menu/items/Story_of_the_Almighty_menu_GG.png"), "story_of_the_almighty_menu_gg")
            # ---- Иконки ----
        self.load_image(resource_path("assets/textures/characters_menu/icons/type_damage/Phys_damage_type.png"), "phys_damage_type")
        self.load_image(resource_path("assets/textures/characters_menu/icons/type_weapon/One_handed_sword.png"), "one_handed_sword")

        # ---- Инвентарь ----
        self.load_image(resource_path("assets/textures/inventory/Cell_inventory.png"), "cell_inventory")
            # ---- Артефакты ----
        self.load_image(resource_path("assets/textures/inventory/artifact_cell/Plume_1_inventory.png"), "plume_1_inventory")
                # ---- Бархатное господство ----
        self.load_image(resource_path("assets/textures/inventory/artifact_cell/velvety_dominance/Flower_2_inventory.png"), "flower_2_inventory")
        self.load_image(resource_path("assets/textures/inventory/artifact_cell/velvety_dominance/Plume_2_inventory.png"), "plume_2_inventory")
        self.load_image(resource_path("assets/textures/inventory/artifact_cell/velvety_dominance/Sands_2_inventory.png"), "sands_2_inventory")
        self.load_image(resource_path("assets/textures/inventory/artifact_cell/velvety_dominance/Goblet_2_inventory.png"), "goblet_2_inventory")
            # ---- Иконки ----
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_artifacts.png"), "icon_artifacts")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_foods.png"), "icon_foods")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_potions.png"), "icon_potions")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_rare_resources.png"), "icon_rare_resources")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_resources.png"), "icon_resources")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_special_tools.png"), "icon_special_tools")
        self.load_image(resource_path("assets/textures/inventory/icons/Icon_weapons.png"), "icon_weapons")
            # ---- Оружия ----
        self.load_image(resource_path("assets/textures/inventory/weapon_cell/Rusted_sword_inventory.png"), "rusted_sword_inventory")
        self.load_image(resource_path("assets/textures/inventory/weapon_cell/Sword_of_steel_inventory.png"), "sword_of_steel_inventory")
            # ---- Меню ----
        self.load_image(resource_path("assets/textures/inventory/menu_inventory/Menu_inventory_1.png"), "menu_inventory_1")
        self.load_image(resource_path("assets/textures/inventory/menu_inventory/Menu_inventory_2.png"), "menu_inventory_2")
            # ---- Часть символики ----
        self.load_image(resource_path("assets/textures/inventory/Hero_duplicate_inventory.png"),"hero_duplicate_inventory")
            # ---- Эликсир ----
        self.load_image(resource_path("assets/textures/inventory/elixir/Magic_elixir_inventory.png"), "magic_elixir_inventory")
        self.load_image(resource_path("assets/textures/inventory/elixir/Concentrated_elixir_of_secret_magic_inventory.png"), "concentrated_elixir_of_secret_magic_inventory")
        self.load_image(resource_path("assets/textures/inventory/elixir/Highly_concentrated_forbidden_magic_inventory.png"), "highly_concentrated_forbidden_magic_inventory")
            # ---- Кристалл ----
        self.load_image(resource_path("assets/textures/inventory/crystal/Electrified_crystal_fragments_inventory.png"), "electrified_crystal_fragments_inventory")
        self.load_image(resource_path("assets/textures/inventory/crystal/Charged_crystal_fragment_inventory.png"), "charged_crystal_fragment_inventory")
        self.load_image(resource_path("assets/textures/inventory/crystal/Crystal_of_true_power_inventory.png"), "crystal_of_true_power_inventory_inventory")
            # ---- Рукописи ----
        self.load_image(resource_path("assets/textures/inventory/manuscripts/Notes_for_beginner_inventory.png"), "notes_for_beginner_inventory")
        self.load_image(resource_path("assets/textures/inventory/manuscripts/Guide_for_the_experienced_traveler_inventory.png"), "guide_for_the_experienced_traveler_inventory")
        self.load_image(resource_path("assets/textures/inventory/manuscripts/Story_of_the_Almighty_inventory.png"), "story_of_the_almighty_inventory")
            # ---- Книги талантов ----
                # ---- Книги по фехтованию ----
        self.load_image(resource_path("assets/textures/inventory/talents_book/fencing_book/Collection_fencing_exercises_inventory.png"), "collection_fencing_exercises_inventory")
        self.load_image(resource_path("assets/textures/inventory/talents_book/fencing_book/Fencing_textbook_inventory.png"), "fencing_textbook_inventory")
        self.load_image(resource_path("assets/textures/inventory/talents_book/fencing_book/Notes_fencing_master_inventory.png"), "notes_fencing_master_inventory")
            # ---- Предметы ----
        self.load_image(resource_path("assets/textures/inventory/items/Poppy_inventory.png"), "poppy_inventory")
        self.load_image(resource_path("assets/textures/inventory/items/Chamomile_inventory.png"), "chamomile_inventory")
        self.load_image(resource_path("assets/textures/inventory/items/Oak_wood_inventory.png"), "oak_wood_inventory")

        # ---- Персонажи ----
            # ---- ГГ ----
                # ---- Стоя ----
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_left_1.png"), "gg_left_1")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_left_2.png"), "gg_left_2")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_back_1.png"), "gg_back_1")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_back_2.png"), "gg_back_2")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_right_1.png"), "gg_right_1")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_right_2.png"), "gg_right_2")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_straight_1.png"), "gg_straight_1")
        self.load_image(resource_path("assets/textures/characters/GG/stand/GG_straight_2.png"), "gg_straight_2")
                # ---- Ходьба ----
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

        # ---- Диалог ----
        self.load_image(resource_path("assets/textures/Dialog_box.png"), "dialog_box")

        # ---- Отряд ----
        self.load_image(resource_path("assets/textures/Squad_list.png"), "squad_list")

        # ---- Иконка ----
        self.load_image(resource_path("assets/textures/icon/Icon.png"), "icon")