import pygame

class Camera:
    def __init__(self, map_width, map_height, tile_size, screen_width, screen_height):
        self.camera_x = 0
        self.camera_y = 0
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = tile_size
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, target_rect):
        target_x = target_rect.centerx - self.screen_width // 2
        target_y = target_rect.centery - self.screen_height // 2
        self.camera_x = max(0, min(target_x, self.map_width - self.screen_width))
        self.camera_y = max(0, min(target_y, self.map_height - self.screen_height))

    def apply(self, rect):
        screen_rect = pygame.Rect(rect.x - self.camera_x, rect.y - self.camera_y, rect.width, rect.height)
        return screen_rect

    def draw_map(self, screen, map_data, tile_textures):
        start_col = int(self.camera_x // self.tile_size)
        end_col = start_col + int(self.screen_width // self.tile_size) + 1
        start_row = int(self.camera_y // self.tile_size)
        end_row = start_row + int(self.screen_height // self.tile_size) + 1
        start_col = max(0, start_col)
        end_col = min(len(map_data[0]), end_col)
        start_row = max(0, start_row)
        end_row = min(len(map_data), end_row)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                tile_type = map_data[row][col]
                texture = tile_textures.get(tile_type)
                screen_x = col * self.tile_size - self.camera_x
                screen_y = row * self.tile_size - self.camera_y
                if texture:
                    screen.blit(texture, (screen_x, screen_y))