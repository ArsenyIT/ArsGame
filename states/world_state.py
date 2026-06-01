import pygame
class WorldState:
    def __init__(self, game):
        self.game = game
        self.player = None   # объект игрока на карте
        self.hero_rect = pygame.Rect(100, 100, 40, 40)
        self.item_rect = pygame.Rect(200, 200, 40, 40)
        self.hint_font = pygame.font.Font(None, 24)
        self.near_item = False
        self.item = True

    def on_enter(self):
        # загрузить карту, спрайты, инициализировать положение игрока
        pass

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
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0,0,255), self.hero_rect, 20)
        if self.item == True:
            pygame.draw.rect(screen, (0,0,0), self.item_rect, 20)

        if self.near_item == True and self.item == True:
            hint_surf = self.hint_font.render("Нажмите F", True, (10, 10, 10))
            screen.blit(hint_surf, (self.item_rect.x - 10, self.item_rect.y - 20))