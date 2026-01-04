### Fichier contenant les classes de l'application ###

import pygame
from config import RED_COLOR, BLUE_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_MARGIN, GROUND_Y, BLACK_COLOR, SKINS

class GameManager:
    def __init__(self):
        # Attributs pour la gestion du score
        self.score = 0
        self.highest_score = 0
        self.last_score_update = 0

        self.speed = 5.0
        self.min_gap = 0
        self.max_gap = 500

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_score_update > 100:
            self.score += 1
            self.last_score_update = current_time

            # Tous les 200 points on augmente la vitesse
            if self.score % 200 == 0:
                self.speed += 0.3
                print(f"Speed up! {self.speed}")

            self.calcul_gaps()


    def calcul_gaps(self):
        # MAJ de l'écart minimum entre 2 obstacles
        if self.score < 200 :
            self.min_gap = int(250)
            self.max_gap = 600
        elif self.score >= 200 and self.score <= 300 :
            self.min_gap = int(120 + self.speed*10)
            self.max_gap = self.min_gap + 300
        elif self.score > 300 and self.score <= 600 :
            self.min_gap = int(120 + self.speed*10)
            self.max_gap = self.min_gap + 250
        elif self.score > 600 and self.score <= 1400 :
            self.min_gap = int(120 + self.speed*15)
            self.max_gap = self.min_gap + 150
        else :
            self.min_gap = int(120 + self.speed*20)
            self.max_gap = self.min_gap + 150
            

    def get_max_obstacles(self):
        if self.score < 100 :
            # Level 1, un seul obstacle à la fois
            return 1
        elif self.score < 400 :
            # Level 2, 2 obstacles maxi à la fois
            return 2 
        else :
            # Pas de limite, l'écran se charge de la limitation
            return 10

    def update_highest_score(self):
        if self.score > self.highest_score :
            self.highest_score = self.score
            # sauvegarde dans un fichier à terme

    def reset(self):
        self.score = 0
        self.speed = 5.0
        self.last_score_update = pygame.time.get_ticks()
        self.calcul_gaps()


class ScoreUI:
    def __init__(self):
        # score
        self.score_font = pygame.font.Font(None, 30)  
        self.highest_font = pygame.font.Font(None, 20) 

        self.score_surface = None
        self.highest_surface = None

        self.last_known_score = -1
        self.last_known_highest = -1

    def draw(self, surface, game_manager):
        # --- OPTIMISATION ---
        if game_manager.score != self.last_known_score:
            self.score_surface = self.score_font.render(f"Score : {game_manager.score}", True, BLACK_COLOR)
            self.last_known_score = game_manager.score
            
        if game_manager.highest_score != self.last_known_highest:
            self.highest_surface = self.highest_font.render(f"Best : {game_manager.highest_score}", True, BLACK_COLOR)
            self.last_known_highest = game_manager.highest_score

        # --- AFFICHAGE ---
        if self.score_surface:
            rect = self.score_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//9))
            surface.blit(self.score_surface, rect)
            
        if self.highest_surface:
            rect_highest = self.highest_surface.get_rect(center=(SCREEN_WIDTH-SCREEN_WIDTH//8, SCREEN_HEIGHT-SCREEN_HEIGHT//11))
            surface.blit(self.highest_surface, rect_highest)

class UIManager:
    def __init__(self):
        # --- ECRAN GAME OVER ---
        self.game_over_font = pygame.font.Font(None, 74)  # None = police par défaut, 74 = taille
        self.game_over_surface = self.game_over_font.render("GAME OVER", True, RED_COLOR)
        self.game_over_rect = self.game_over_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

        self.replay_font = pygame.font.Font(None, 30)
        self.replay_surface = self.replay_font.render("Press 'R' to restart", True, BLACK_COLOR)
        self.replay_rect = self.replay_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))

        # --- ECRAN DEMARRAGE
        self.start_font = pygame.font.Font(None, 50)
        self.start_surface = self.start_font.render("Press 'Space' to start", True, BLACK_COLOR)
        self.start_rect = self.start_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    
    def draw_game_over(self, surface):
        """
        Fonction permettant d'afficher l'écran de game over.

        :param surface: objet pygame.display
        """
        surface.blit(self.game_over_surface, self.game_over_rect)
        surface.blit(self.replay_surface, self.replay_rect)


    def draw_start(self, surface):
        """
        Fonction permettant d'afficher l'écran de démarrage.

        :param surface: objet pygame.display
        """
        surface.blit(self.start_surface, self.start_rect)

