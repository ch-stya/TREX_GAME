### Definition des éléments nécessaire et fonctionnement du jeu ###

import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS, GREEN_COLOR, IMG_PATHS
from entities import Player, Obstacle, Score, Yarn, Big_Box, Small_Box, GameManager
from utils import draw_game_over_screen, draw_start_screen, convert_img

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        # --- CHARGEMENT DES ASSETS (Une seule fois !) ---
        self.assets = {}
        for name, path in IMG_PATHS.items():
            # C'est ici qu'on charge et convertit
            self.assets[name] = pygame.image.load(path).convert_alpha()
        #self.skins = {}

        pygame.display.set_icon(self.assets['icon']) # icone du jeu

        # à transformer en un groupe de sprites
        self.obstacles_classes = [Yarn, Big_Box, Small_Box]
        self.obstacle = random.choice(self.obstacles_classes)()

        self.game_manager = GameManager()
        self.score = Score() # gérer le score dans le GameManager ?
        self.player = Player("grey")
        self.running = True
        self.game_over = False
        self.start = False    

    def spawn_obstacle(self):
        # Quand on crée un obstacle, on lui DONNE l'image chargée
        # Plus besoin de charger dans l'obstacle !
        #nouveau_box = Box(x=800, y=300, image=self.assets['box'])
        #self.obstacles.add(nouveau_box)
        pass

    def run(self):
        while self.running :
            for event in pygame.event.get():
                # Detection de clic sur la croix pour fermer l'app
                if (event.type == pygame.QUIT):
                    self.running = False
                # Detection d'une touche pressé
                elif (event.type == pygame.KEYDOWN and not self.game_over and self.start):
                    # Detection de la touche espace
                    if event.key == pygame.K_SPACE:
                        self.player.jump()      
                elif (event.type == pygame.KEYDOWN and self.game_over and self.start):
                    # Detection de la touche R pour relancer une partie en cas de game over
                    if event.key == pygame.K_r:
                        self.game_over = False
                        self.obstacle.reset()
                        self.player.reset()
                        self.score.reset()
                        self.start = False
                elif (event.type == pygame.KEYDOWN and not self.start and not self.game_over):
                    if event.key == pygame.K_SPACE:
                        self.start = True
                        self.player.set_state("run")
        
            if not self.game_over and self.start : 
                # update des positions
                self.obstacle.update(self.game_manager.speed)
                self.player.apply_gravity()
                self.score.update()
                # test de collision entre hitbox joueur et obstacle
                if self.player.hitbox.colliderect(self.obstacle.hitbox):
                    self.game_over = True
                # création aléatoire d'un obstacle
                if self.obstacle.on_screen is False :
                    self.obstacle = random.choice(self.obstacles_classes)()
                    self.obstacle.reset()

            # draw
            self.screen.fill(GREEN_COLOR)
            self.obstacle.draw(self.screen)
            self.player.draw(self.screen)
            self.score.draw(self.screen)
            #obstacle.draw_hitbox(screen)
            #player.draw_hitbox(screen)

            if self.game_over :
                self.player.reset()
                self.player.set_state("idle")
                self.score.update_best() # maj du meilleur score retenu
                draw_game_over_screen(self.screen)
            elif not self.start :
                draw_start_screen(self.screen)
                self.player.set_state("idle")

            pygame.display.flip() # maj affichage
            self.clock.tick(FPS)
        pygame.quit()
