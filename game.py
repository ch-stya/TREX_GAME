### Definition des éléments nécessaire et fonctionnement du jeu ###

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS, BLUE_COLOR

def run_game() :
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    running = True
    while running :
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
        screen.fill(BLUE_COLOR)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()