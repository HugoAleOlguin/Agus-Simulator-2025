import sys
import os
import pygame

# Asegurar que src esté en el path
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

import time
import random
from src.utils import load_audio, load_image, load_music
from src.ui.menu import show_menu, show_mode_selection_menu
from src.ui.hud import draw_timer, draw_peaceful_progress, draw_fall_speed, draw_emoji_count
from src.entities.player import Player
from src.entities.emoji import Emoji
from src.config import FPS, MENU_WIDTH, MENU_HEIGHT, COLORS

def init_pygame():
    pygame.init()
    # Optimizaciones de pygame
    pygame.display.set_allow_screensaver(True)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    pygame.display.set_caption("Agus Simulator - V3")
    
    if sys.platform.startswith('win'):
        # Optimizaciones específicas para Windows
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()

def run_game_loop(screen, clock, mode_description, resources, WIDTH, HEIGHT, player_image, emoji_image):
    MAX_EMOJIS = 5  # Límite máximo de emojis activos
    start_time = time.time()
    last_catch_time = start_time
    last_stress_sound_time = start_time
    emoji_count = 0
    emojis = []
    player = Player(WIDTH // 2, HEIGHT - 100)
    player.set_image(player_image)
    running = True

    description_display_time = 3
    description_start_time = time.time()
    
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: player.move(-5, 0, WIDTH, HEIGHT)
        if keys[pygame.K_d]: player.move(5, 0, WIDTH, HEIGHT)
        if keys[pygame.K_w]: player.move(0, -5, WIDTH, HEIGHT)
        if keys[pygame.K_s]: player.move(0, 5, WIDTH, HEIGHT)

        elapsed_time = current_time - start_time
        if len(emojis) < MAX_EMOJIS and random.randint(1, max(2, 20 - int(elapsed_time // 5000))) == 1:
            emojis.append(Emoji([random.randint(0, WIDTH - 20), 0], emoji_image))  # Usar el emoji_image pasado

        fall_speed = round(2 + int(elapsed_time // 10), 2)  # Redondear la velocidad
        for emoji in emojis[:]:
            emoji.fall(fall_speed)
            if emoji.isCaught(player.get_position(), player.get_size()):
                player.grow(WIDTH, HEIGHT)  # Siempre crece al atrapar
                emojis.remove(emoji)
                last_catch_time = current_time
                emoji_count += 1

        screen.fill((160, 160, 160))
        player.draw(screen)
        for emoji in emojis:
            emoji.draw(screen)

        if current_time - description_start_time <= description_display_time:
            font = pygame.font.Font(None, 50)
            max_width = WIDTH - 40
            render_multiline_text(
                screen,
                mode_description,
                font,
                (255, 255, 255),
                0,
                0,
                max_width,
                WIDTH // 2,
                HEIGHT // 2
            )

        draw_timer(screen, start_time, 10, 10)
        draw_emoji_count(screen, emoji_count, WIDTH - 250, 10)
        draw_peaceful_progress(screen, last_catch_time, WIDTH // 2 - 100, HEIGHT - 40, 200, 20)
        draw_fall_speed(screen, fall_speed, 10, HEIGHT - 40)
        pygame.display.flip()
        clock.tick(FPS)

        if current_time - last_stress_sound_time >= 10:
            resources['stress_sound'].play()
            last_stress_sound_time = current_time

def render_multiline_text(screen, text, font, color, margin_x, margin_y, max_width, center_x, center_y):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    total_height = len(lines) * font.get_linesize()
    start_y = center_y - total_height // 2

    for i, line in enumerate(lines):
        rendered_text = font.render(line, True, color)
        text_width = font.size(line)[0]
        line_x = center_x - text_width // 2
        line_y = start_y + i * font.get_linesize()
        screen.blit(rendered_text, (line_x, line_y))

def main():
    try:
        init_pygame()

        screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
        clock = pygame.time.Clock()

        # Imprimir directorio de trabajo actual para debugging
        print(f"Directorio de trabajo: {os.getcwd()}")

        # Cargar recursos (rutas relativas a la carpeta assets)
        try:
            music_path = load_music('music/background.ogg')
            if music_path:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Error música: {e}")

        # Cargar imágenes
        player_image = load_image('img.png')
        if not player_image:
            # Crear imagen de respaldo más grande
            player_image = pygame.Surface((400, 400))
            player_image.fill((255, 0, 0))
            print("Usando imagen de respaldo para el jugador")

        try:
            emoji_image = load_image('emojis/emoji.png')  # Simplificado para usar el helper
            if not emoji_image:
                print("No se pudo cargar el emoji, usando respaldo")
                emoji_image = pygame.Surface((50, 50))
                emoji_image.fill((0, 255, 0))
        except Exception as e:
            print(f"Error cargando emoji: {e}")
            emoji_image = pygame.Surface((50, 50))
            emoji_image.fill((0, 255, 0))

        # Obtener dimensiones
        game_width = player_image.get_width()
        game_height = player_image.get_height()
        print(f"Tamaño de ventana de juego: {game_width}x{game_height}")

        try:
            resources = {
                'stress_sound': pygame.mixer.Sound(load_audio('music/stress.ogg'))
            }
        except FileNotFoundError as e:
            print(f"Error sonido: {e}")
            resources = {
                'stress_sound': pygame.mixer.Sound(buffer=b'\x00' * 44100)
            }

        # Show main menu y manejar resultado
        while True:
            if show_menu(screen):
                selected_mode = show_mode_selection_menu(screen)
                if selected_mode:
                    # Adaptar ventana al tamaño de la imagen del jugador
                    screen = pygame.display.set_mode((game_width, game_height))

                    # Ejecutar modo seleccionado
                    package = f"modes.{selected_mode}"
                    mode_module = __import__(package, fromlist=[selected_mode])
                    mode_class_name = selected_mode.title().replace('_', '')
                    mode_class = getattr(mode_module, mode_class_name)
                    mode_instance = mode_class(
                        screen,
                        clock,
                        game_width,    # Usar dimensiones de la imagen del jugador
                        game_height,   # Usar dimensiones de la imagen del jugador
                        player_image,
                        emoji_image,
                        resources
                    )
                    mode_instance.run_mode()

                    # Volver al tamaño del menú
                    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
            else:
                break  # Salir si el menú retorna False
    except Exception as e:
        print(f"Error: {e}")
        print(f"Ruta actual: {os.getcwd()}")
    finally:
        pygame.quit()
        sys.exit()  # Usar sys.exit() en lugar de exit()

if __name__ == "__main__":
    main()