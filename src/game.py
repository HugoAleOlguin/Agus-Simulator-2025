# revision 2 completa
import pygame
import random
import time
from player import Player
from emoji import Emoji
from utils import load_image, load_gif_frames
from hud import draw_timer, draw_peaceful_progress, draw_fall_speed, draw_emoji_count
from menu import show_menu, show_mode_selection_menu
from endings import show_biggest_ally_ending, show_dodger_ending, show_secret_ending
from config import FPS

def show_mode_description(screen, description):
    pygame.font.init()
    font = pygame.font.Font(None, 50)
    screen.fill((0, 0, 0))
    text = font.render(description, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Mostrar la descripción durante 2 segundos

def render_multiline_text(screen, text, font, color, margin_x, margin_y, max_width, center_x, center_y):
    """Renderiza texto en múltiples líneas ajustándose al tamaño de la ventana con márgenes y centrado."""
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
    lines.append(current_line)  # Agregar la última línea

    # Calcular la altura total del texto para centrarlo verticalmente
    total_height = len(lines) * font.get_linesize()
    start_y = center_y - total_height // 2

    for i, line in enumerate(lines):
        rendered_text = font.render(line, True, color)
        text_width = font.size(line)[0]
        line_x = center_x - text_width // 2  # Centrar horizontalmente
        line_y = start_y + i * font.get_linesize()
        screen.blit(rendered_text, (line_x, line_y))

def main():
    # Inicializar Pygame y recursos
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('assets/music/background.mp3')
    pygame.mixer.music.play(-1)
    victory_sound = pygame.mixer.Sound('assets/music/victory.mp3')
    budagus_sound = pygame.mixer.Sound('assets/music/budagus.mp3')
    stress_sound = pygame.mixer.Sound('assets/music/stress.mp3')  # Asegúrate de tener este archivo
    stress_sound.set_volume(1.0)  # Volumen inicial del sonido de estrés
    secret_sound = pygame.mixer.Sound('assets/music/secret.mp3')  # Cargar la canción del final secreto
    player_image = load_image('assets/img.png')
    emoji_image = load_image('assets/emojis/emoji.png')
    gif_frames = load_gif_frames('assets/endings/congratulations')
    dodger_image = load_image('assets/endings/budagus.png')  # Cargar la imagen del ending de esquivar

    # Configuración de la ventana
    WIDTH, HEIGHT = player_image.get_size()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Agus Simulator - Beta 2.5")  # Cambiar el título de la ventana
    clock = pygame.time.Clock()

    while True:
        # Mostrar el menú inicial
        show_menu(screen)

        # Mostrar el menú de selección de modo
        selected_mode = show_mode_selection_menu(screen)

        # Configurar el modo de juego según la selección
        if selected_mode == 1:
            mode_description = "¡Atrapa o esquiva banderas!"
        elif selected_mode == 2:
            mode_description = "Modo Hetero: Próximamente."
        elif selected_mode == 3:
            mode_description = "Modo Infinito: Próximamente."

        # Si el modo no está implementado, volver al menú
        if selected_mode in [2, 3]:
            continue

        # Reinicializar variables del juego
        start_time = time.time()
        last_emoji_catch_time = start_time
        last_stress_sound_time = start_time  # Tiempo de la última reproducción del sonido de estrés
        emoji_count = 0
        emojis = []
        player = Player(WIDTH // 2, HEIGHT - 100)
        player.set_image(player_image)
        secret_ending_triggered = False  # Bandera para el final secreto
        running = True

        print(f"Modo seleccionado: {mode_description}")

        # Mostrar la descripción del modo seleccionado en el fondo durante los primeros segundos
        description_display_time = 3  # Segundos para mostrar la descripción
        description_start_time = time.time()

        # Bucle principal del juego
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Movimiento del jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]: player.move(-5, 0, WIDTH, HEIGHT)
            if keys[pygame.K_d]: player.move(5, 0, WIDTH, HEIGHT)
            if keys[pygame.K_w]: player.move(0, -5, WIDTH, HEIGHT)
            if keys[pygame.K_s]: player.move(0, 5, WIDTH, HEIGHT)

            # Generar emojis
            elapsed_time = time.time() - start_time
            if random.randint(1, max(2, 20 - int(elapsed_time // 5000))) == 1:
                emojis.append(Emoji([random.randint(0, WIDTH - 20), 0], emoji_image))

            # Actualizar emojis
            fall_speed = 2 + int(elapsed_time // 10)  # Aumentar la velocidad de caída con el tiempo
            for emoji in emojis[:]:
                emoji.fall(fall_speed)
                if emoji.isCaught(player.get_position(), player.get_size()):
                    player.grow(WIDTH, HEIGHT)
                    emojis.remove(emoji)
                    last_emoji_catch_time = time.time()
                    emoji_count += 1

            # Dibujar en pantalla con fondo restaurado
            screen.fill((160, 160, 160))  # Fondo gris original
            player.draw(screen)
            for emoji in emojis:
                emoji.draw(screen)

            # Mostrar la descripción del modo seleccionado en el fondo durante los primeros segundos
            if time.time() - description_start_time <= description_display_time:
                font = pygame.font.Font(None, 50)
                max_width = WIDTH - 40  # Ancho máximo ajustado al tamaño de la ventana con márgenes
                render_multiline_text(
                    screen,
                    mode_description,
                    font,
                    (255, 255, 255),
                    0,  # No se usa margen_x porque el centrado es automático
                    0,  # No se usa margen_y porque el centrado es automático
                    max_width,
                    WIDTH // 2,  # Centro horizontal
                    HEIGHT // 2  # Centro vertical
                )

            # Dibujar HUD
            draw_timer(screen, start_time, 10, 10)
            draw_emoji_count(screen, emoji_count, WIDTH - 250, 10)
            draw_peaceful_progress(screen, last_emoji_catch_time, WIDTH // 2 - 100, HEIGHT - 40, 200, 20)
            draw_fall_speed(screen, fall_speed, 10, HEIGHT - 40)
            pygame.display.flip()
            clock.tick(FPS)

            # Reproducir sonido de estrés cada 5 segundos
            if time.time() - last_stress_sound_time >= 10:
                stress_sound.play()
                last_stress_sound_time = time.time()

            # Verificar si se activa el final secreto
            if not secret_ending_triggered and time.time() - start_time >= 100:
                secret_ending_triggered = True  # Activar la bandera del final secreto

            # Verificar condiciones de victoria
            if player.get_size() >= WIDTH or player.get_size() >= HEIGHT:
                pygame.mixer.music.stop()  # Detener la música de fondo
                stress_sound.stop()  # Detener el sonido de estrés
                if secret_ending_triggered:
                    show_secret_ending(screen, start_time, secret_sound, clock, FPS)  # Mostrar final secreto
                else:
                    show_biggest_ally_ending(screen, start_time, gif_frames, victory_sound, clock, FPS)
                running = False
                continue  # Asegurar que no se ejecute otro ending después

            # Verificar final de esquivar
            if time.time() - last_emoji_catch_time >= 30:
                pygame.mixer.music.stop()  # Detener la música de fondo
                stress_sound.stop()  # Detener el sonido de estrés
                if secret_ending_triggered:
                    show_secret_ending(screen, start_time, secret_sound, clock, FPS)  # Mostrar final secreto
                else:
                    show_dodger_ending(screen, start_time, dodger_image, budagus_sound, clock, FPS)
                running = False
                continue  # Asegurar que no se ejecute otro ending después

if __name__ == "__main__":
    main()