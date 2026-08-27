import pygame
from inventory import ITEM_DATA
from game_data import calculate_weapon_stats

class WeaponUpgradeState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.stats_font = None
        self.weapon_uid = None
        self.weapon_data = None
        self.upgrade_btn_rect = None

    def on_enter(self):
        self.font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 28)
        self.weapon_uid = getattr(self.game, "temp_weapon_uid", None)
        if not self.weapon_uid:
            print("Ошибка: не передан UID оружия!")
            self.game.change_state("weapon")
            return
        # Удаляем временную переменную
        if hasattr(self.game, "temp_weapon_uid"):
            del self.game.temp_weapon_uid

        # Здесь загружаем фон и кнопки
        char_index = self.game.selected_character_index
        char = self.game.player.party[char_index]
        char_key = char.resource_key
        self.bg = self.game.resources.get_image(f"{char_key}_upgrade")
        if self.bg is None:
            self.bg = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
            self.bg.fill((40, 40, 60))
        try:
            self.upgrade_btn_img = self.game.resources.get_image(f"button_improve_{char_key}")
        except:
            self.upgrade_btn_img = None

        self.weapon_data = char.weapon_data.get(str(self.weapon_uid), {})
        if not self.weapon_data:
            print(f"Оружие с UID {self.weapon_uid} не найдено в данных!")
            self.game.change_state("weapon")
            return

    def on_exit(self):
        print("Выход из экрана Прокачка оружия")
        self.game.save_all()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_state("weapon")
                elif event.key == pygame.K_c:
                    self.game.change_state("world")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.upgrade_btn_rect and self.upgrade_btn_rect.collidepoint(event.pos):
                    self.try_upgrade()

    def try_upgrade(self):
        char = self.game.player.party[self.game.selected_character_index]
        inventory = self.game.player.inventory
        success = char.upgrade_weapon(str(self.weapon_uid), inventory)
        if success:
            # Обновляем локальные данные
            self.weapon_data = char.weapon_data.get(str(self.weapon_uid), {})
            # Помечаем, что данные партии изменились
            self.game.player.mark_modified()
            self.game.save_all()
            print("Оружие улучшено и сохранено!")
        else:
            print("Не удалось улучшить оружие")

    def draw(self, screen):
        if self.bg:
            screen.blit(self.bg, (0, 0))
        else:
            screen.fill((40, 40, 60))

        # Информация об оружии
        weapon_id = self.weapon_data.get("weapon_id")
        level = self.weapon_data.get("level", 1)
        if weapon_id:
            template = ITEM_DATA.get(weapon_id, {})
            name = template.get("name", "Неизвестно")
            weapon_stats = calculate_weapon_stats(weapon_id, level)
            atk_display = weapon_stats["atk"]
            sec_display = weapon_stats["secondary_value"]
            sec_name = weapon_stats["secondary_stat"]

            # Выводим информацию
            name_text = self.font.render(f"Оружие: {name}", True, (255, 255, 255))
            screen.blit(name_text, (self.game.WIDTH * 0.512, self.game.HEIGHT * 0.039)) #700,30

            level_text = self.stats_font.render(f"Уровень: {level}", True, (220, 220, 220))
            screen.blit(level_text, (self.game.WIDTH * 0.512, self.game.HEIGHT * 0.078)) #700,60

            atk_text = self.stats_font.render(f"Базовая атака: {atk_display}", True, (200, 200, 200))
            screen.blit(atk_text, (self.game.WIDTH * 0.512, self.game.HEIGHT * 0.117)) #700,90

            if sec_name:
                sec_text = self.stats_font.render(f"{sec_name}: +{sec_display}", True, (200, 200, 200))
                screen.blit(sec_text, (self.game.WIDTH * 0.512, self.game.HEIGHT * 0.15625)) #700,120

            # Кнопка "Улучшить"
            btn_y = self.game.HEIGHT * 0.82  # 630
            btn_width = self.game.WIDTH * 0.2035  # 278
            btn_height = self.game.HEIGHT * 0.0807  # 62
            self.upgrade_btn_rect = pygame.Rect(self.game.WIDTH * 0.6588, btn_y, btn_width, btn_height) #900
            if self.upgrade_btn_img:
                screen.blit(self.upgrade_btn_img, self.upgrade_btn_rect)
            else:
                pygame.draw.rect(screen, (60, 60, 80), self.upgrade_btn_rect)
                pygame.draw.rect(screen, (200, 200, 200), self.upgrade_btn_rect, 2)
                text = self.font.render("Улучшить", True, (255, 255, 255))
                screen.blit(text, (self.upgrade_btn_rect.x + self.game.WIDTH * 0.0073, self.upgrade_btn_rect.y + self.game.HEIGHT * 0.013)) #10
        else:
            error_text = self.font.render("Ошибка: оружие не найдено", True, (255, 0, 0))
            screen.blit(error_text, (self.game.WIDTH * 0.512, self.game.HEIGHT * 0.1042)) #700,80

        exp = self.weapon_data.get("exp", 0)
        exp_next = self.weapon_data.get("exp_next", 100)
        exp_ratio = exp / exp_next if exp_next > 0 else 0
        # Полоска опыта
        pygame.draw.rect(screen, (80, 80, 80), (self.game.WIDTH * 0.512, self.game.HEIGHT * 0.26, self.game.WIDTH * 0.1464, self.game.HEIGHT * 0.0195)) #700,200,200,15
        pygame.draw.rect(screen, (100, 200, 100), (self.game.WIDTH * 0.512, self.game.HEIGHT * 0.26, int(self.game.WIDTH * 0.1464 * exp_ratio), self.game.HEIGHT * 0.0195)) #700,200,200,15
        exp_text = self.stats_font.render(f"Опыт: {exp}/{exp_next}", True, (200, 200, 200))
        screen.blit(exp_text, (self.game.WIDTH * 0.512, self.game.HEIGHT * 0.28646)) #700,220
        crystals = self.game.player.inventory.get_count("crystal_of_true_power")
        crystal_text = self.stats_font.render(f"Кристаллов: {crystals}", True, (200, 200, 200))
        screen.blit(crystal_text, (self.game.WIDTH * 0.512, self.game.HEIGHT * 0.3125)) #700,240