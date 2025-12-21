# Wrapper class to handle all globally shared stuff

import pygame

class Screen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

    def stop(self):
        pygame.quit()
        exit(0)
