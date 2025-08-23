### Definition des éléments nécessaire et fonctionnement du jeu ###

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS, BLACK_COLOR, RED_COLOR, GREEN_COLOR
from entities import Player, Obstacle, Score
from utils import draw_game_over_screen

def run_game() :
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    player = Player()
    obstacle = Obstacle()
    score = Score()
    
    running = True
    game_over = False

    while running :
        for event in pygame.event.get():
            # Detection de clic sur la croix pour fermer l'app
            if (event.type == pygame.QUIT):
                running = False
            # Detection d'une touche pressé
            elif (event.type == pygame.KEYDOWN and not game_over):
                # Detection de la touche espace
                if event.key == pygame.K_SPACE:
                    player.jump()      
            elif (event.type == pygame.KEYDOWN and game_over):
                # Detection de la touche R pour relancer une partie en cas de game over
                if event.key == pygame.K_r:
                    game_over = False
                    
                    obstacle.reset()
                    player.reset()
                    score.reset()

        if not game_over : 
            # update des positions
            obstacle.update()
            player.apply_gravity()
            score.update()
            # test de collision entre joueur et obstacle
            if player.rect.colliderect(obstacle.rect):
                game_over = True

        # draw
        screen.fill(GREEN_COLOR)
        obstacle.draw(screen)
        player.draw(screen)
        score.draw(screen)

        if game_over :
            score.update_best() # maj du meilleur score retenu
            draw_game_over_screen(screen)

        pygame.display.flip() # maj affichage
        clock.tick(FPS)
    pygame.quit()