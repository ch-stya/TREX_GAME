### Fichier contenant les classes de l'application ###

import pygame
from config import RED_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_MARGIN

class Player:
    def __init__(self, width=10, height=20, color=RED_COLOR):
        self.width = width
        self.height = height
        self.color = color
        # Création du rectangle à la bonne position (x fixe, y ajusté via bottom)
        self.rect = pygame.Rect(
            (SCREEN_WIDTH - self.width) // 5, # x, un peu sur la gauche
            0, # y
            self.width, # width
            self.height) # height
        self.rect.bottom = SCREEN_HEIGHT - GROUND_MARGIN # ajustement du y

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)