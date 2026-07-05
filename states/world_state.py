import pygame
import json

class WorldState:
    def __init__(self, game):
        self.game = game
        self.hero_rect = pygame.Rect(100, 100, 45, 90)
        self.item_rect = pygame.Rect(200, 200, 13, 32)
        self.hint_font = pygame.font.Font(None, 24)
        self.near_item = False
        self.item = True
        self.tile_size = 50

    def on_enter(self):
        # загрузить карту, спрайты, инициализировать положение игрока
        with open("assets/maps/map.json", "r", encoding="utf-8") as f:
            map_json = json.load(f)
        self.map_data = map_json["data"]
        self.tile_textures = {
            0: pygame.image.load("assets/textures/tiles/Grass_1.png").convert_alpha(),
        }
        self.player_img = pygame.image.load("assets/textures/GG_left.png").convert_alpha()
        self.item_img = pygame.image.load("assets/textures/items/Oak_wood_item.png")
        self.squad = pygame.image.load("assets/textures/Squad_list.png")

    def on_exit(self):
        # сохранить данные, очистить ресурсы
        pass

    def update(self, dt, events):
        # Обработать ввод для перемещения, открытия меню, начала диалога и т.д.
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.game.change_state("inventory")
                elif event.key == pygame.K_c:
                    self.game.change_state("character")
                elif event.key == pygame.K_m:
                    self.game.change_state("map")
                elif event.key == pygame.K_j:
                    self.game.change_state("quest_log")
                elif event.key == pygame.K_g:
                    self.game.change_state("tutorials")
                elif event.key == pygame.K_t:
                    self.game.change_state("party")
                elif event.key == pygame.K_f:
                    if self.near_item == True:
                        print('Получен Предмет')
                        self.game.player.inventory.add_item("oak_wood", 1)
                        self.item = False
                    else:
                        self.game.change_state("dialog")
                elif event.key == pygame.K_F1:
                    self.game.change_state("events")
                elif event.key == pygame.K_F2:
                    self.game.change_state("battlepass")
                elif event.key == pygame.K_F3:
                    self.game.change_state("gacha")
                elif event.key == pygame.K_F4:
                    self.game.change_state("passport")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.hero_rect.y -= 5
        if keys[pygame.K_s]:
            self.hero_rect.y += 5
        if keys[pygame.K_a]:
            self.hero_rect.x -= 5
        if keys[pygame.K_d]:
            self.hero_rect.x += 5

        self.near_item = False
        if self.hero_rect.colliderect(self.item_rect):
            self.near_item = True

    def draw(self, screen):
        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                tile_type = self.map_data[row][col]
                x = col * self.tile_size
                y = row * self.tile_size
                screen.blit(self.tile_textures[tile_type], (x, y))
        screen.blit(self.player_img, self.hero_rect)
        ramka = pygame.Rect(screen.get_width() - 250 - 30, 80, 250, 350)
        screen.blit(self.squad, ramka)

        if self.item == True:
            screen.blit(self.item_img, self.item_rect)

        if self.near_item == True and self.item == True:
            hint_surf = self.hint_font.render("Нажмите F", True, (10, 10, 10))
            screen.blit(hint_surf, (self.item_rect.x - 10, self.item_rect.y - 20))