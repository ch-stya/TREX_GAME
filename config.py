### Fichier contenant les éléments de configuration de l'application ###

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
        "run": "assets/skins/grey_cat/run.png",
        "idle": "assets/skins/grey_cat/idle.png",
        "jump": "assets/skins/grey_cat/jump.png"
    },
    "brown":{
        "run": "assets/skins/brown_cat/run.png",
        "idle": "assets/skins/brown_cat/idle.png",
        "jump": "assets/skins/brown_cat/jump.png"
    }
}