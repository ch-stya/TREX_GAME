### Definition des éléments nécessaire et fonctionnement du jeu ###

import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS, GREEN_COLOR, IMG_PATHS, SKINS
from entities import Player, Obstacle, GameManager, ScoreUI, UIManager
from utils import convert_img, convert_spritesheet, scale_frames

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_assets()
        self.init_objects()
        pygame.display.set_icon(self.assets['icon']) # icone du jeu

        self.running = True
        self.game_over = False
        self.start = False  
        self.debug = False

    def load_assets(self):
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
        SCALE_FACTOR = 2
        for name, data in SKINS.items():
            self.skins[name] = {}
            run_frames = convert_spritesheet(data['run'], 7)[0]
            idle_frames = convert_spritesheet(data['idle'], 7)[0]
            jump_up_frames = convert_spritesheet(data['jump'], 7, start=0, end=3)[0]
            jump_down_frames = convert_spritesheet(data['jump'], 7, start=3, end=6)[0]
            self.skins[name]['run'] = scale_frames(run_frames, SCALE_FACTOR)
            self.skins[name]['idle'] = scale_frames(idle_frames, SCALE_FACTOR)
            self.skins[name]['jump_up'] = scale_frames(jump_up_frames, SCALE_FACTOR)
            self.skins[name]['jump_down'] = scale_frames(jump_down_frames, SCALE_FACTOR)

    def init_objects(self):
        self.game_manager = GameManager()
        self.score_ui = ScoreUI()
        self.ui_manager = UIManager()
        self.player = Player(self.skins["grey"])
        # On crée le groupe d'obstacles
        self.obstacles_group = pygame.sprite.Group()
        # Liste des obstacles possibles
        self.obstacle_types = ['yarn', 'big_box', 'small_box']  

    def handle_input(self):
        """
        Gère toutes les entrées utilisateur (clavier/souris)
        
        :param self:
        """
        for event in pygame.event.get():
                # Detection de clic sur la croix pour fermer l'app
                if (event.type == pygame.QUIT):
                    self.running = False

                # Detection d'une touche pressée
                elif (event.type == pygame.KEYDOWN) :
                    # - Detection de la touche D -
                    if event.key == pygame.K_d:
                        # activation/désactivation du mode debug
                        self.debug = not self.debug

                    # EN JEU
                    if not self.game_over and self.start:
                        # Detection de la touche espace
                        if event.key == pygame.K_SPACE:
                            # Action : jump du joueur
                            self.player.jump()      

                    # GAME OVER
                    if self.game_over and self.start:
                        # Detection de la touche R
                        if event.key == pygame.K_r:
                            # Action : reset des éléments et restart la game
                            self.reset_game()                 

                    # ECRAN ACCUEIL
                    if not self.start and not self.game_over:
                        # Detection de la touche espace
                        if event.key == pygame.K_SPACE:
                            # Action : lance une partie
                            self.start = True
                            self.player.set_state("run")
                
    def reset_game(self):
        """
        Remet le jeu à zéro.
        
        :param self: Description
        """
        self.game_over = False
        self.start = False
        self.player.reset()
        self.game_manager.reset()
        self.obstacles_group.empty()

    def update(self):
        # MAJ score + vitesse
        self.game_manager.update()
        self.obstacles_group.update(self.game_manager.speed)
        # MAJ gravité du joueur
        self.player.apply_gravity()
        # test de collision entre hitbox joueur et hitbox obstacle
        if pygame.sprite.spritecollideany(self.player, self.obstacles_group, collided=Game.collision_par_hitbox):
            self.game_over = True
        # création aléatoire des obstacles
        if len(self.obstacles_group) == 0:
            self.spawn_obstacle()

    def draw(self):
        self.screen.fill(GREEN_COLOR)
        self.obstacles_group.draw(self.screen)
        self.player.draw(self.screen)
        self.score_ui.draw(self.screen, self.game_manager)

        if self.debug :
            # Affichage des hitbox
            self.player.draw_hitbox(self.screen)
            for obstacle in self.obstacles_group:
                obstacle.draw_hitbox(self.screen)

        if self.game_over :
            self.player.reset()
            self.player.set_state("idle")
            self.game_manager.update_highest_score() # maj du meilleur score retenu
            self.ui_manager.draw_game_over(self.screen)
        elif not self.start :
            self.ui_manager.draw_start(self.screen)
            self.player.set_state("idle")

        pygame.display.flip() # maj affichage

    def run(self):
        while self.running :
            self.handle_input()
            if not self.game_over and self.start : 
                self.update()

            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    @staticmethod
    def collision_par_hitbox(sprite1, sprite2):
        # On vérifie si la hitbox du sprite 1 touche la hitbox du sprite 2
        return sprite1.hitbox.colliderect(sprite2.hitbox)  

    def spawn_obstacle(self):
        # Quand on crée un obstacle, on lui DONNE l'image chargée
        # Plus besoin de charger dans l'obstacle !
        #nouveau_box = Box(x=800, y=300, image=self.assets['box'])
        #self.obstacles.add(nouveau_box)
        obstacle = random.choice(self.obstacle_types)
        new_obstacle = Obstacle(img=self.assets[obstacle]['img'], hitbox_factor=self.assets[obstacle]['hitbox_factor'])
        self.obstacles_group.add(new_obstacle) 
