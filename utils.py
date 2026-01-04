### Fichier contenant les fonctions de l'application ###

import pygame
from PIL import Image

def convert_spritesheet(path, total_images, start=0, end=None):
    """
    Fonction permettant de convertir un spritesheet en une liste de frames.
    
    :param path: (str) Chemin vers le fichier contenant le spritesheet 
    :param total_images: (int) Nombre d'images contenues dans le sprisheet
    :param start: (int) Par défaut 0, modulable si l'on ne veut pas récupérer toutes les images du spritesheet
    :param end: (int) Par défaut None, modulable si l'on ne veut pas récupérer toutes les images du spritesheet
    """
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

def convert_img(chemin, res) :
    """
    Fonction servant à convertir une image avec  Pillow. Ecrire "from PIL import Image" en début de programme pour l'utiliser.
    Convertit l'image et la place dans le même dossier, avec  taille de l'image dans le nom. 
    Exemple d'utilisation : convert_img("assets/images/saotome_pretty.png", (240, 320))

    :param chemin: (str) Chemin de l'image 
    :param res: (tuple) Nouvelle résolution souhaitée 
    """
    # Conversion d'une image avec Pillow (à ne faire qu'une fois)
    image = Image.open(chemin)
    # Redimensionnement de l'image
    nouvelle_image = image.resize(res)
    chemin = chemin[:-4]
    # Enregistrement de la nouvelle image
    nouvelle_image.save(chemin + "(" + str(res[0]) + "x" + str(res[1]) + ").png")

def scale_frames(frames, factor):
    """
    Fonction permettant d'appliquer une mise à l'échelle à une sélection d'images.

    :param frames: (liste) Liste des frames à mettre à l'échelle
    :param factor: (float) Facteur de mise à l'échelle
    """
    scaled = []
    for frame in frames:
        width = int(frame.get_width() * factor)
        height = int(frame.get_height() * factor)
        scaled_frame = pygame.transform.scale(frame, (width, height))
        scaled.append(scaled_frame)
    return scaled