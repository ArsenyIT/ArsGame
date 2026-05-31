import pygame
class WorldState:
    def __init__(self, game):
        self.game = game
        self.player = None   # объект игрока на карте
        self.hero_rect = pygame.Rect(100, 100, 40, 40)

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
                    self.game.change_state("dialog")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.hero_rect.y -= 5
        if keys[pygame.K_s]:
            self.hero_rect.y += 5
        if keys[pygame.K_a]:
            self.hero_rect.x -= 5
        if keys[pygame.K_d]:
            self.hero_rect.x += 5

    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), self.hero_rect)