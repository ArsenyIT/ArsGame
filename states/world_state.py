import pygame
import json
from camera import Camera
from input_handler import InputHandler

class WorldState:
    def __init__(self, game):
        self.game = game
        item_x = int(self.game.WIDTH * 0.15)
        item_y = int(self.game.HEIGHT * 0.3)
        item_width = int(self.game.WIDTH * 0.01)
        item_height = int(self.game.HEIGHT * 0.045)
        self.item_rect = pygame.Rect(item_x, item_y, item_width, item_height)
        self.hint_font = pygame.font.Font(None, 24)
        self.near_item = False
        self.item = True
        self.tile_size = 50
        self.direction = "right"
        self.idle_frames = {
            "back": ["gg_back_1", "gg_back_2"],
            "straight": ["gg_straight_1", "gg_straight_2"],
            "left": ["gg_left_1", "gg_left_2"],
            "right": ["gg_right_1", "gg_right_2"]
        }
        self.walk_frames = {
            "back": ["gg_goes_back_1", "gg_goes_back_2", "gg_goes_back_3", "gg_goes_back_4"],
            "straight": ["gg_goes_straight_1", "gg_goes_straight_2", "gg_goes_straight_3", "gg_goes_straight_4"],
            "left": ["gg_goes_left_1", "gg_goes_left_2", "gg_goes_left_3", "gg_goes_left_4"],
            "right": ["gg_goes_right_1", "gg_goes_right_2", "gg_goes_right_3", "gg_goes_right_4"]
        }
        self.idle_frames_index = 0
        self.walk_frames_index = 0
        self.idle_timer = 0.0
        self.walk_timer = 0.0
        self.idle_interval = 0.5
        self.walk_interval = 0.2
        self.is_moving = False

    def on_enter(self):
        # загрузить карту, спрайты, инициализировать положение игрока
        spawn_tile_x = 140
        spawn_tile_y = 150
        hero_x = spawn_tile_x * self.tile_size
        hero_y = spawn_tile_y * self.tile_size
        hero_width = int(self.game.WIDTH * 0.0329) #45
        hero_height = int(self.game.HEIGHT * 0.12) #90
        self.hero_rect = pygame.Rect(hero_x, hero_y, hero_width, hero_height)
        with open("assets/maps/map.json", "r", encoding="utf-8") as f:
            map_json = json.load(f)
        map_width = map_json["width"] * self.tile_size
        map_height = map_json["height"] * self.tile_size
        self.ground_data = None
        self.collision_data = None
        self.collision_rects = []
        for layer in map_json["layers"]:
            if layer["type"] == "tilelayer":
                if layer["name"] == "Ground":
                    width = map_json["width"]
                    height = map_json["height"]
                    data_2d = [layer["data"][i * width: (i + 1) * width] for i in range(height)]
                    self.ground_data = data_2d
                if layer["name"] == "Collision_tiles":
                    width = map_json["width"]
                    height = map_json["height"]
                    data_2d = [layer["data"][i * width: (i + 1) * width] for i in range(height)]
                    self.collision_data = data_2d
            elif layer["type"] == "objectgroup" and layer["name"] == "Collision_objects":
                for obj in layer["objects"]:
                    rect = pygame.Rect(obj["x"], obj["y"], obj["width"], obj["height"])
                    self.collision_rects.append(rect)

        self.camera = Camera(map_width, map_height, self.tile_size, self.game.WIDTH, self.game.HEIGHT)
        self.tile_textures = {
            1: self.game.resources.get_image("grass_1"),
            2: self.game.resources.get_image("grass_2"),
            3: self.game.resources.get_image("void_1"),
            4: self.game.resources.get_image("void_2"),
            5: self.game.resources.get_image("water_1_level"),
            6: self.game.resources.get_image("water_2_level"),
            7: self.game.resources.get_image("water_3_level"),
            8: self.game.resources.get_image("water_4_level"),
            9: self.game.resources.get_image("white"),
            10: self.game.resources.get_image("border_middle"),
            11: self.game.resources.get_image("border_1"),
            12: self.game.resources.get_image("border_2"),
            13: self.game.resources.get_image("border_3"),
            14: self.game.resources.get_image("border_4"),
            15: self.game.resources.get_image("border_angel_1"),
            16: self.game.resources.get_image("border_angel_2"),
            17: self.game.resources.get_image("border_angel_3"),
            18: self.game.resources.get_image("border_angel_4"),
            19: self.game.resources.get_image("border_square_1"),
            20: self.game.resources.get_image("border_square_2"),
            21: self.game.resources.get_image("border_square_3"),
            22: self.game.resources.get_image("border_square_4"),
            23: self.game.resources.get_image("path"),
            24: self.game.resources.get_image("forest_grass")
        }
        self.item_img = self.game.resources.get_image("oak_wood")
        self.squad = self.game.resources.get_image("squad_list")
        self.oak_butt = self.game.resources.get_image("oak_butt")

    def on_exit(self):
        # сохранить данные, очистить ресурсы
        pass

    def check_tile_collision(self, rect):
        if self.collision_data is None:
            return False

        left = rect.left // self.tile_size
        right = (rect.right - 1) // self.tile_size
        top = rect.top // self.tile_size
        bottom = (rect.bottom - 1) // self.tile_size
        width = len(self.collision_data[0])
        height = len(self.collision_data)
        for row in range(top, bottom + 1):
            for col in range(left, right + 1):
                if row < 0 or row >= height:
                    return True
                if col < 0 or col >= width:
                    return True
                if self.collision_data[row][col] != 0:
                    return True
        return False

    def update(self, dt, events):
        # Обработать ввод для перемещения, открытия меню, начала диалога и т.д.
        if InputHandler.is_key_pressed(events, pygame.K_b):
            self.game.change_state("inventory")
        if InputHandler.is_key_pressed(events, pygame.K_c):
            self.game.change_state("character")
        if InputHandler.is_key_pressed(events, pygame.K_m):
            self.game.change_state("map")
        if InputHandler.is_key_pressed(events, pygame.K_j):
            self.game.change_state("quest_log")
        if InputHandler.is_key_pressed(events, pygame.K_g):
            self.game.change_state("tutorials")
        if InputHandler.is_key_pressed(events, pygame.K_t):
            self.game.change_state("party")
        if InputHandler.is_key_pressed(events, pygame.K_f):
            if self.near_item == True:
                print('Получен Предмет')
                self.game.player.inventory.add_item("oak_wood", 1)
                self.item = False
            else:
                self.game.change_state("dialog")
        if InputHandler.is_key_pressed(events, pygame.K_F1):
            self.game.change_state("events")
        if InputHandler.is_key_pressed(events, pygame.K_F2):
            self.game.change_state("battlepass")
        if InputHandler.is_key_pressed(events, pygame.K_F3):
            self.game.change_state("gacha")
        if InputHandler.is_key_pressed(events, pygame.K_F4):
            self.game.change_state("passport")

        keys = pygame.key.get_pressed()
        self.is_moving = False
        dx = 0
        dy = 0
        move_speed = 5
        if InputHandler.is_key_held(keys, pygame.K_w):
            dy -= move_speed
            self.direction = "back"
            self.is_moving = True
        if InputHandler.is_key_held(keys, pygame.K_s):
            dy += move_speed
            self.direction = "straight"
            self.is_moving = True
        if InputHandler.is_key_held(keys, pygame.K_a):
            dx -= move_speed
            self.direction = "left"
            self.is_moving = True
        if InputHandler.is_key_held(keys, pygame.K_d):
            dx += move_speed
            self.direction = "right"
            self.is_moving = True

        new_rect_x = self.hero_rect.move(dx, 0)
        if not self.check_tile_collision(new_rect_x) and not any(new_rect_x.colliderect(r) for r in self.collision_rects):
            self.hero_rect.x = new_rect_x.x
        new_rect_y = self.hero_rect.move(0, dy)
        if not self.check_tile_collision(new_rect_y) and not any(new_rect_y.colliderect(r) for r in self.collision_rects):
            self.hero_rect.y = new_rect_y.y

        self.camera.update(self.hero_rect)

        if not self.is_moving:
            self.idle_timer += dt
            if self.idle_timer >= self.idle_interval:
                self.idle_frames_index = (self.idle_frames_index + 1) % len(self.idle_frames[self.direction])
                self.idle_timer = 0.0
        else:
            self.idle_frames_index = 0
            self.idle_timer = 0.0

        if self.is_moving:
            self.walk_timer += dt
            if self.walk_timer >= self.walk_interval:
                self.walk_frames_index = (self.walk_frames_index + 1) % len(self.walk_frames[self.direction])
                self.walk_timer = 0.0
        else:
            self.walk_frames_index = 0
            self.walk_timer = 0.0

        self.near_item = False
        if self.hero_rect.colliderect(self.item_rect):
            self.near_item = True

    def draw(self, screen):
        self.camera.draw_map(screen, self.ground_data, self.tile_textures)

        for rect in self.collision_rects:
            screen_rect = self.camera.apply(rect)
            screen.blit(self.oak_butt, screen_rect)

        hero_screen_rect = self.camera.apply(self.hero_rect)
        if self.is_moving == False:
            frames = self.idle_frames[self.direction]
            key = frames[self.idle_frames_index]
        elif self.is_moving == True:
            frames = self.walk_frames[self.direction]
            key = frames[self.walk_frames_index]
        player_sprite = self.game.resources.get_image(key)
        if player_sprite:
            screen.blit(player_sprite, hero_screen_rect)

        squad_width = int(self.game.WIDTH * 0.18)
        squad_height = int(self.game.HEIGHT * 0.45)
        squad_y = int(self.game.HEIGHT * 0.1)
        squad_x = self.game.WIDTH - squad_width - self.game.WIDTH * 0.02
        ramka = pygame.Rect(squad_x, squad_y, squad_width, squad_height)
        screen.blit(self.squad, ramka)

        if self.item == True:
            item_screen_rect = self.camera.apply(self.item_rect)
            screen.blit(self.item_img, item_screen_rect)

        if self.near_item == True and self.item == True:
            item_screen_rect = self.camera.apply(self.item_rect)
            hint_x = item_screen_rect.x - 10
            hint_y = item_screen_rect.y - 20
            hint_surf = self.hint_font.render("Нажмите F", True, (10, 10, 10))
            screen.blit(hint_surf, (hint_x, hint_y))