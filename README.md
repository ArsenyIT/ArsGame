# ArsGame

## Структура проекта:


***

## Библиотеки:


***

## Основные файлы:

### Файл main:
1. Предназначение:
* Запускает и управляет циклом, передавая всю логику классу Game.

2. Библиотеки:
* import pygame (Работа с графикой, звуком и событиями)
* from game import Game (Состояния игры)

3. Функция main():
* Назначение: Главная функция, которая запускает игру. В ней происходит вся инициализация и главный цикл.
* Параметры: Отсутствуют.
* Инициализация Pygame:
    * pygame.init() - инициализирует все подсистемы Pygame. Без этого вызова ничего не будет работать.
* Настройки окна:
    * WIDTH и HEIGHT - размеры игрового окна (ширина и высота в пикселях).
    * screen = pygame.display.set_mode((WIDTH, HEIGHT)) – создаёт окно с указанными размерами.
    * pygame.display.set_caption("ArsGame") – устанавливает заголовок окна.
* Часы для ограничения FPS:
    * clock = pygame.time.Clock() – создаёт объект для управления кадрами в секунду (FPS).
* Создание объекта игры:
    * game = Game(screen, WIDTH, HEIGHT) – создаёт экземпляр класса Game, передавая ему экран и размеры окна.
* Главный цикл:
    * running = True – флаг, который управляет продолжением цикла.
    * while running: – бесконечный цикл, пока running не станет False.
    * dt = clock.tick(60) / 1000.0:
        * clock.tick(60) – ограничивает цикл до 60 кадров в секунду и возвращает время, прошедшее с предыдущего кадра (в миллисекундах).
        * dt – время в секундах между кадрами (delta time). Используется для плавного движения, чтобы игра работала одинаково на разных частотах обновления.
    * dt = min(dt, 0.05) - минимальное ограничение времени между кадрами.
    * events = pygame.event.get() – получает список всех событий, произошедших за время цикла (нажатия клавиш, движение мыши, закрытие окна и т.д.).
    * Обработка событий:
        * for event in events: – перебирает все события.
            * if event.type == pygame.QUIT: – проверяет, не нажата ли кнопка закрытия окна (крестик).
            * elif event.type == pygame.KEYDOWN: - проверяет, не нажата ли кнопка клавиша.
                * if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL): - проверяет, не нажата ли кнопка S+Ctrl.
    * game.update(dt, events) – передаёт текущее время и список событий в объект игры для обновления логики (движение персонажей, физика, ИИ и т.д.).
    * game.draw(screen) – вызывает отрисовку всех объектов на экране (передаёт поверхность screen).
    * pygame.display.flip() – обновляет окно, показывая нарисованное. Без этого вызова экран останется пустым.
* Завершение работы:
    * game.save_all() – сохраняет прогресс игры (инвентарь, данные персонажа) на диск.
    * pygame.quit() – корректно завершает работу Pygame (освобождает ресурсы, закрывает окно).
4. Конструкция if __name__ == "__main__":
* main() - вызывается только если файл запущен напрямую (а не импортирован как модуль).

### Файл game:
1. Предназначение:
* Cоздаёт игрока, загружает все возможные состояния (экраны) и переключает между ними.

2. Библиотеки:
* from player import Player (Подключает класс Player, который содержит инвентарь и отряд персонажей.)

3. Класс Game:
* Функция init(self, screen, WIDTH, HEIGHT):
    * Назначение: Создаёт экземпляр игры, инициализирует состояния и игрока.
    * Параметры:
        * self — ссылка на текущий объект
        * screen - окно
        * WIDTH, HEIGHT - размеры окна
    * Атрибуты:
        * self.screen – поверхность окна, переданная из main.py.
        * self.state – текущее активное состояние (например, world_state, inventory_state).
        * self.states – словарь, где ключ – имя состояния (строка), значение – объект состояния (экземпляр класса).
        * self.player – объект игрока (содержит инвентарь, партию, прогресс).
        * self.WIDTH и self.HEIGHT – размеры окна (передаются из main.py). 
        * self.change_state("world") - начальное состояние
        * self.load_states() - загружает все состояния.
4. Функции класса Game:
* load_states(self):
    * Назначение: Загружает все состояния игры и регистрирует их в словаре self.states.
    * from states.имя_файла import ИмяКласса - импортирует классы состояний из папки states.
    * self.states["имя"] = ИмяКласса(self) - создаёт экземпляр каждого состояния, передавая ему ссылку на Game (через self) и сохраняет их в словарь self.states.
    * Важно: Все состояния должны иметь методы on_enter(), on_exit(), update(dt, events), draw(screen). Это единый интерфейс, который использует Game.
* change_state(self, new_state_name):
    * Назначение: Переключает текущее состояние на новое.
    * Параметры: 
        * new_state_name – строка, ключ в словаре self.states.
    * if self.state: self.state.on_exit() - если есть текущее состояние (self.state), вызывает его метод on_exit() – для завершения (сохранение данных, очистка ресурсов).
    * self.state = self.states[new_state_name] - устанавливает новое состояние из словаря
    * self.state.on_enter() - инициализация всех данных нового состояния.
* update(self, dt, events):
    * Назначение: Обновляет логику текущего состояния.
    * Параметры: 
        * dt – дельта-время 
        * events – список событий Pygame.
    * if self.state: self.state.update(dt, events) - если есть текущее состояние (self.state), вызывает его метод update(dt, events).
* draw(self, screen):
    * Назначение: Отрисовывает текущее состояние.
    * Параметры: 
        * screen – поверхность окна.
    * if self.state: self.state.draw(screen) - если есть текущее состояние, вызывает его метод draw(screen).
* save_all(self):
    * Назначение: Сохраняет прогресс игры (инвентарь и данные персонажа) на диск.
    * saved = False - флаг сохранения всех изменений
    * if self.player.inventory.modified: self.player.inventory.save("assets/data/inventory.json") - если инвентарь изменён, сохраняет его в inventory.json.
    * if self.player.modified: self.player.save_party("assets/data/party_save.json") - если данные персонажа изменены, сохраняет их в party_save.json.

### Файл player:
1. Предназначение:
* Управляет игроком и всеми его данными: инвентарём, отрядом, загрузкой и сохранением прогресса.

