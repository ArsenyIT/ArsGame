import pygame

class ArtifactState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.offset = 10
        self.btn_width = int(self.game.WIDTH * 0.2372)
        self.btn_height = int(self.game.HEIGHT * 0.15625)
        self.circle_positions = {
            "flower": (441, 238),
            "plume": (1017, 239),
            "sands": (439, 419),
            "goblet": (1018, 421),
        }
        self.circle_radius = 60
        self.circle_rects = {}
        for name, pos in self.circle_positions.items():
            x, y = pos
            self.circle_rects[name] = pygame.Rect(x - self.circle_radius, y - self.circle_radius,
                                                  self.circle_radius * 2, self.circle_radius * 2)

    def on_enter(self):
        print("Вход в экран Артефакты")
        self.font = pygame.font.Font(None, 36)
        self.bg = pygame.image.load("assets/textures/characters_menu/GG/GG_artifacts.png").convert_alpha()
        self.portrait_GG = pygame.image.load("assets/textures/characters_menu/characters_portraits/GG.png")

        self.artifact_icons = {
            "plume_1": pygame.image.load("assets/textures/artifacts/Plume_1.png").convert_alpha(),
            "plume_2": pygame.image.load("assets/textures/artifacts/Plume_2.png").convert_alpha(),
            "flower_1": pygame.image.load("assets/textures/artifacts/Flower_1.png").convert_alpha(),
            "sands_1": pygame.image.load("assets/textures/artifacts/Sands_1.png").convert_alpha(),
            "goblet_1": pygame.image.load("assets/textures/artifacts/Goblet_1.png").convert_alpha()
        }

        self.button_images = {}
        button_names = ["characteristic", "weapon", "artifacts", "talents", "constellations"]
        for name in button_names:
            filename = f"assets/textures/buttons/Button_{name}.png"
            try:
                img = pygame.image.load(filename).convert_alpha()
                img = pygame.transform.scale(img, (self.btn_width, self.btn_height))
                self.button_images[name] = img
            except pygame.error:
                surf = pygame.Surface((self.btn_width, self.btn_height))
                surf.fill((80, 80, 120))
                self.button_images[name] = surf

        self.nav_buttons = []
        x0_btn = 0
        y0_btn = int(self.game.HEIGHT * 0.0521)
        for i, text in enumerate(button_names):
            y = y0_btn + self.offset + i * (self.btn_height + self.offset)
            rect = pygame.Rect(x0_btn + self.offset, y, self.btn_width, self.btn_height)
            self.nav_buttons.append({"text": text, "rect": rect})

    def on_exit(self):
        print("Выход из экрана Артефакты")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c or event.key == pygame.K_ESCAPE:
                    self.game.change_state("world")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Проверка кликов по кругам (переход в artifact_upgrade)
                for slot_name, rect in self.circle_rects.items():
                    if rect.collidepoint(event.pos):
                        self.game.temp_slot = slot_name
                        self.game.change_state("artifact_upgrade")
                        break
                # Проверка кликов по навигации
                for btn in self.nav_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        text = btn["text"]
                        if text == "characteristic":
                            self.game.change_state("character")
                        elif text == "weapon":
                            self.game.change_state("weapon")
                        elif text == "artifacts":
                            pass
                        elif text == "talents":
                            self.game.change_state("talents")
                        elif text == "constellations":
                            self.game.change_state("constellations")
                        break

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        portrait_x = int(self.game.WIDTH * 0.425)
        portrait_y = int(self.game.HEIGHT * 0.282)
        screen.blit(self.portrait_GG, (portrait_x, portrait_y))
        for btn in self.nav_buttons:
            screen.blit(self.button_images[btn["text"]], btn["rect"])

        char = self.game.player.party[0]
        for slot_name, pos in self.circle_positions.items():
            x, y = pos
            # Проверяем, есть ли артефакт в этом слоте
            uid = char.artifacts.get(slot_name)
            if uid:
                data = char.artifact_data.get(str(uid), {})
                artifact_id = data.get("artifact_id")
                if artifact_id:
                    icon = self.artifact_icons.get(artifact_id)
                    if icon:
                        icon_rect = icon.get_rect(center=(x, y))
                        screen.blit(icon, icon_rect)
                    # Если иконка не найдена, можно вывести сообщение в консоль
                    else:
                        print(f"Иконка для {artifact_id} не найдена")