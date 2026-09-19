import pygame
from input_handler import InputHandler

class ArtifactState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.offset_y = self.game.HEIGHT * 0.013
        self.offset_x = self.game.WIDTH * 0.0073
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
        self.font = pygame.font.Font(None, 36)
        char_index = self.game.selected_character_index
        char = self.game.player.party[char_index]
        char_key = char.resource_key
        self.bg = self.game.resources.get_image(f"{char_key}_artifacts")
        if self.bg is None:
            self.bg = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
            self.bg.fill((40, 40, 60))

        try:
            self.portrait_img = pygame.image.load(char.portrait_path).convert_alpha()
        except (pygame.error, FileNotFoundError, AttributeError):
            self.portrait_img = pygame.Surface((290, 415))
            self.portrait_img.fill((150, 150, 200))
            print(f"Портрет для {char.name} не найден, создана заглушка")

        self.artifact_icons = {
            "plume_1": self.game.resources.get_image("plume_1"),
            "plume_2": self.game.resources.get_image("plume_2"),
            "flower_2": self.game.resources.get_image("flower_2"),
            "sands_2": self.game.resources.get_image("sands_2"),
            "goblet_2": self.game.resources.get_image("goblet_2")
        }

        self.button_images = {}
        button_names = ["characteristic", "weapon", "artifacts", "talents", "constellations"]
        for name in button_names:
            filename = f"button_{name}_{char_key}"
            try:
                img = self.game.resources.get_image(filename)
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
            y = y0_btn + self.offset_y + i * (self.btn_height + self.offset_y)
            rect = pygame.Rect(x0_btn + self.offset_x, y, self.btn_width, self.btn_height)
            self.nav_buttons.append({"text": text, "rect": rect})

    def on_exit(self):
        print("Выход из экрана Артефакты")

    def update(self, dt, events):
        if InputHandler.is_key_pressed(events, pygame.K_c) or InputHandler.is_key_pressed(events, pygame.K_ESCAPE):
            self.game.change_state("world")

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
        portrait_x = self.game.WIDTH * 0.4282 #585
        portrait_y = self.game.HEIGHT * 0.247 #190
        screen.blit(self.portrait_img, (portrait_x, portrait_y))
        for btn in self.nav_buttons:
            screen.blit(self.button_images[btn["text"]], btn["rect"])

        set_name = self.font.render("Сеты:", True, (250, 250, 250))
        screen.blit(set_name, (self.game.WIDTH * 0.8126, self.game.HEIGHT * 0.0651))  # 1110,50

        effects_name = self.font.render("Эффекты сета:", True, (250, 250, 250))
        screen.blit(effects_name, (self.game.WIDTH * 0.8126, self.game.HEIGHT * 0.3033))  # 1110,50

        char = self.game.player.party[self.game.selected_character_index]
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
                    else:
                        print(f"Иконка для {artifact_id} не найдена")