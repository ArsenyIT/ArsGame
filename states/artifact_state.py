import pygame

class ArtifactState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.field_width = 344
        self.offset = 10
        self.btn_width = self.field_width - 2 * self.offset  # 324
        self.btn_height = 120
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
        self.bg = pygame.image.load("assets/textures/Арсений_Артефакты.png").convert_alpha()
        self.portrait_GG = pygame.image.load("assets/textures/ГГ_меню.png")

        self.artifact_icons = {
            "feather_1": pygame.image.load("assets/textures/Перо_1.png").convert_alpha(),
            "feather_2": pygame.image.load("assets/textures/Перо_2.png").convert_alpha(),
        }

        self.button_images = {}
        button_names = ["Характеристика", "Оружие", "Артефакты", "Таланты", "Созвездия"]
        for name in button_names:
            filename = f"assets/textures/buttons/Кнопка_{name}.png"
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
        y0_btn = 40
        offset = 10
        btn_width = 324
        btn_height = 120
        for i, text in enumerate(button_names):
            y = y0_btn + offset + i * (btn_height + offset)
            rect = pygame.Rect(x0_btn + offset, y, btn_width, btn_height)
            self.nav_buttons.append({"text": text, "rect": rect})

    def on_exit(self):
        print("Выход из экрана Артефакты")

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                        if text == "Характеристика":
                            self.game.change_state("character")
                        elif text == "Оружие":
                            self.game.change_state("weapon")
                        elif text == "Артефакты":
                            pass
                        elif text == "Таланты":
                            self.game.change_state("talents")
                        elif text == "Созвездия":
                            self.game.change_state("constellations")
                        break

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.portrait_GG, (580, 200))
        for btn in self.nav_buttons:
            screen.blit(self.button_images[btn["text"]], btn["rect"])

        char = self.game.player.party[0]
        for slot_name, pos in self.circle_positions.items():
            x, y = pos
            # Проверяем, есть ли артефакт в этом слоте
            equipped_id = char.artifacts.get(slot_name)
            if equipped_id and equipped_id in self.artifact_icons:
                icon = self.artifact_icons[equipped_id]
                icon_rect = icon.get_rect(center=(x, y))
                screen.blit(icon, icon_rect)