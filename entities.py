### Fichier contenant les classes de l'application ###

import pygame
from config import RED_COLOR, BLUE_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_MARGIN, GROUND_Y, BLACK_COLOR
from utils import convert_spritesheet

class Player:
    def __init__(self):
        # Animation run player
        self.run_frames, self.run_height, self.run_width = convert_spritesheet("assets/catgray/64x64/2d/run.png", 7)
        # Animation idle player
        self.idle_frames, self.idle_height, self.idle_width = convert_spritesheet("assets/catgray/64x64/2d/idle.png", 7)
        # Animation jump up player
        self.jump_up_frames, self.jump_up_height, self.jump_up_width = convert_spritesheet("assets/catgray/64x64/2d/jump.png", 7, 0, 3)
        # Animation jump down player
        self.jump_down_frames, self.jump_down_height, self.jump_down_width = convert_spritesheet("assets/catgray/64x64/2d/jump.png", 7, 3, 6)

        # Création du rectangle à la bonne position
        self.rect = pygame.Rect(
            (SCREEN_WIDTH - self.idle_width) // 5, # x, un peu sur la gauche
            GROUND_Y - self.idle_height, # y, sur le sol et en déduisant la taille de l'objet car coord x,y se trouvent en haut à gauche
            self.idle_width, # width
            self.idle_height) # height
        
        self.frames = self.idle_frames # Set de frame actuel
        self.gravity = 0
        self.jump_strength = -11
        self.current_frame = 0
        self.state = "idle"
        self.frame_speed = 0.1 # Vitesse entre les frames de l'animation
        self.hitbox = self.rect.inflate(-self.idle_width//2, 0)
        
    def draw(self, surface):
        #pygame.draw.rect(surface, RED_COLOR, self.rect)
        if self.current_frame < len(self.frames)-1 :
            self.current_frame += self.frame_speed
        elif self.current_frame >= len(self.frames)-1 and self.state in ("jump_up", "jump_down") :
            self.current_frame = len(self.frames)-1
        else :
            self.current_frame = 0
        surface.blit(self.frames[int(self.current_frame)], self.rect)

    def set_state(self, state):
        if self.state != state :
            self.current_frame = 0
        self.state=state
        bottom = self.rect.bottom # garder le bas du joueur constant
        if self.state == "run" :
            self.rect.height = self.run_height
            self.rect.width = self.run_width
            self.frames = self.run_frames
            self.frame_speed = 0.3
            self.hitbox = self.rect.inflate(-self.run_width//2, 0)
        elif self.state == "idle" :
            self.rect.height = self.idle_height
            self.rect.width = self.idle_width
            self.frames = self.idle_frames
            self.frame_speed = 0.1
            self.hitbox = self.rect.inflate(-self.idle_width//2, 0)
        elif self.state == "jump_up" : # vers le haut
            self.rect.height = self.jump_up_height
            self.rect.width = self.jump_up_width
            self.frames = self.jump_up_frames
            self.frame_speed = 0.2
            self.hitbox = self.rect.inflate(-self.jump_up_width//2, 0)
        elif self.state == "jump_down" : # vers le bas
            self.rect.height = self.jump_down_height
            self.rect.width = self.jump_down_width
            self.frames = self.jump_down_frames
            self.frame_speed = 0.3
            self.hitbox = self.rect.inflate(-self.jump_down_width//2, 0)
        self.rect.bottom = bottom # repositionner le bas à sa position d'origine
        self.update_hitbox()

    def update_hitbox(self):
        self.hitbox.center = self.rect.center

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)

    def jump(self):
        # Saut seulement si le joueur est au sol
        # rect.bottom regarde les coordonnées sur le bas du rectangle plutôt qu'en haut à gauche avec rect
        if self.rect.bottom == GROUND_Y :
            self.gravity = self.jump_strength

    def apply_gravity(self):
        # Appliquer la gravité 
        self.gravity += 0.5
        self.rect.y += self.gravity
        self.update_hitbox()

        # Empêcher de passer à travers le sol
        if self.rect.bottom >= GROUND_Y :
            self.rect.bottom = GROUND_Y
            self.gravity = 0
            self.set_state("run")
        else :
            if self.gravity < 0 :
                self.set_state("jump_up")
            elif self.gravity > 1 :
                self.set_state("jump_down")
        

    def reset(self):
        # Reset de la position
        self.rect.height = self.idle_height
        self.rect.width = self.idle_width
        self.rect.x = (SCREEN_WIDTH - self.idle_width) // 5
        self.rect.y = GROUND_Y - self.idle_height
        self.gravity = 0

class Obstacle:
    def __init__(self, width=30, height=30, type='yarn', speed=5):
        self.width = width # largeur
        self.height = height # hauteur
        self.type = type # type d'objet
        self.speed = speed # vitesse
        # Création du rectangle à la bonne position (x fixe, y ajusté via bottom)
        self.rect = pygame.Rect(
            SCREEN_WIDTH, # x, tout à droite légérement en dehors de la fenêtre
            GROUND_Y - self.height, # y, sur le sol et en déduisant la taille de l'objet car coord x,y se trouvent en haut à gauche
            self.width, # width
            self.height) # height
        if self.type == 'yarn' :
            self.img = pygame.image.load("assets/objects/pink_yarn(32x32).png").convert_alpha()
    

    def draw(self, surface):
        #pygame.draw.rect(surface, BLUE_COLOR, self.rect)
        surface.blit(self.img, self.rect)

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