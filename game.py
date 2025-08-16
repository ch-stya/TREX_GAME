### Definition des éléments nécessaire et fonctionnement du jeu ###

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS, BLUE_COLOR, RED_COLOR, GREEN_COLOR
from entities import Player, Obstacle

def run_game() :
    pygame.init()
    pygame.display.set_caption(GAME_TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)  # None = police par défaut, 74 = taille
    game_over_text = font.render("GAME OVER", True, RED_COLOR)  # texte rouge
    game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

    player = Player()
    obstacle = Obstacle()
    
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

        if not game_over : 
            # update des positions
            obstacle.update()
            player.apply_gravity()
            # test de collision entre joueur et obstacle
            if player.rect.colliderect(obstacle.rect):
                game_over = True

        # draw
        screen.fill(GREEN_COLOR)
        obstacle.draw(screen)
        player.draw(screen)

        if game_over :
            screen.blit(game_over_text, game_over_text_rect)

        pygame.display.flip() # maj affichage
        clock.tick(FPS)
    pygame.quit()