2. Библиотеки:
* from inventory import Inventory (Класс для управления инвентарём)
* from game_data import Character (Класс персонажа)
* import random (Генерация случайных значений)
* import json (Работа с JSON-файлами)
* import os (Работа с путями)
* from game_data import generate_artifact_main_stat (Функция, выбирающая случайный основной стат для артефакта)
* from inventory import ITEM_DATA (Словарь со всеми данными предметов)
* from inventory import PREFIX_WEAPON (Строковая константа, используется для идентификации предметов)

3. Класс Player:
* Функция init(self):
    * Назначение: Создаёт игрока и хранит его данные игрока, управляет загрузкой/сохранением прогресса, добавлением предметов и восстановлением данных экипировки.
    * Параметры: 
        * self – ссылка на текущий объект
    * Атрибуты:
        * Инвентарь:
            * self.inventory = Inventory() - создаётся объект Inventory
            * self.inventory.load("assets/data/inventory.json") - загружаются данные из inventory.json.
        * Данные героя:
            * with open("assets/data/characters/GG.json", "r", encoding="utf-8") as f: data = json.load(f) - открывается файл с начальными статами героя и загружается в словарь data.
        * Создание объекта Character:
            * hero = Character(...) - создаётся экземпляр класса Character с параметрами из data.
        * Создание отряда и загрузка сохранения:
            * self.party = [hero] - отряд пока состоит из одного героя.
            * self.load_party("assets/data/party_save.json") - load_party загружает сохранённый прогресс и обновляет данные героя.
        * Восстановление данных оружия:
            * hero = self.party[0] - берём первого персонажа из отряда.
            * for uid in self.inventory.get_all_uids("weapons"): - получаем список всех UID оружия из инвентаря и проходим по каждому.
            * uid_str = str(uid) – преобразуем UID в строку, потому что в словарях weapon_data ключи хранятся как строки.
            * if uid_str not in hero.weapon_data: – проверяем, есть ли у этого персонажа уже запись для данного UID. Если запись уже есть – пропускаем.
            * for item_id, uids in self.inventory.items.items(): - Если записи нет, начинаем поиск в словаре self.inventory.items.
            * if isinstance(uids, list) and uid in uids: – проверяем, что uids является списком и текущий UID присутствует в этом списке.
            * if self.inventory.get_item_type(item_id) == "weapons": – проверяем, что предмет действительно оружие.
            * hero.weapon_data[uid_str] = {...} - если все проверки пройдены, создаём запись.
            * break – выходим из внутреннего цикла, потому что мы нашли нужный предмет и не нужно продолжать поиск.
        * Восстановление данных артефактов:
            * for uid in self.inventory.get_all_uids("artifacts"): - получаем список всех UID артефактов из инвентаря и проходим по каждому.
            * uid_str = str(uid) – преобразуем UID в строку, потому что в словарях artifact_data ключи хранятся как строки.
            * if uid_str not in hero.artifact_data: – проверяем, есть ли у этого персонажа уже запись для данного UID. Если запись уже есть – пропускаем.
            * for item_id, uids in self.inventory.items.items(): - Если записи нет, начинаем поиск в словаре self.inventory.items.
            * if isinstance(uids, list) and uid in uids: – проверяем, что uids является списком и текущий UID присутствует в этом списке.
            * if self.inventory.get_item_type(item_id) == "artifacts": – проверяем, что предмет действительно артефакт.
            * main_stat = generate_artifact_main_stat(item_id) – генерируем основной стат, потому что он выбирается случайно при создании артефакта.
            * if not main_stat: main_stat = {} – если по какой-то причине функция вернула пустой результат (например, в данных нет возможных статов), создаём пустой словарь, чтобы не было ошибки.
            * hero.artifact_data[uid_str] = {...} - создаём запись в artifact_data.
            * break – выходим из внутреннего цикла, потому что мы нашли нужный предмет и не нужно продолжать поиск.
        * Сохранение начального состояния:
            * self.save_party("assets/data/party_save.json") - Сохраняет данные, чтобы на диске была актуальная копия.
 
4. Функции класса Player:
* mark_modified(self):
    * Назначение: Устанавливает флаг, что данные игрока изменились.
    * self.modified = True - меняет флаг со лжи на истину.

* add_artifact(self, artifact_id):
    * Назначение: Добавляет артефакт в инвентарь и создаёт запись в artifact_data героя.
    * Параметры: 
        * artifact_id – строка (идентификатор артефакта из ITEM_DATA).
    * uid = self.inventory.add_item(artifact_id, 1) - вызываем метод add_item у инвентаря, который добавляет 1 предмет с artifact_id, генерирует новый UID для этого предмета и возвращает этот UID или None, если добавление не удалось.
    * if uid: – если UID получен, то продолжаем.
    * hero = self.party[0] – берём первого персонажа из отряда. 
    * art_data = ITEM_DATA.get(artifact_id, {}) – получаем данные артефакта из глобального словаря ITEM_DATA.
    * slot = art_data.get("slot") – получаем слот артефакта.
    * possible_main = art_data.get("possible_main_stats", []) – получаем список возможных основных статов для этого артефакта.
    * if not possible_main or not slot: – если нет слота или нет возможных основных статов – значит, данные артефакта некорректны.
    * self.inventory.remove_item(artifact_id, uid) - удаляем предмет из инвентаря.
    * chosen = random.choice(possible_main) – случайно выбираем один из возможных основных статов.
    * stat_name = list(chosen.keys())[0] – извлекаем имя стата из списка.
    * growth_key = f"{slot}_{stat_name}" – формируем ключ для роста артефакта.
    * hero.artifact_data[str(uid)] = {...} - создаём запись в artifact_data.

* add_weapon(self, weapon_id):
    * Назначение: Добавляет оружие в инвентарь и создаёт запись в weapon_data героя.
    * Параметры: 
        * weapon_id – строка (идентификатор оружия из ITEM_DATA).
    * uid = self.inventory.add_item(weapon_id, 1) - добавляет оружие в инвентарь и получает UID.
    * if uid: hero = self.party[0] and hero.weapon_data[str(uid)] = {...} - создаёт запись в weapon_data.

* save_party(self, filename):
    * Назначение: Сохраняет отряд в JSON-файл.
    * Параметры: 
        * filename – строка (путь к файлу).
    * chars_data = [] - список данных всех персонажей.
    * for char in self.party: char_data = {...} - проходит по всем персонажам в self.party и для каждого собирает все важные данные в словарь.
    * chars_data.append(char_data) - переносит данные персонажа в список.
    * full_data = {"characters": chars_data} - оборачивает список персонажей в словарь с ключом "characters".
    * os.makedirs(os.path.dirname(filename), exist_ok=True) - создаёт папку, если её нет.
    * with open(filename, 'w', encoding='utf-8') as f: json.dump(full_data, f, ensure_ascii=False, indent=2) - записывает данные в JSON с отступами для читаемости.
    * self.modified = False - сбрасывает флаг.

