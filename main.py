import pygame
from pygame import FULLSCREEN, SCALED

from game import Game

def main():
    # 1. Инициализация pygame
    pygame.init()

    # 2. Настройки окна (размеры, название)
    info = pygame.display.Info()
    WIDTH = info.current_w
    HEIGHT = info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
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
        dt = min(dt, 0.05)

        # Получаем все события от Pygame
        events = pygame.event.get()

        # Проверяем, не закрыто ли окно
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                    game.save_all()

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