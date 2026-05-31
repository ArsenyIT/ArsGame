import pygame
class InputHandler:
    @staticmethod
    def is_key_pressed(events, key):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == key:
                return True
        return False

    @staticmethod
    def is_key_held(keys, key):
        return keys[key]