class Player:
    def __init__(self, assets):
        self.assets = assets
        self.hitbox_factor = 1.6 # facteur de réduction de la hitbox par rapport à la frame originale
        # Animation run player
        self.run_frames = assets['run']
        self.run_width = self.run_frames[0].get_width()
        self.run_height = self.run_frames[0].get_height()
        # Animation idle player
        self.idle_frames = assets['idle']
        self.idle_width = self.idle_frames[0].get_width()
        self.idle_height = self.idle_frames[0].get_height()
        # Animation jump up player
        self.jump_up_frames = assets['jump_up']
        self.jump_up_width = self.jump_up_frames[0].get_width()
        self.jump_up_height = self.jump_up_frames[0].get_height()
        # Animation jump down player
        self.jump_down_frames = assets['jump_down']
        self.jump_down_width = self.jump_down_frames[0].get_width()
        self.jump_down_height = self.jump_down_frames[0].get_height()

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
        self.hitbox = self.rect.inflate(-self.idle_width//self.hitbox_factor, 0)

        #print(self.run_width, self.idle_width)
        
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
            self.hitbox = self.rect.inflate(-self.run_width//self.hitbox_factor, 0)
        elif self.state == "idle" :
            self.rect.height = self.idle_height
            self.rect.width = self.idle_width
            self.frames = self.idle_frames
            self.frame_speed = 0.1
            self.hitbox = self.rect.inflate(-self.idle_width//self.hitbox_factor, 0)
        elif self.state == "jump_up" : # vers le haut
            self.rect.height = self.jump_up_height
            self.rect.width = self.jump_up_width
            self.frames = self.jump_up_frames
            self.frame_speed = 0.2
            self.hitbox = self.rect.inflate(-self.jump_up_width//self.hitbox_factor, 0)
        elif self.state == "jump_down" : # vers le bas
            self.rect.height = self.jump_down_height
            self.rect.width = self.jump_down_width
            self.frames = self.jump_down_frames
            self.frame_speed = 0.3
            self.hitbox = self.rect.inflate(-self.jump_down_width//self.hitbox_factor, 0)
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

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, img=None, hitbox_factor=2, width=60, height=60):
        super().__init__()
        if img == None :
            # Image fictive s'il n'y en a pas
            self.image = pygame.Surface((width, height))
            self.image.fill(BLUE_COLOR)
            self.width = width # largeur
            self.height = height # hauteur
        else :
            self.image = img
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        # Création du rectangle à la bonne position (x fixe, y ajusté via bottom)
        self.rect = pygame.Rect(
            SCREEN_WIDTH, # x, tout à droite légérement en dehors de la fenêtre
            GROUND_Y - self.height, # y, sur le sol et en déduisant la taille de l'objet car coord x,y se trouvent en haut à gauche
            self.width, # width
            self.height) # height
        self.hitbox = self.rect.inflate(-self.width//hitbox_factor, 0)
        self.on_screen = False

    """
    # Pas de méthode draw, c'est Sprite qui la reprend
    def draw(self, surface):
        self.update_hitbox()
        if self.image == None :
            pygame.draw.rect(surface, BLUE_COLOR, self.rect)
        else :
            surface.blit(self.image, self.rect)"""

    def update(self, current_speed):
        # Déplacement de l'obstacle vers la gauche
        self.rect.x -= int(current_speed)
        self.update_hitbox()
        self.current_pos()

    def current_pos(self):
        if self.rect.x < -self.width  or self.rect.x > SCREEN_WIDTH :
            self.kill()
            self.on_screen = False
        else :
            self.on_screen = True
            
    def reset(self):
        self.kill()

    def update_hitbox(self):
        self.hitbox.center = self.rect.center

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)