* load_party(self, filename):
    * Назначение: Загружает отряд из JSON-файла и обновляет данные существующего героя.
    * Параметры: 
        * filename – строка (путь к файлу).
    * if os.path.exists(filename) and os.path.getsize(filename) > 0: - проверяет, существует ли файл и не пуст ли он. Если нет – выводит сообщение и выходит.
    * with open(filename, 'r', encoding='utf-8') as f: data = json.load(f) - загружает данные из JSON.
    * if isinstance(data, list): chars_data = data and full_data = {"characters": chars_data} - если файл старого формата (просто список) – оборачивает его в словарь.
    * chars_data = full_data.get("characters", []) - для каждого персонажа в отряде берёт соответствующие сохранённые данные.
    * for i, char in enumerate(self.party): if i < len(chars_data): - обновляет все поля текущего героя (если поле отсутствует в сохранении, оставляет текущее значение).
    * Важно: для каждого артефакта проверяет наличие growth_key. Если его нет – восстанавливает из slot и названия основного стата (для совместимости со старыми сохранениями). 

### Файл inventory:
1. Предназначение:
* Управляет системой предметов в игре. Этот модуль является связующим звеном между предметами и персонажем

2. Библиотеки:
* json (Загрузка и сохранения инвентаря в файл) 
* os (Работа с путями, проверка существования и создание папок)
* time – пока не используется (может быть задел для будущих систем, например, тайминга предметов).

3. Константы:
* PREFIX_ARTIFACT = "artifact_" - используется для идентификации уникальных артефактов.
* PREFIX_WEAPON = "weapon_" - используется для идентификации уникального оружия.

4. Словари:
* ITEM_DATA:
    * Главный источник данных о всех предметах в игре. Каждый ключ – это строковый идентификатор предмета (например, "oak_wood"), а значение – словарь с его свойствами.

5. Класс Item:
* Функция init(self, item_id, max_stack=1000):
    * Назначение: Этот класс пока не используется в коде. Он, вероятно, задумывался как представление отдельного предмета с его свойствами. Сейчас вся логика инвентаря реализована через класс Inventory.
    * Параметры:
        * self - ссылка на текущий объект.
        * item_id - ID предмета.
        * max_stack - максимальное кол-во предметов в стаке.
    * Атрибуты:
        * self.id = item_id - ID предмета.
        * self.data = ITEM_DATA.get(item_id, {}) - информация о предмете.
        * self.max_stack = max_stack - максимальное кол-во предметов в стаке.
        * self.items = {} - словарь предметов.
        * self.modified = False - флаг изменений.
        * self.counter = 0 - счётчик.

6. Класс Inventory:
* Функция init(self):
    * Назначение: Управляет инвентарём игрока, хранит предметы двух типов: ресурсы и уникальные предметы (оружие, артефакты).
    * Параметры:
        * self - ссылка на текущий объект. 
    * Атрибуты:
        * self.items – словарь для ресурсов и уникальных предметов.
        * self.modified – флаг, указывающий, были ли изменения (для сохранения).
        * self.uid_counter – глобальный счётчик для генерации новых UID.

7. Функции класса Inventory:
* Функция get_item_type(self, item_id):
    * Назначение: Определяет тип предмета по его ID.
    * Параметры: 
        * item_id - ID предмета.
    * if item_id in ITEM_DATA: return ITEM_DATA[item_id].get("type") - проверяет наличие ID предмета.
    * elif item_id.startswith(PREFIX_WEAPON): return "weapons" - проверяет константу оружия.
    * elif item_id.startswith(PREFIX_ARTIFACT): return "artifacts" - проверяет константу артефакта.
* Функция add_item(self, item_id, amount=1):
    * Назначение: Добавляет предмет в инвентарь.
    * Параметры:
        * item_id - ID предмета.
        * amount - кол-во предметов.
    * item_data = ITEM_DATA.get(item_id, {}) - получаем всю информацию из ITEM_DATA.
    * item_type = item_data.get("type") - получаем все типы предметов из ITEM_DATA.
    * if item_type == "resources": - если предмет типа "resources" – увеличивает количество в self.items (или создаёт новую запись).
    * elif item_type in ["artifacts", "weapons"]: - если предмет типа "artifacts" или "weapons" – генерирует новый UID (self.uid_counter += 1), добавляет UID в список для этого item_id и возвращает UID.
    * self.modified = True - меняет флаг изменений.
* Функция remove_item(self, item_id, uid=None):
    * Назначение: Удаляет предмет из инвентаря. 
    * Параметры:
        * item_id - ID предмета.
        * uid - UID предмета.
    * if item_id in ITEM_DATA and ITEM_DATA[item_id].get("type") == "resources": - если предмет типа "resources" - уменьшает количество на 1. Если становится 0, удаляет запись.
    * elif item_id in ITEM_DATA and ITEM_DATA[item_id].get("type") in ["artifacts", "weapons"]: - если предмет типа "artifacts" или "weapons", если uid не указан, удаляет последний UID из списка, если указан, удаляет конкретный UID, если список становится пустым, удаляет запись.
    * self.modified = True - меняет флаг изменений.
* Функция get_count(self, item_id):
    * Назначение: Возвращает количество предметов данного ID.
    * Параметры:
        * item_id - ID предмета.
    * if item_id in ITEM_DATA and ITEM_DATA[item_id].get("type") == "resources": - для ресурсов – возвращает число из self.items.get(item_id, 0), а для уникальных – возвращает длину списка UID.
* Функция get_uid_list(self, item_id):
    * Назначение: Возвращает список UID для указанного ID предмета или пустой список, если предмета нет или это ресурс.
    * Параметры:
        * item_id - ID предмета.
* Функция get_all_uids(self, item_type=None):
    * Назначение: Возвращает все UID предметов определённого типа (например, "weapons" или "artifacts"), или все UID, если тип не указан. 
    * Параметры:
        * item_type - тип предмета.
    * for item_id, uids in self.items.items(): - проходит по self.items.
    * if isinstance(uids, list): - проверяет, чтобы значение было списком.
    * if item_type is None or (ITEM_DATA.get(item_id, {}).get("type") == item_type): result.extend(uids).
