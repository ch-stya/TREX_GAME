### Fichier contenant les classes de l'application ###

import pygame
from config import RED_COLOR, BLUE_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_MARGIN, GROUND_Y, BLACK_COLOR

class Player:
    def __init__(self, width=40, height=50, color=RED_COLOR):
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
        self.current_frame = 0

        # Animation run player
        spritesheet = pygame.image.load("assets/catgray/64x64/2d/run.png").convert_alpha()
        frame_width = spritesheet.get_width() // 7
        frame_height = spritesheet.get_height()
        self.frames = []
        for i in range(7):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame_image = spritesheet.subsurface(rect)
            self.frames.append(frame_image)
        
    def draw(self, surface):
        #pygame.draw.rect(surface, self.color, self.rect)
        if self.current_frame < len(self.frames)-1:
            self.current_frame +=0.3
        else :
            self.current_frame = 0
        surface.blit(self.frames[int(self.current_frame)], self.rect)

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

class Score:
    def __init__(self, score=0):
        self.score = score
        self.best = 0
        self.last_update_time = 0
        # score
        self.score_font = pygame.font.Font(None, 30)  
        self.score_text = self.score_font.render("Score : " + str(self.score), True, BLACK_COLOR) 
        self.score_text_rect = self.score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//9))
        # meilleur score
        self.best_font = pygame.font.Font(None, 20) 
        self.best_text = self.best_font.render("Best : " + str(self.best), True, BLACK_COLOR) 
        self.best_text_rect = self.best_text.get_rect(center=(SCREEN_WIDTH-SCREEN_WIDTH//8, SCREEN_HEIGHT-SCREEN_HEIGHT//11))

    def draw(self, surface):
        # Affichage score actuel
        self.score_text = self.score_font.render("Score : " + str(self.score), True, BLACK_COLOR) 
        surface.blit(self.score_text, self.score_text_rect)
        # Affichage meilleur score
        self.best_text = self.best_font.render("Best : " + str(self.best), True, BLACK_COLOR) 
        surface.blit(self.best_text, self.best_text_rect)

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.last_update_time+100 < current_time :
            self.score += 1
            self.last_update_time = current_time

    def add(self, bonus):
        self.score += bonus

    def reset(self):
        self.score = 0
        self.last_update_time = pygame.time.get_ticks()

    def update_best(self):
        if self.score > self.best :
            self.best = self.score