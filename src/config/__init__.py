"""
Configuración central del juego Agus Simulator.
Todas las constantes del juego deben definirse aquí.
"""
import os

# Configuración de ventana y FPS
FPS = 60

# Tamaño del menú (más ancho para evitar superposición de textos)
MENU_WIDTH = 900
MENU_HEIGHT = 600

# Tamaño fijo de la ventana de juego
GAME_WIDTH = 600
GAME_HEIGHT = 600

# Alias para compatibilidad
WINDOW_WIDTH = MENU_WIDTH
WINDOW_HEIGHT = MENU_HEIGHT


# Configuración de finales
VICTORY_SIZE_RATIO = 0.9  # El jugador debe alcanzar 90% de la altura
DODGE_TIME = 30.0         # Segundos sin atrapar emojis para final pacífico
SECRET_TIME = 100.0       # Segundos totales de juego para final secreto

# Paleta de colores del juego
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

# Rutas de recursos
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS_PATH = os.path.join(BASE_PATH, 'src', 'assets')
ENDINGS_PATH = os.path.join(ASSETS_PATH, 'endings')
MUSIC_PATH = os.path.join(ASSETS_PATH, 'music')

# Definición de recursos
RESOURCES = {
    'ENDINGS': {
        'VICTORY_GIF': os.path.join(ENDINGS_PATH, 'congratulations'),
        'DODGE_IMAGE': os.path.join(ENDINGS_PATH, 'budagus.webp'),
    },
    'MUSIC': {
        'BACKGROUND': os.path.join(MUSIC_PATH, 'background.ogg'),
        'VICTORY': os.path.join(MUSIC_PATH, 'victory.ogg'),
        'DODGE': os.path.join(MUSIC_PATH, 'budagus.ogg'),
        'SECRET': os.path.join(MUSIC_PATH, 'secret.ogg'),
        'STRESS': os.path.join(MUSIC_PATH, 'stress.ogg'),
        'DEATH': os.path.join(MUSIC_PATH, 'death.ogg'),
    }
}