* Функция save(self, filename):
    * Назначение: Сохраняет self.items в JSON-файл.
    * Параметры:
        * filename - имя файла.
    * with open(filename, 'w', encoding='utf-8') as f: json.dump(self.items, f, ensure_ascii=False, indent=2) - открывает файл, записывает новую информацию.
    * self.modified = False - сбрасывает флаг.
* Функция load(self, filename):
    * Назначение: Загружает данные инвентаря из JSON-файла.
    * Параметры:
        * filename - имя файла.
    * if os.path.exists(filename) and os.path.getsize(filename) > 0: - проверяет существование и не пустоту файла.
    * with open(filename, 'r', encoding='utf-8') as f: self.items = json.load(f) - если файл есть, то загружает его.
    * else: self.items = {} - устанавливает пустой список.
    * self.modified = False - сбрасывает флаг.

### Файл game_data:
1. Предназначение:
* Этот модуль связывает предметы (из inventory.py) и игровую логику (прокачка, экипировка, бой).

2. Библиотеки:
* import json (Для загрузки файлов роста оружия/артефактов и данных персонажа).
* from inventory import ITEM_DATA (Для работы с экипировкой и прокачкой предметов).
* import random (Для генерации случайных значений).

3. Константы:
* MAX_ARTIFACT_LEVEL_BY_RARITY - определяет максимальный уровень артефакта в зависимости от его редкости.
* TALENT_BOOK_REQUIREMENTS - кол-во книг и их редкость для прокачки таланта.

4. Функции:
* generate_artifact_main_stat(artifact_id):
    * Назначение: Возвращает случайный основной стат для артефакта.
    * Параметры:
        * artifact_id - ID артефакта.
    * art_data = ITEM_DATA.get(artifact_id, {}) - берём всё информацию об артефакте.
    * possible_main = art_data.get("possible_main_stats", []) - получаем все возможные основные статы у артефактов. 
* load_weapon_growth():
    * Назначение: Загрузка данных прокачки оружия.
    * with open("assets/data/weapon_growth.json", "r", encoding="utf-8") as f: _weapon_growth_cache = json.load(f) - читаем и загружаем файл прокачки оружия.
* load_artifact_main_growth():
    * Назначение: Загрузка данных прокачки артефакта.
    * with open("assets/data/artifact_main_growth.json", "r", encoding="utf-8") as f: _artifact_main_growth_cache = json.load(f) - читаем и загружаем файл прокачки артефакта.
* get_artifact_main_stat_value(growth_key, level):
    * Назначение: Возвращает значение основного стата артефакта для заданного уровня.
    * Параметры:
        * growth_key – строка вида "slot_statname" (например, "plume_atk").
        * level – текущий уровень артефакта.
    * growth = load_artifact_main_growth() - загружает данные роста через load_artifact_main_growth().
    * stat_growth = growth.get(growth_key, {}) - из полученного словаря берёт запись для growth_key.
    * if level_str in stat_growth: return stat_growth[level_str] - пытается получить значение для переданного уровня и возвращает значение для него.
    * keys = [int(k) for k in stat_growth.keys() if k.isdigit()] and if not keys: return 0 and closest = max(k for k in keys if k <= level) - если его нет, ищет ближайший меньший уровень и возвращает значение для него.
    * return stat_growth[str(closest)] - возвращает значение стата.
* calculate_weapon_stats(weapon_id, level):
    * Назначение: Рассчитывает итоговые статы оружия на основе шаблона из ITEM_DATA и данных роста.
    * Параметры:
        * weapon_id – ID оружия. 
        * level – текущий уровень.
    * template = ITEM_DATA.get(weapon_id, {}) - получает шаблон оружия из ITEM_DATA.
    * base_atk = template.get("base_atk", 0), secondary = template.get("secondary_stat", {}), sec_base = secondary.get("value", 0), sec_stat = secondary.get("stat", "") - извлекает данные оружия.
    * growth_data = load_weapon_growth() - получает шаблон прокачки оружия.
    * growth = growth_data.get(growth_key, {}).get(str(level), {}) - берём данные из файла прокачки оружия.
    * atk_bonus = growth.get("atk_bonus", 0), sec_bonus = growth.get("secondary_bonus", 0) - ищет бонусы для данного weapon_id и уровня.
    * return {...} - суммирует базовые значения с бонусами и возвращает итоговое значение.

5. Класс Weapon:
* Функция init(self, name, weapon_type, rarity, base_atk):
    * Назначение: Представляет оружие как отдельный объект.
    * Параметры:
        * self - ссылка на объект.
        * name - имя оружия.
        * weapon_type - тип оружия.
        * rarity - редкость.
        * base_atk - базовая атака.
    * Атрибуты:
        * secondary_stat = None - второстепенные статы.
        * level = 1 - уровень.
        * max_level = 100 - максимальный уровень.
        * weapon_growth_data = {} - словарь с прокачкой оружия.
        * load_weapon_growth() - вызов функции.

6. Функции класса Weapon:
* Функция load_weapon_growth(self):
    * Назначение: Загружает JSON.
* Функция get_total_atk(self):
    * Назначение: Возвращает base_atk.
* Функция get_weapon_stats(self, weapon_id, level):
    * Назначение: Рассчитывает итоговые статы оружия на основе шаблона из ITEM_DATA и данных роста.
    * Параметры:
        * weapon_id – ID оружия. 
        * level – текущий уровень.
    * template = ITEM_DATA.get(weapon_id, {}) - получает шаблон оружия из ITEM_DATA.
    * base_atk = template.get("base_atk", 0), secondary = template.get("secondary_stat", {}), sec_base = secondary.get("value", 0), sec_stat = secondary.get("stat", "") - извлекает данные оружия.
    * growth_data = load_weapon_growth() - получает шаблон прокачки оружия.
    * growth = growth_data.get(growth_key, {}).get(str(level), {}) - берём данные из файла прокачки оружия.
    * atk_bonus = growth.get("atk_bonus", 0), sec_bonus = growth.get("secondary_bonus", 0) - ищет бонусы для данного weapon_id и уровня.
    * return {...} - суммирует базовые значения с бонусами и возвращает итоговое значение.

7. Класс Artifact:
* Функция init(self, slot, set_name, rarity, main_stat):
    * Назначение: Представляет артефакт как объект.
    * Параметры:
        * self - ссылка на объект.
        * slot - слот артефакта.
        * set_name - имя сета.
        * rarity - редкость.
        * main_stat - основной стат.
    * Атрибуты:
        * level = 0 - уровень.
        * sub_stats = [] - список второстепенных статов.

