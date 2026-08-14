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

3. Функция def main():
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
    * if item_type == "resources": - если предмет типа "resources" – увеличивает количество в self.items (или создаёт новую запись) и возвращает None.
    * elif item_type in ["artifacts", "weapons"]: - если предмет типа "artifacts" или "weapons" – генерирует новый UID (self.uid_counter += 1), добавляет UID в список для этого item_id и возвращает UID.
    * self.modified = True - меняет флаг изменений.
* Функция remove_item(self, item_id, uid=None):
    * Название: Удаляет предмет из инвентаря. 
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

### Файл input_handler: 
1. Предназначение:
* Содержит статические методы для проверки состояния клавиш.

2. Библиотеки:
* import pygame (Использование констант событий)

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

### Файл init.py:


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

#### Папка Инвентарь:


***

## Файл texture_colors: