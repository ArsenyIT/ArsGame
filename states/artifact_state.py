import pygame
from input_handler import InputHandler
import json
from inventory import ITEM_DATA

class ArtifactState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.offset_y = self.game.HEIGHT * 0.026 #20
        self.offset_x = self.game.WIDTH * 0.0073 #10
        self.btn_width = int(self.game.WIDTH * 0.2372)
        self.btn_height = int(self.game.HEIGHT * 0.15625)
        self.circle_positions = {
            "flower": (self.game.WIDTH * 0.3265, self.game.HEIGHT * 0.2943), #446,226
            "plume": (self.game.WIDTH * 0.7313, self.game.HEIGHT * 0.2943), #999,226
            "sands": (self.game.WIDTH * 0.3265, self.game.HEIGHT * 0.5859), #446,450
            "goblet": (self.game.WIDTH * 0.7313, self.game.HEIGHT * 0.5859), #999,450
        }
        self.circle_radius = 60
        self.circle_rects = {}
        for name, pos in self.circle_positions.items():
            x, y = pos
            self.circle_rects[name] = pygame.Rect(x - self.circle_radius, y - self.circle_radius,
                                                  self.circle_radius * 2, self.circle_radius * 2)
        self.set_counts = {}

    def on_enter(self):
        self.font = pygame.font.Font(None, 36)
        self.mini_font = pygame.font.Font(None, 24)
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
        y0_btn = self.game.HEIGHT * 0.058 #45
        for i, text in enumerate(button_names):
            y = y0_btn + self.offset_y + i * (self.btn_height + self.offset_y)
            rect = pygame.Rect(x0_btn + self.offset_x, y, self.btn_width, self.btn_height)
            self.nav_buttons.append({"text": text, "rect": rect})

    def on_exit(self):
        print("Выход из экрана Артефакты")

    def set_count(self):
        char = self.game.player.party[self.game.selected_character_index]
        for slot_name, pos in self.circle_positions.items():
            # Проверяем, есть ли артефакт в этом слоте
            uid = char.artifacts.get(slot_name)
            if uid:
                data = char.artifact_data.get(str(uid), {})
                artifact_id = data.get("artifact_id")
                if artifact_id:
                    item_info = ITEM_DATA.get(artifact_id, {})
                    set_id = item_info.get("set")
                    self.set_counts[set_id] = self.set_counts.get(set_id, 0) + 1

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
        self.set_counts = {}
        self.set_count()
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

        with open(f"assets/data/artifact_sets.json", "r", encoding="utf-8") as f:
            sets = json.load(f)

        for set_id, count in self.set_counts.items():
            texts = sets[set_id]
            name_set = texts["name"]
            set_y1_1 = self.game.HEIGHT * 0.1172 #90
            set_y2_1 = self.game.HEIGHT * 0.36458 #280
            if count >= 2:
                text_2pc = texts["text_2pc"]
                lines = self.wrap_text(text_2pc, self.mini_font, self.game.WIDTH * 0.1464) #200
                y_offset = self.game.HEIGHT * 0.4036 #310
                for line in lines:
                    line_surf = self.mini_font.render(line, True, (250, 250, 250))
                    screen.blit(line_surf, (self.game.WIDTH * 0.8126, y_offset)) #1110
                    y_offset += self.game.HEIGHT * 0.03255 #25
                set = self.mini_font.render(f"{name_set} ({count})", True, (250, 250, 250))
                screen.blit(set, (self.game.WIDTH * 0.8126, set_y1_1)) #1110,90
                set_y1_1 += self.game.HEIGHT * 0.03255 #25
                screen.blit(set, (self.game.WIDTH * 0.8126, set_y2_1)) #1110,280
                set_y2_1 += 110

            if count >= 4 and "4pc" in texts:
                text_4pc = texts["text_4pc"]
                lines = self.wrap_text(text_4pc, self.mini_font, self.game.WIDTH * 0.1464) #200
                y_offset = self.game.HEIGHT * 0.468 #360
                for line in lines:
                    line_surf = self.mini_font.render(line, True, (250, 250, 250))
                    screen.blit(line_surf, (self.game.WIDTH * 0.8126, y_offset)) #1110
                    y_offset += self.game.HEIGHT * 0.03255 #25

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines