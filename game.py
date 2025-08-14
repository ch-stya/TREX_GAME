### Definition des éléments nécessaire et fonctionnement du jeu ###

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS, BLUE_COLOR, GREEN_COLOR
from entities import Player

def run_game() :
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    player = Player()
    
    running = True
    while running :
        for event in pygame.event.get():
            # Detection de clic sur la croix pour fermer l'app
            if (event.type == pygame.QUIT):
                running = False
            # Detection d'une touche pressé
            elif (event.type == pygame.KEYDOWN):
                # Detection de la touche espace
                if event.key == pygame.K_SPACE:
                    player.jump()
        screen.fill(GREEN_COLOR)
        player.apply_gravity()
        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()