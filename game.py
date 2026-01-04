### Definition des éléments nécessaire et fonctionnement du jeu ###

import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS, GREEN_COLOR, IMG_PATHS, SKINS
from entities import Player, Obstacle, Score, GameManager
from utils import draw_game_over_screen, draw_start_screen, convert_img

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        # --- CHARGEMENT DES ASSETS ---
        self.assets = {}
        for name, data in IMG_PATHS.items():
            if isinstance(data, dict):
                self.assets[name] = {
                    'img': pygame.image.load(data['img']).convert_alpha(),
                    'hitbox_factor': data['hitbox_factor']
                }
            else :
                self.assets[name] = pygame.image.load(data).convert_alpha()
        # --- CHARGEMENT DES SKINS ---
        self.skins = {}
        for name, data in SKINS.items():
            self.assets[name] = {
                'run': pygame.image.load(data['run']).convert_alpha(),
                'idle': pygame.image.load(data['idle']).convert_alpha(),
                'jump': pygame.image.load(data['jump']).convert_alpha(),
            }

        pygame.display.set_icon(self.assets['icon']) # icone du jeu

        # à transformer en un groupe de sprites
        # On crée le groupe d'obstacles vide
        self.obstacles_group = pygame.sprite.Group()
        self.obstacle_types = ['yarn', 'big_box', 'small_box']

        self.game_manager = GameManager()
        self.score = Score() # gérer le score dans le GameManager ?
        self.player = Player("grey")
        self.running = True
        self.game_over = False
        self.start = False  
        self.debug = False  

    def spawn_obstacle(self):
        # Quand on crée un obstacle, on lui DONNE l'image chargée
        # Plus besoin de charger dans l'obstacle !
        #nouveau_box = Box(x=800, y=300, image=self.assets['box'])
        #self.obstacles.add(nouveau_box)
        obstacle = random.choice(self.obstacle_types)
        new_obstacle = Obstacle(img=self.assets[obstacle]['img'], hitbox_factor=self.assets[obstacle]['hitbox_factor'])
        self.obstacles_group.add(new_obstacle)

    @staticmethod
    def collision_par_hitbox(sprite1, sprite2):
        # On vérifie si la hitbox du sprite 1 touche la hitbox du sprite 2
        return sprite1.hitbox.colliderect(sprite2.hitbox)

    def run(self):
        while self.running :
            for event in pygame.event.get():
                # Detection de clic sur la croix pour fermer l'app
                if (event.type == pygame.QUIT):
                    self.running = False
                # Detection d'une touche pressée pendant que la partie est en cours
                elif (event.type == pygame.KEYDOWN and not self.game_over and self.start):
                    # Detection de la touche espace
                    if event.key == pygame.K_SPACE:
                        # Action : jump du joueur
                        self.player.jump()      
                # Detection d'une touche pressée pendant que la partie est en game over
                elif (event.type == pygame.KEYDOWN and self.game_over and self.start):
                    # Detection de la touche R
                    if event.key == pygame.K_r:
                        # Action : reset des éléments et restart la game
                        self.game_over = False
                        self.player.reset()
                        self.score.reset()
                        self.obstacles_group.empty()
                        self.start = False
                # Detection d'une touche pressée pendant l'écran de démarrage
                elif (event.type == pygame.KEYDOWN and not self.start and not self.game_over):
                    # Detection de la touche espace
                    if event.key == pygame.K_SPACE:
                        # Action : lance une partie
                        self.start = True
                        self.player.set_state("run")
                # Detection d'une touche pressée à n'importe quel moment
                if (event.type == pygame.KEYDOWN) :
                    # Detection de la touche D
                    if event.key == pygame.K_d:
                        # activation/désactivation du mode debug
                        self.debug = not self.debug
        
            if not self.game_over and self.start : 
                # update des positions
                self.obstacles_group.update(self.game_manager.speed)
                self.player.apply_gravity()
                self.score.update()
                # test de collision entre hitbox joueur et hiotbox obstacle
                if pygame.sprite.spritecollideany(self.player, self.obstacles_group, collided=Game.collision_par_hitbox):
                    self.game_over = True
                # création aléatoire des obstacles
                if len(self.obstacles_group) == 0:
                    self.spawn_obstacle()

            # draw
            self.screen.fill(GREEN_COLOR)
            self.obstacles_group.draw(self.screen)
            self.player.draw(self.screen)
            self.score.draw(self.screen)

            if self.debug :
                # Affichage des hitbox
                self.player.draw_hitbox(self.screen)
                for obstacle in self.obstacles_group:
                    obstacle.draw_hitbox(self.screen)

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
