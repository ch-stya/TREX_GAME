### Fichier contenant les classes de l'application ###

import pygame
from config import RED_COLOR, BLUE_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_MARGIN, GROUND_Y

class Player:
    def __init__(self, width=10, height=20, color=RED_COLOR):
        self.width = width
        self.height = height
        self.color = color
        # Création du rectangle à la bonne position
        self.rect = pygame.Rect(
            (SCREEN_WIDTH - self.width) // 5, # x, un peu sur la gauche
            GROUND_Y - self.height, # y, sur le sol et en déduisant la taille de l'objet car coord x,y se trouvent en haut à gauche
            self.width, # width
            self.height) # height
        self.gravity = 0
        self.jump_strength = -17
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def jump(self):
        # Saut seulement si le joueur est au sol
        # rect.bottom regarde les coordonnées sur le bas du rectangle plutôt qu'en haut à gauche avec rect
        if self.rect.bottom == GROUND_Y :
            self.gravity = self.jump_strength

    def apply_gravity(self):
        # Appliquer la gravité 
        self.gravity += 1
        self.rect.y += self.gravity

        # Empêcher de passer à travers le sol
        if self.rect.bottom >= GROUND_Y :
            self.rect.bottom = GROUND_Y
            self.gravity = 0

    def reset(self):
        # Reset de la position
        self.rect.x = (SCREEN_WIDTH - self.width) // 5
        self.rect.y = GROUND_Y - self.height
        self.gravity = 0

class Obstacle:
    def __init__(self, width=30, height=30, color=BLUE_COLOR, speed=5):
        self.width = width # largeur
        self.height = height # hauteur
        self.color = color # couleur
        self.speed = speed # vitesse
        # Création du rectangle à la bonne position (x fixe, y ajusté via bottom)
        self.rect = pygame.Rect(
            SCREEN_WIDTH, # x, tout à droite légérement en dehors de la fenêtre
            GROUND_Y - self.height, # y, sur le sol et en déduisant la taille de l'objet car coord x,y se trouvent en haut à gauche
            self.width, # width
            self.height) # height

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self):
        # Déplacement de l'obstacle vers la gauche
        if self.rect.right < 0 :
            self.rect.x = SCREEN_WIDTH 
        else :
            self.rect.x -= self.speed
            
    def reset(self):
        # Reset de la position
        self.rect.x = SCREEN_WIDTH
        self.rect.y = GROUND_Y - self.height