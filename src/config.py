import os

# Paths
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
ASSETS_PATH = os.path.join(BASE_PATH, 'assets')
ENDINGS_PATH = os.path.join(ASSETS_PATH, 'endings')
MUSIC_PATH = os.path.join(ASSETS_PATH, 'music')

# Game settings
FPS = 60
MENU_WIDTH = 800
MENU_HEIGHT = 600

# Endings settings
VICTORY_SIZE_RATIO = 0.9  # Player must reach 90% of screen height
DODGE_TIME = 30.0        # Seconds without catching emojis
SECRET_TIME = 100.0      # Seconds of total gameplay

# Colors
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'YELLOW': (255, 255, 0),
    'GRAY': (150, 150, 150),
    'BACKGROUND': (160, 160, 160)
}

# Resource paths
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
