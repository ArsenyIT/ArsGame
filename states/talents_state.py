import pygame
from inventory import ITEM_DATA
from game_data import TALENT_BOOK_REQUIREMENTS

class TalentsState:
    def __init__(self, game):
        self.game = game
        self.font = None
        self.stats_font = None
        self.circle_positions = {
             "normal": (1058, 79),
             "skill": (1058, 157),
             "burst": (1058, 235),
            }
        self.circle_radius = 35
        self.field_width = 344
        self.offset = 10
        self.btn_width = self.field_width - 2 * self.offset  # 324
        self.btn_height = 120
        self.circle_rects = {}
        for name, pos in self.circle_positions.items():
            x, y = pos
            self.circle_rects[name] = pygame.Rect(x - self.circle_radius, y - self.circle_radius,
                                                  self.circle_radius * 2, self.circle_radius * 2)
        # Переменная для хранения активного таланта (если открыта плашка)
        self.active_talent = None
        # Кнопка "Улучшить" внутри плашки
        self.upgrade_button_rect = pygame.Rect(400, 400, 150, 40)
        # Кнопка закрытия плашки (крестик)
        self.close_button_rect = pygame.Rect(600, 200, 30, 30)

    def on_enter(self):
        print("Вход в экран Таланты")
        self.font = pygame.font.Font(None, 36)
        self.stats_font = pygame.font.Font(None, 28)
        self.popup_bg = pygame.image.load("assets/textures/Popup.png").convert_alpha()
        self.portrait_GG = pygame.image.load("assets/textures/GG_menu.png")
        try:
            self.background = pygame.image.load("assets/textures/GG_talents.png").convert_alpha()
        except pygame.error:
            self.background = None
        self.button_images = {}
        button_names = ["Характеристика", "Оружие", "Артефакты", "Таланты", "Созвездия"]
        for name in button_names:
            filename = f"assets/textures/buttons/Кнопка_{name}.png"
            try:
                img = pygame.image.load(filename).convert_alpha()
                # Масштабируем под размер кнопки (btn_width, btn_height)
                img = pygame.transform.scale(img, (self.btn_width, self.btn_height))
                self.button_images[name] = img
            except pygame.error:
                print(f"Не удалось загрузить картинку для кнопки {name}, используется заглушка")
                # Можно создать цветной прямоугольник как запасной вариант
                surf = pygame.Surface((self.btn_width, self.btn_height))
                surf.fill((80, 80, 120))
                self.button_images[name] = surf
        self.nav_buttons = []
        button_names = ["Характеристика", "Оружие", "Артефакты", "Таланты", "Созвездия"]
        x0_btn = 0
        y0_btn = 40
        offset = 10
        btn_width = 324
        btn_height = 120

        for i, text in enumerate(button_names):
            y = y0_btn + offset + i * (btn_height + offset)
            rect = pygame.Rect(x0_btn + offset, y, btn_width, btn_height)
            self.nav_buttons.append({"text": text, "rect": rect})
            # Картинки уже загружены в self.button_images
        #self.icons = {}
        #for name in self.circle_positions.keys():
        #    try:
        #        icon = pygame.image.load(f"assets/textures/icons/talent_{name}.png").convert_alpha()
        #        icon = pygame.transform.scale(icon, (60, 60))
        #        self.icons[name] = icon
        #    except pygame.error:
        #        self.icons[name] = None

        try:
            self.upgrade_btn_img = pygame.image.load("assets/textures/buttons/Кнопка_Улучшить.png").convert_alpha()
        except pygame.error:
            self.upgrade_btn_img = None
            print("Не удалось загрузить картинку кнопки 'Улучшить'")

    def on_exit(self):
        print("Выход из экрана Таланты")
        self.game.save_all()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.active_talent:
                        # Если открыта плашка, закрываем её
                        self.active_talent = None
                    else:
                        pass

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.active_talent:
                    # Если плашка открыта, обрабатываем клики внутри неё
                    self.handle_click_inside_popup(event.pos)
                    self.handle_click_on_nav_buttons(event.pos)
                else:
                    # Иначе проверяем клики по кругам
                    self.handle_click_on_circles(event.pos)
                    # Проверяем клики по кнопкам навигации
                    self.handle_click_on_nav_buttons(event.pos)

    def handle_click_on_nav_buttons(self, pos):
        for btn in self.nav_buttons:
            if btn["rect"].collidepoint(pos):
                # Если плашка открыта, закрываем её
                if self.active_talent:
                    self.active_talent = None
                # Переход на соответствующий экран
                text = btn["text"]
                if text == "Характеристика":
                    self.game.change_state("character")
                elif text == "Оружие":
                    self.game.change_state("weapon")
                elif text == "Артефакты":
                    self.game.change_state("artifact")
                elif text == "Таланты":
                    pass
                elif text == "Созвездия":
                    self.game.change_state("constellations")
                break

    def handle_click_on_circles(self, pos):
        #Обработка клика по кругам талантов
        for name, rect in self.circle_rects.items():
            if rect.collidepoint(pos):
                self.active_talent = name
                print(f"Открыта плашка таланта {name}")
                break

    def handle_click_inside_popup(self, pos):
        """Обработка кликов внутри плашки"""
        # Закрытие плашки
        #if self.close_button_rect.collidepoint(pos):
        #    self.active_talent = None
        #    return
        # Улучшение таланта
        if self.upgrade_button_rect.collidepoint(pos):
            self.try_upgrade_talent()

    def try_upgrade_talent(self):
        #Попытка улучшить активный талант
        if not self.active_talent:
            return
        char = self.game.player.party[0]  # временно первый персонаж
        talent_name = self.active_talent
        current_level = char.talents[talent_name]
        if not char.can_upgrade_talent(talent_name):
            print(f"Талант {talent_name} уже достиг максимального уровня!")
            return
        # Получаем требования для текущего уровня
        required_rarity, required_amount = char.get_talent_book_requirement(current_level)
        if required_rarity is None:
            print("Нет требований для этого уровня!")
            return
        # Проверяем наличие книг в инвентаре
        book_id = f"talent_book_{required_rarity}"  # например, "talent_book_2"
        if self.game.player.inventory.get_count(book_id) >= required_amount:
            # Тратим книги
            self.game.player.inventory.remove_item(book_id, required_amount)
            # Повышаем уровень таланта
            char.talents[talent_name] += 1
            print(f"Талант {talent_name} повышен до {char.talents[talent_name]} уровня!")
        else:
            print(f"Недостаточно книг! Нужно {required_amount} книг {required_rarity}★")

    def draw(self, screen):
        # Отрисовка фона
        screen.blit(self.background, (0, 0))
        screen.blit(self.portrait_GG, (560, 180))

        # Рисуем кнопки навигации (пока заглушка)
        for btn in self.nav_buttons:
            screen.blit(self.button_images[btn["text"]], btn["rect"])

        # Отрисовка кругов с иконками
        char = self.game.player.party[0]
        for name, pos in self.circle_positions.items():
            x, y = pos
            # Рисуем круг (можно сделать разным цветом для активного)
            color = (0, 0, 0) if self.active_talent == name else (0, 0, 0)
            pygame.draw.circle(screen, color, (x, y), self.circle_radius, 2)
            # Если есть иконка, рисуем её
            #if self.icons.get(name):
            #    icon_rect = self.icons[name].get_rect(center=(x, y))
            #    screen.blit(self.icons[name], icon_rect)
            # Текст уровня под кругом
            #level = char.talents[name]
            #level_text = self.font.render(str(level), True, (255, 255, 255))
            #screen.blit(level_text, (x - 10, y + self.circle_radius + 5))

            # Если открыта плашка, рисуем её
        if self.active_talent:
            self.draw_popup(screen, char)

    def draw_popup(self, screen, char):
        #Рисует плашку с описанием таланта
        # Затемнение фона
        dark = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        dark.fill((0, 0, 0, 150))
        screen.blit(dark, (0, 0))

        # Основной прямоугольник плашки
        popup_rect = pygame.Rect(0, 0, 400, 768)
        screen.blit(self.popup_bg, popup_rect)

        talent_name = self.active_talent
        current_level = char.talents[talent_name]
        max_level = char.get_talent_max_level()

        # Название таланта
        name_text = self.font.render(f"Талант: {talent_name.capitalize()}", True, (255, 255, 255))
        screen.blit(name_text, (popup_rect.x + 20, popup_rect.y + 20))

        # Уровень
        level_text = self.stats_font.render(f"Уровень: {current_level} / {max_level}", True,
                                                            (220, 220, 220))
        screen.blit(level_text, (popup_rect.x + 20, popup_rect.y + 60))

        # Описание таланта (пока временное)
        description = "Наносит урон в зависимости от силы атаки."
        desc_lines = self.wrap_text(description, self.stats_font, popup_rect.width - 40)
        y = popup_rect.y + 100
        for line in desc_lines:
            line_surf = self.stats_font.render(line, True, (200, 200, 200))
            screen.blit(line_surf, (popup_rect.x + 20, y))
            y += 25

        # Кнопка "Улучшить"
        if self.upgrade_btn_img:
            screen.blit(self.upgrade_btn_img, (30, 630))
            # Обновляем прямоугольник для проверки кликов
            self.upgrade_button_rect = pygame.Rect(30, 630, 278, 62)  # подгони размер под картинку
        else:
            # Запасной вариант – прямоугольник с текстом
            self.upgrade_button_rect = pygame.Rect(30, 630, 278, 62)
            pygame.draw.rect(screen, (60, 60, 80), self.upgrade_button_rect)
            pygame.draw.rect(screen, (200, 200, 200), self.upgrade_button_rect, 2)
            btn_text = self.font.render("Улучшить", True, (255, 255, 255))
            screen.blit(btn_text, (self.upgrade_button_rect.x + 10, self.upgrade_button_rect.y + 5))

        # Кнопка закрытия (крестик)
        #pygame.draw.rect(screen, (200, 50, 50), self.close_button_rect)
        #close_text = self.font.render("X", True, (255, 255, 255))
        #screen.blit(close_text, (self.close_button_rect.x + 5, self.close_button_rect.y))

        # Отображение требований к улучшению
        #req_rarity, req_amount = char.get_talent_book_requirement(current_level)
        #if req_rarity:
        #    req_text = self.stats_font.render(f"Требуется: {req_amount} книг {req_rarity}★", True,
        #                                      (255, 200, 100))
        #    screen.blit(req_text, (popup_rect.x + 20, popup_rect.y + 200))

    def wrap_text(self, text, font, max_width):
        """Разбивает текст на строки по ширине"""
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