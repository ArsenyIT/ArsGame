import pygame
from game import Game

def main():
    # 1. Инициализация pygame
    pygame.init()

    # 2. Настройки окна (размеры, название)
    WIDTH = 1366  # можешь изменить на свой размер
    HEIGHT = 708
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ArsGame")

    # 3. Часы для ограничения FPS
    clock = pygame.time.Clock()

    # 4. Создаём объект игры
    game = Game(screen, WIDTH, HEIGHT)

    # 5. Главный цикл
    running = True
    while running:
        # Ограничение до 60 кадров в секунду, dt — время в секундах между кадрами
        dt = clock.tick(60) / 1000.0

        # Получаем все события от Pygame
        events = pygame.event.get()

        # Проверяем, не закрыто ли окно
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Обновление игровой логики
        game.update(dt, events)

        # Отрисовка
        game.draw(screen)

        # Показываем нарисованное на экране
        pygame.display.flip()
        # Сохранение всех данных
        game.save_all()

    # 6. Завершение работы
    game.save_all()
    pygame.quit()

if __name__ == "__main__":
    main()