8. Класс Character:
* Функция init__(self, name, exp, exp_next, base_hp, base_atk, base_defense, portrait_path, crit_rate, crit_dmg, energy_recharge, elemental_mastery, phys_bonus, resistance, speed, talents=None):
    * Назначение: Представляет персонажа как объект.
    * Параметры:
        * self - ссылка на объект.
        * name - имя персонажа.
        * exp - кол-во опыта.
        * exp_next - нужное кол-во опыта для следующего уровня.
        * base_hp - базовое здоровье.
        * base_atk - базовая атака.
        * base_defense - базовая защита.
        * portrait_path - путь портрета персонажа.
        * crit_rate - шанс крита.
        * crit_dmg - крит урон.
        * energy_recharge - восстановление энергии.
        * elemental_mastery - мастерство стихий.
        * phys_bonus - бонус физического урона.
        * resistance - сопротивление.
        * speed - скорость.
        * talents=None - таланты.
    * Атрибуты:
        * self.level = 1 - уровень.
        * self.max_level = 10 - максимальный уровень.
        * self.talents = talents or {"normal": 1, "skill": 1, "burst": 1} - таланты.
        * self.constellation = 0 - уровень созвездия.
        * self.weapon = None - оружие.
        * self.artifacts = {...} - артефакты.
        * self.artifact_data = {} - данные артефакта.
        * self.weapon_data = {} - данные оружия.
        * self.load_growth_data() - вызов функции с загрузкой данных персонажа.

9. Функции класса Character:
* load_growth_data(self):
    * Назначение: Загружает JSON-файл с прибавками к статам на каждом уровне.
* calculate_total_stats(self):
    * Назначение: Вычисляет итоговые статы персонажа.
    * total = {...} - Создаёт словарь total с копией всех базовых статов.
    * uid_str = str(self.weapon) and weapon_data = self.weapon_data.get(uid_str, {}) - получаем UID оружия.
    * weapon_id = weapon_data.get("weapon_id") and level = weapon_data.get("level", 1) - получаем ID оружия и его уровень.
    * stats = calculate_weapon_stats(weapon_id, level) - вызываем пересчёт статы оружия.
    * total["atk"] += stats["atk"] - добавляем атаку с оружия к атаке персонажа.
    * for slot, uid in self.artifacts.items(): - проходим по каждому UID артефакта в каждом слоте.
    * data = self.artifact_data.get(uid_str, {}) - получаем данные артефакта через UID.
    * growth_key = data.get("growth_key") - получаем слот и его стат.
    * level = data.get("level", 0) - получаем уровень артефакта.
    * value = get_artifact_main_stat_value(growth_key, level) - определяем значение основного стата.
    * stat_name = growth_key.split('_', 1)[1] - определяем тип стата.
    * if stat_name: total["..."] += int(value) - добавляем значение основного стата.
    * for sub in data.get("sub_stats", []): sub_name = sub.get("stat") and sub_value = sub.get("value", 0) - перебираем все второстепенные статы и получаем нужные значения.
    * if sub_name: total["..."] += sub_value - добавляем значение второстепенного стата.
* add_exp(self, amount):
    * Назначение: Добавляет опыт и вызывает повышение уровня.
    * Параметры:
        * amount - кол-во опыта.
    * self.exp += amount - добавляем опыт.
    * while self.exp >= self.exp_next: self.exp -= self.exp_next and self.level_up() - когда кол-во опыта превышает нужное для следующего уровня кол-во опыта, вычитает нужное для следующего уровня кол-во опыта и повышаем уровень.
* level_up(self):
    * Назначение: Повышает уровень песонажа и увеличивает значение статов.
    * self.level += 1 - повышаем уровень.
    * growth = self.growth_data.get(str(self.level), {}) - получаем данные о прокачке персонажа.
    * self.name_stat += growth.get("...", 0) - увеличиваем значение статов.
    * self.exp_next = int(self.exp_next * 1.5) + 250 - увеличиваем значение exp_next.
* can_ascend(self):
    * Назначение: Проверяет находиться ли уровень в списке уровней для возвышения.
    * ascend_levels = [10, 20, 30, 40, 50, 60, 70, 80, 90] - список уровней для возвышения.
* ascend(self):
    * Назначение: Увеличивает max_level.
    * self.max_level += 10 - увеличивает максимальный уровень персонажа.
    * self.exp = 0 - обнуляет кол-во опыта.
* get_talent_max_level(self):
    * Назначение: Возвращает максимальный уровень таланта.
    * if self.max_level <= 10: return 2 - определяет максимальный уровень талантов зависимо от максимального уровня персонажа.
* get_talent_book_requirement(self, current_level):
    * Назначение: Возвращает (редкость, количество) книг для повышения таланта.
    * Параметры: 
        * current_level - текущий уровень.
* can_upgrade_talent(self, talent_name):
    * Назначение: Проверяет, не достигнут ли максимальный уровень для указанного таланта.
    * Параметры:
        * talent_name - имя таланта.
    * current_level = self.talents.get(talent_name, 1) - получаем текущий уровень.
    * max_level = self.get_talent_max_level() - получаем максимальный уровень.
    * return current_level < max_level - возвращает True если текущий уровень меньше максимального.
* activate_constellation(self):
    * Назначение: Увеличивает constellation.
    * if self.constellation >= 5: return False - проверка не достигнута ли последнее созвездие.
    * self.constellation += 1 - увеличивает созвездие на 1.
* equip_artifact(self, slot, uid):
    * Назначение: Экипирует артефакт на нужный слот.
    * Параметры:
        * slot - слот.
        * uid - UID артефакта.
    * uid_str = str(uid) - переводим UID в строку.
    * if uid_str not in self.artifact_data: return False - запрет на экипировку если нет такого UID в артефактах.
    * if slot not in self.artifacts: return False - запрет на экипировку если отсутствует указанный слот.
    * if self.artifacts[slot] is not None: self.unequip_artifact(slot) - снимает старый артефакт если слот не пустой.
    * self.artifacts[slot] = uid_str - экипирует артефакт если все проверки пройдены.
* unequip_artifact(self, slot):
    * Назначение: Снимает артефакт.
    * Параметры:
        * slot - слот.
    * if slot in self.artifacts and self.artifacts[slot] is not None: self.artifacts[slot] = None - делает слот пустым если слот существует и он не пустой.
