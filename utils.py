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

def draw_start_screen(surface):
    start_font = pygame.font.Font(None, 50)
    start_text = start_font.render("Press 'Space' to start", True, BLACK_COLOR)
    start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    surface.blit(start_text, start_text_rect)
    return None

def convert_spritesheet(path, total_images, start=0, end=None):
    spritesheet = pygame.image.load(path).convert_alpha()
    frame_width = spritesheet.get_width() // total_images
    frame_height = spritesheet.get_height()
    frames = []
    if end is None : # si end pas précisé on prends le total images
        end = total_images
    for i in range(start, end):
        rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame_image = spritesheet.subsurface(rect)
        frames.append(frame_image)
    return frames, frame_height, frame_width