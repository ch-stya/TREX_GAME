### Fichier contenant les éléments de configuration de l'application ###

import os

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMG_PATHS = {
    'small_box': os.path.join(ASSETS_DIR, 'objects', 'box(32x32).png'),
    'big_box': os.path.join(ASSETS_DIR, 'objects', 'box(64x64).png'),
    'yarn': os.path.join(ASSETS_DIR, 'objects', 'pink_yarn(32x32).png'), 
    'icon': os.path.join(ASSETS_DIR, 'icon', 'icone.png') 
}


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GAME_TITLE = "TREX GAME"
FPS = 60
BLUE_COLOR = (0, 0, 255)
RED_COLOR = (100, 0, 0)
GREEN_COLOR = (143, 188, 143)
BLACK_COLOR = (0, 0, 0)
GROUND_MARGIN = SCREEN_HEIGHT // 4 # Marge entre le bas de la fenêtre et le sol
GROUND_Y = SCREEN_HEIGHT - GROUND_MARGIN # Position verticale du sol

SKINS = {
    "grey":{
        "run": os.path.join(ASSETS_DIR, "skins", "grey_cat", "run.png"),
        "idle": os.path.join(ASSETS_DIR, "skins", "grey_cat", "idle.png"),
        "jump": os.path.join(ASSETS_DIR, "skins", "grey_cat", "jump.png")
    },
    "brown":{
        "run": os.path.join(ASSETS_DIR, "skins", "brown_cat", "run.png"),
        "idle": os.path.join(ASSETS_DIR, "skins", "brown_cat", "idle.png"),
        "jump": os.path.join(ASSETS_DIR, "skins", "brown_cat", "jump.png")
    },
    "white":{
        "run": os.path.join(ASSETS_DIR, "skins", "white_cat", "run.png"),
        "idle": os.path.join(ASSETS_DIR, "skins", "white_cat", "idle.png"),
        "jump": os.path.join(ASSETS_DIR, "skins", "white_cat", "jump.png")
    }
}