* get_artifact_max_level(self, artifact_id):
    * Назначение: Возвращает максимальный уровень артефакта.
    * Параметры:
        * artifact_id - ID артефакта.
    * art_data = ITEM_DATA.get(artifact_id, {}) - получаем информацию об артефакте.
    * rarity = art_data.get("rarity", 1) - получаем редкость артефакта.
    * return MAX_ARTIFACT_LEVEL_BY_RARITY.get(rarity, 4) - возвращаем максимальный уровень артефакте.
* upgrade_artifact(self, uid, inventory):
    * Назначение: Улучшает артефакт.
    * Параметры: 
        * uid - уникальный номер артефакта.
        * inventory - ссылка на файл.
    * uid_str = str(uid) - переводим UID в строку.
    * if uid_str not in self.artifact_data: return False - запрет на прокачку при отсутствии UID в артефактах.
    * data = self.artifact_data[uid_str] - получаем информацию об артефакте по UID.
    * if "exp" not in data: data["exp"] = 0 - устанавливает значение exp при их отсутствии в записи.
    * artifact_id = data.get("artifact_id") - получаем все ID артефактов.
    * max_level = self.get_artifact_max_level(artifact_id) - получаем максимальный уровень артефакта.
    * if data.get("level", 0) >= max_level: return False - проверяет достиг ли артефакт максимального уровня.
    * exp_gain = ITEM_DATA.get("artifact_exp", {}).get("exp_gain", 50) - получаем кол-во флаконов опыта.
    * if inventory.get_count("artifact_exp") == 0: return False - возвращаем False если флаконов опыта нет.
    * inventory.remove_item("artifact_exp", 1) - вычитаем флакон опыта.
    * data["exp"] += exp_gain - добавляем опыт к артефакту.
    * while data["exp"] >= data["exp_next"]: data["exp"] -= data["exp_next"], data["level"] += 1, data["exp_next"] = int(data["exp_next"] * 1.5) + 50 - повышает уровень, вычитает лишний опыт и вычисляет exp_next.
    * if data["level"] in [4, 8, 12, 16, 20]: self._add_substat(data) - добавляет второстепенную характеристику при достижении определённого уровня.
* _add_substat(self, data):
    * Назначение: Добавляет второстепенную характеристику.
    * Параметры: 
        * data - словарь с данными конкретного артефакта.
    * template_id = data.get("artifact_id") - получаем ID артефактов.
    * art_data = ITEM_DATA.get(template_id, {}) - получаем данные артефактов по ID.
    * pool = art_data.get("possible_sub_stats", []) - получаем все возможные второстепенные статы для артефакта.
    * existing_names = {sub["stat"] for sub in data["sub_stats"]} - получаем кол-во второстепенных статов в артефакте.
    * available = [s for s in pool if s not in existing_names] - список из статов которых нет в существующих.
    * if available: new_stat_name = random.choice(available), new_value = self.get_initial_sub_stat_value(new_stat_name) - если список не пуст то тогда определяем какой стат будет добавлен и какое будет у него значение.
    * data["sub_stats"].append({"stat": new_stat_name, "value": new_value}) - добавляем новый второстепенный стат.
    * if data["sub_stats"]: sub_to_upgrade = random.choice(data["sub_stats"]) - если список второстепенных статов не пуст, то выбираем какой стат прокачать.
    * upgrade_amount = self.get_sub_stat_upgrade_amount(sub_to_upgrade["stat"]) - вызываем функцию для выбора значения, на которое увеличится стат.
    * sub_to_upgrade["value"] += upgrade_amount - увеличивает значение стата.
* get_initial_sub_stat_value(self, stat_name):
    * Назначение: Генерирует начальное значение для нового субстата.
    * Параметры:
        * stat_name - имя стата.
    * ranges = {...} - словарь со значениями статов.
    * low, high = ranges.get(stat_name, (1, 5))
    * return round(random.uniform(low, high), 1)
* get_sub_stat_upgrade_amount(self, stat_name):
    * Назначение: Возвращает прибавку к существующему субстату при его улучшении. 
    * Параметры:
        * stat_name - имя стата.
    * if "%" in stat_name: return round(random.uniform(0.5, 1.5), 1) - бафф если стат процентный.
    * else: return round(random.uniform(1, 5)) - бафф если стат без процентный.
* equip_weapon(self, uid):
    * Назначение: Экипирует оружие.
    * Параметры: 
        * uid - уникальный номер оружия.
    * uid_str = str(uid) - переводим UID в строку.
    * if uid_str in self.weapon_data: - проверяем существует ли оружие.
    * if self.weapon is not None: self.unequip_weapon() - если оружие уже экипировано, то вызывает функцию для снятия оружия.
    * self.weapon = uid_str - экипирует оружие.
* unequip_weapon(self):
    * Назначение: Снимает оружие.
    * if self.weapon is not None: self.weapon = None - если оружие экипировано, то тогда снимает его.
* upgrade_weapon(self, uid, inventory):
    * Назначение: Прокачка оружия.
    * Параметры:
        * uid - уникальный номер артефакта.
        * inventory - ссылка на файл.
    * uid_str = str(uid) - переводим UID в строку.
    * if uid_str not in self.weapon_data: return False - запрет на прокачку если UID нет среди оружий.
    * data = self.weapon_data[uid_str] - получаем информацию об оружии по UID.
    * if "exp" not in data: data["exp"] = 0 - устанавливает значение exp если его не было.
    * exp_gain = ITEM_DATA.get("crystal_of_true_power", {}).get("exp_gain", 50) - получаем кол-во кристаллов и их опыт.
    * if inventory.get_count("crystal_of_true_power") == 0: return False - запрет на прокачку если кристалов нет.
    * inventory.remove_item("crystal_of_true_power", 1) - тратим кристал.
    * data["exp"] += exp_gain - добавляем опыт.
    * while data["exp"] >= data["exp_next"]: data["exp"] -= data["exp_next"], data["level"] += 1, data["exp_next"] = int(data["exp_next"] * 1.5) + 50 - повышает уровень, вычитает лишний опыт и вычисляет exp_next.

### Файл camera:
1. Предназначение:
* Управляет камерой в игре: определяет, какая часть карты отображается на экране, обеспечивает следование за игроком и отрисовку только видимой области для оптимизации производительности.

2. Библиотеки:
* import pygame (Для работы с поверхностями и отрисовкой).

