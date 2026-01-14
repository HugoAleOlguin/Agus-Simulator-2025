"""
Módulo principal del juego Agus Simulator.
Inicializa pygame, carga recursos y maneja el flujo del menú.
"""
import sys
import os
import pygame

# Asegurar que src esté en el path para imports
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

if base_path not in sys.path:
    sys.path.append(base_path)

# Asegurar que el directorio raíz del proyecto esté en sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)
if project_dir not in sys.path:
    sys.path.append(project_dir)

from src.utils import load_audio, load_image, load_music
from src.utils.skin_manager import SkinManager
from src.ui.menu import show_menu, show_mode_selection_menu
from src.config import FPS, MENU_WIDTH, MENU_HEIGHT


def init_pygame():
    """Inicializa pygame con optimizaciones."""
    pygame.init()
    pygame.display.set_allow_screensaver(True)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    pygame.display.set_caption("Agus Simulator - V3.1")
    
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()


def main():
    """Punto de entrada principal del juego."""
    try:
        init_pygame()

        screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
        clock = pygame.time.Clock()

        print(f"Directorio de trabajo: {os.getcwd()}")

        # Inicializar el gestor de skins
        skin_manager = SkinManager()

        # Cargar música de fondo
        try:
            music_path = load_music('music/background.ogg')
            if music_path:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Error música: {e}")

        # Cargar imagen del emoji
        try:
            emoji_image = load_image('emojis/emoji.png')
            if not emoji_image:
                print("No se pudo cargar el emoji, usando respaldo")
                emoji_image = pygame.Surface((50, 50))
                emoji_image.fill((0, 255, 0))
        except Exception as e:
            print(f"Error cargando emoji: {e}")
            emoji_image = pygame.Surface((50, 50))
            emoji_image.fill((0, 255, 0))

        # Cargar recursos de audio
        try:
            resources = {
                'stress_sound': pygame.mixer.Sound(load_audio('music/stress.ogg'))
            }
        except FileNotFoundError as e:
            print(f"Error sonido: {e}")
            resources = {
                'stress_sound': pygame.mixer.Sound(buffer=b'\x00' * 44100)
            }

        # Loop principal del menú
        while True:
            if show_menu(screen):
                selected_mode = show_mode_selection_menu(screen, skin_manager)
                if selected_mode:
                    # Importar tamaño fijo del juego
                    from src.config import GAME_WIDTH, GAME_HEIGHT
                    
                    # Cargar la skin seleccionada
                    selected_skin = skin_manager.get_selected_skin()
                    player_image_original = skin_manager.load_skin_image(selected_skin)
                    
                    if not player_image_original:
                        player_image_original = pygame.Surface((400, 400))
                        player_image_original.fill((255, 0, 0))
                        print("Usando imagen de respaldo para el jugador")
                    
                    # Escalar la skin al tamaño del juego (manteniendo aspecto)
                    player_image_original = player_image_original.convert_alpha()
                    orig_w, orig_h = player_image_original.get_size()
                    scale = min(GAME_WIDTH / orig_w, GAME_HEIGHT / orig_h)
                    new_size = (int(orig_w * scale), int(orig_h * scale))
                    player_image = pygame.transform.smoothscale(player_image_original, new_size)
                    
                    print(f"Skin: {selected_skin} | Original: {orig_w}x{orig_h} | Escalado: {new_size}")

                    # Usar tamaño fijo del juego
                    game_width = GAME_WIDTH
                    game_height = GAME_HEIGHT
                    
                    # Adaptar ventana al tamaño fijo del juego
                    screen = pygame.display.set_mode((game_width, game_height))

                    # Cargar y ejecutar modo seleccionado dinámicamente
                    package = f"modes.{selected_mode}"
                    mode_module = __import__(package, fromlist=[selected_mode])
                    mode_class_name = selected_mode.title().replace('_', '')
                    mode_class = getattr(mode_module, mode_class_name)
                    mode_instance = mode_class(
                        screen,
                        clock,
                        game_width,
                        game_height,
                        player_image,
                        emoji_image,
                        resources
                    )
                    mode_instance.run_mode()

                    # Volver al tamaño del menú
                    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
            else:
                break
    except Exception as e:
        print(f"Error: {e}")
        print(f"Ruta actual: {os.getcwd()}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()