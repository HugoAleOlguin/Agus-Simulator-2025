# Configuración de ventana y FPS
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Alias para el menú
MENU_WIDTH = WINDOW_WIDTH
MENU_HEIGHT = WINDOW_HEIGHT

# Colores del juego
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'GRAY': (128, 128, 128),
    'BACKGROUND': (160, 160, 160)
}

# Configuración de paths
import os
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS_PATH = os.path.join(BASE_PATH, 'assets')
ENDINGS_PATH = os.path.join(ASSETS_PATH, 'endings')
MUSIC_PATH = os.path.join(ASSETS_PATH, 'music')