3. Класс Camera:
* Функция __init__(self, map_width, map_height, tile_size, screen_width, screen_height)
    * Назначение: Инициализирует камеру с параметрами карты и экрана, которая перемещается по карте и преобразует мировые координаты в экранные.
    * Параметры:
        * map_width – ширина карты в пикселях. 
        * map_height – высота карты в пикселях. 
        * tile_size – размер одного тайла в пикселях. 
        * screen_width – ширина окна в пикселях. 
        * screen_height – высота окна в пикселях. 
    * Атрибуты:
        * camera_x, camera_y – координаты левого верхнего угла камеры (в пикселях относительно карты).

4. Функции класса Camera:
* Функция update(self, target_rect):
    * Назначение: Обновляет позицию камеры, чтобы она следовала за целью (игроком), но не выходила за границы карты. 
    * Параметры:
        * target_rect – прямоугольник (pygame.Rect) игрока в мировых координатах. 
    * target_x = target_rect.centerx - self.screen_width // 2 – вычисляет желаемую позицию, чтобы игрок был в центре экрана по горизонтали. 
    * target_y = target_rect.centery - self.screen_height // 2 – аналогично по вертикали. 
    * self.camera_x = max(0, min(target_x, self.map_width - self.screen_width)) – ограничивает камеру, чтобы она не выходила за левую и правую границы карты. 
    * self.camera_y = max(0, min(target_y, self.map_height - self.screen_height)) – ограничивает по вертикали.
* Функция apply(self, rect):
    * Назначение: Преобразует мировые координаты объекта в экранные (с учётом смещения камеры). 
    * Параметры:
        * rect – прямоугольник объекта в мировых координатах. 
    * screen_rect = pygame.Rect(rect.x - self.camera_x, rect.y - self.camera_y, rect.width, rect.height) - вычисляет новый screen_rect.
