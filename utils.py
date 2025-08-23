### Fichier contenant les fonctions de l'application ###

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, RED_COLOR, BLACK_COLOR

def draw_game_over_screen(surface):
    game_over_font = pygame.font.Font(None, 74)  # None = police par défaut, 74 = taille
    game_over_text = game_over_font.render("GAME OVER", True, RED_COLOR)  # texte rouge
    game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    replay_font = pygame.font.Font(None, 30)
    replay_text = replay_font.render("Press 'R' to restart", True, BLACK_COLOR)  # texte rouge
    replay_text_rect = replay_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+40))
    surface.blit(game_over_text, game_over_text_rect)
    surface.blit(replay_text, replay_text_rect)
    return None