* Функция draw_map(self, screen, map_data, tile_textures):
    * Назначение: Отрисовывает только видимую часть карты. 
    * Параметры:
        * screen – поверхность, на которой рисуем. 
        * map_data – двумерный список тайлов (список строк). 
        * tile_textures – словарь, где ключ – тип тайла (число), значение – поверхность Pygame (текстура). 
    * start_col = int(self.camera_x // self.tile_size) - начало колонки.
    * end_col = start_col + int(self.screen_width // self.tile_size) + 1 - конец колонки.
    * start_row = int(self.camera_y // self.tile_size) - начало строки.
    * end_row = start_row + int(self.screen_height // self.tile_size) + 1 - конец строки. 
    * start_col = max(0, start_col) and end_col = min(len(map_data[0]), end_col) - ограничения колонок.
    * start_row = max(0, start_row) and end_row = min(len(map_data), end_row) - ограничения строк.
    * for row in range(start_row, end_row): for col in range(start_col, end_col): - перебираем все строки и колонки. 
    * tile_type = map_data[row][col] – получает тип тайла. 
    * texture = tile_textures.get(tile_type) – получает текстуру. 
    * screen_x = col * self.tile_size - self.camera_x – экранная координата X. 
    * screen_y = row * self.tile_size - self.camera_y – экранная координата Y. 
    * screen.blit(texture, (screen_x, screen_y)) – отрисовывает тайл, если текстура существует.

### Файл resource_manager:
1. Предназначение:
* Централизованная загрузка и хранение игровых ресурсов (изображений, шрифтов, звуков). Состояния получают ресурсы через get_image().

2. Библиотеки:
* import pygame (Для загрузки текстур и шрифтов)

3. Класс ResourceManager:
* Функция init(self):
    * Назначение: Загружает все ресурсы и возвращает их по ключу.
    * Параметры:
        * self - ссылка на объект. 
    * Атрибуты:
        * self.images – словарь {ключ: поверхность Pygame}. 
        * self.fonts – словарь {ключ: объект шрифта}. 
        * self.sounds – словарь {ключ: звук}.

4. Функции класса ResourceManager:
* Функция load_image(self, path, key): 
    * Назначение: Загружает изображение.
    * Параметры:
        * path - путь к изображению.
        * key - ключ изображения.
    * try: self.images[key] = pygame.image.load(path).convert_alpha() - при отсутствии ошибки загружает изображение.
    * except (pygame.error, FileNotFoundError): surf = pygame.Surface((100, 100)) surf.fill((255, 0, 255)) self.images[key] = surf - при ошибке создаёт заглушку.
* Функция get_image(self, key): 
    * Назначение: Возвращает изображение по ключу.
    * Параметры:
        * key - ключ изображения.
* Функция load_font(self, path, size, key): 
    * Назначение: Загружает шрифт.
    * Параметры:
        * path - путь к шрифту.
        * size - размер шрифта.
        * key - ключ шрифта.
    * try: self.fonts[key] = pygame.font.Font(path, size) - при отсутствии ошибки загружает шрифт.
    * except (pygame.error, FileNotFoundError): self.fonts[key] = None - при ошибке сохраняет None.
* Функция get_font(self, key): 
    * Назначение: Возвращает шрифт или None.
    * * Параметры:
        * key - ключ шрифта.
* Функция load_all(self): 
    * Назначение: Загружает все ресурсы, используемые в игре.
    * self.load_image("...", "...") - загружает изображение и выдаёт ему ключ.

### Файл input_handler: 
1. Предназначение:
* Содержит статические методы для проверки состояния клавиш.

2. Библиотеки:
* import pygame (Использование констант событий).

3. Класс InputHandler:
* Назначение: Служит как набор вспомогательных функций для работы с вводом. 

4. Методы:
* @staticmethod - означает, что методы принадлежат классу, а не экземпляру. Их можно вызывать без создания объекта: InputHandler.is_key_pressed(...).

5. Функции класса InputHandler:
* is_key_pressed(events, key):
    * Назначение: Проверяет, было ли нажатие клавиши key среди списка событий events. Используется для обработки однократных нажатий.
    * Параметры:
        * events – список событий Pygame. 
        * key – код клавиши.
    * for event in events: - проходит по всем событиям в списке.
    * if event.type == pygame.KEYDOWN and event.key == key: - если находит событие типа pygame.KEYDOWN и его атрибут key совпадает с переданным, возвращает True.
* is_key_held(keys, key):
    * Назначение: Проверяет, зажата ли клавиша key в данный момент. Используется для постоянного удержания. 
    * Параметры:
        * keys – список, возвращённый pygame.key.get_pressed(). 
        * key – код клавиши.
    * return keys[key] - возвращает keys[key] — это булево значение, означающее, зажата ли клавиша в текущем кадре. 

***

## Файлы states:

### Файл init:

### Файл world_state:
1. Предназначение:
* Главное игровое состояние, в котором происходит весь геймплей на карте.

2. Библиотеки:
* import pygame (Для работы с текстурами)
* import json (Работа с данными персонажами)
* from camera import Camera (Работа с камерой)
* from input_handler import InputHandler (Обработка действий)

3. Класс WorldState:
* Функция init(self, game):
    * Назначение: Создание мира, переход во все остальные события и обработка передвижения персонажа.
    * Параметры:
        * self - ссылка на объект.
        * game – ссылка на главный объект игры (доступ к состояниям, ресурсам, игроку).
    * Атрибуты:
        * hero_rect – прямоугольник персонажа в мировых координатах. Координаты и размеры вычислены адаптивно (проценты от WIDTH и HEIGHT). 
        * item_rect – прямоугольник собираемого предмета (тестовый дубовый бревно). 
        * hint_font – шрифт для подсказки "Нажмите F". 
        * near_item – флаг, находится ли игрок рядом с предметом. 
        * item – флаг, существует ли предмет на карте (исчезает после сбора). 
        * tile_size – размер одного тайла в пикселях (50). 
        * direction – текущее направление персонажа ("right", "left", "back", "straight"). 
        * idle_frames – словарь со списками ключей спрайтов для стоячих анимаций (по направлениям). 
        * walk_frames – аналогично для ходьбы. 
        * idle_frames_index / self.walk_frames_index – текущий индекс кадра. 
        * idle_timer / self.walk_timer – таймеры для переключения кадров. 
        * idle_interval / self.walk_interval – интервалы смены кадров (в секундах). 
        * is_moving – флаг движения (используется для выбора анимации).
      
4. Функции класса WorldState:
* Метод on_enter(self):
    * Назначение: Загрузка всех нужных текстур и json файлов, а также создание объекта камеры.
    * with open("assets/maps/map.json", "r", encoding="utf-8") as f: map_json = json.load(f) - чтение json файла по карте.
    * self.map_data = map_json["data"] - получение данных карты.
    * map_width = len(self.map_data[0]) * self.tile_size - ширина карты.
    * map_height = len(self.map_data) * self.tile_size - высота карты.
    * self.camera = Camera(map_width, map_height, self.tile_size, self.game.WIDTH, self.game.HEIGHT) - создаём объект камеры.
    * self.tile_textures = {...} - загрузка тайлов карты.
    * self.item_img = self.game.resources.get_image("oak_wood") - загрузка предмета.
    * self.squad = self.game.resources.get_image("squad_list") - загрузка списка персонажей.
* Функция update(self, dt, events):
    * Назначение: Обработка всех событий в мире.
    * Параметры:
        * dt - время между кадрами.
        * events - все события.
    * if InputHandler.is_key_pressed(events, pygame.K_): self.game.change_state("...") - обработка событий для перехода на другое состояние.
    * if InputHandler.is_key_pressed(events, pygame.K_f): if self.near_item == True: self.game.player.inventory.add_item("oak_wood", 1) self.item = False - обработка события для получения события.
    * keys = pygame.key.get_pressed() - получаем нажатые клавиши.
    * if InputHandler.is_key_held(keys, pygame.K_): self.hero_rect -+= 5 self.is_moving = True - обработка события для передвижения персонажа.
    * if InputHandler.is_key_held(keys, pygame.K_): self.direction = "..." - смена текстуры при движении.
    * if not self.is_moving: self.idle_timer += dt - если персонаж стоит то добавляется время для смены позы персонажа. 
    * if self.idle_timer >= self.idle_interval: self.idle_frames_index = (self.idle_frames_index + 1) % len(self.idle_frames[self.direction]) self.idle_timer = 0.0 - если таймер равен или больше интервала то меняется поза персонажа и обнуляется таймер.
    * else: self.idle_frames_index = 0 self.idle_timer = 0.0 - если персонаж не стоит то тогда текстура и таймер обнуляется.
    * if self.is_moving: self.walk_timer += dt - если персонаж движется то добавляется время для смены позы персонажа. 
    * if self.walk_timer >= self.walk_interval: self.walk_frames_index = (self.walk_frames_index + 1) % len(self.walk_frames[self.direction]) self.walk_timer = 0.0 - если таймер равен или больше интервала то меняется поза персонажа и обнуляется таймер.
    * else: self.walk_frames_index = 0 self.walk_timer = 0.0 - - если персонаж не движется то тогда текстура и таймер обнуляется.
    * if self.hero_rect.colliderect(self.item_rect): self.near_item = True - если персонаж касается предмета то тогда его можно подобрать. 
* Функция draw(self, screen):
    * Назначение: Отрисовывает видимую часть карты через self.camera.draw_map().
    * Параметры:
        * screen - экран.
    self.camera.draw_map(screen, self.map_data, self.tile_textures) - отрисовываем карту.
    hero_screen_rect = self.camera.apply(self.hero_rect) - получаем размеры персонажа.
    if self.is_moving == False: frames = self.idle_frames[self.direction] key = frames[self.idle_frames_index] - смена текстуры стоя. 
    elif self.is_moving == True: frames = self.walk_frames[self.direction] key = frames[self.walk_frames_index] - смена текстуры идя. 
    player_sprite = self.game.resources.get_image(key) - получаем текстуру персонажа.
    if player_sprite: screen.blit(player_sprite, hero_screen_rect) - отрисовка игрока. 
    ramka = pygame.Rect(squad_x, squad_y, squad_width, squad_height) - размеры рамки отряда.
    screen.blit(self.squad, ramka) - отрисовываем рамку отряда.
    if self.item == True: item_screen_rect = self.camera.apply(self.item_rect) screen.blit(self.item_img, item_screen_rect) - если флаг истина то тогда предмет отрисовывается.
    if self.near_item == True and self.item == True: item_screen_rect = self.camera.apply(self.item_rect) - если персонаж касается предмета то выводится текст подсказка.
    hint_surf = self.hint_font.render("Нажмите F", True, (10, 10, 10)) - надпись и цвет текста.
    screen.blit(hint_surf, (hint_x, hint_y)) - отрисовка текста.

***

## Папка assets:

### Папка data:

#### Папка characters:

#### Папка dialogues:

### Папка font:

### Папка maps:

### Папка textures:

#### Папка buttons:

#### Папка tiles:

#### Папка inventory:


***

## Файл texture_colors: