# revision 2 completa
import pygame
import random
import time
from player import Player
from emoji import Emoji
from utils import load_image, load_gif_frames
from hud import draw_timer, draw_peaceful_progress, draw_fall_speed, draw_emoji_count
from menu import show_menu
from endings import show_congratulations, show_peaceful_ending
from config import FPS

def main():
    # Inicializar Pygame y recursos
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('assets/background.mp3')
    pygame.mixer.music.play(-1)
    victory_sound = pygame.mixer.Sound('assets/victory.mp3')
    stress_sound = pygame.mixer.Sound('assets/stress.mp3')  # Asegúrate de tener este archivo
    stress_sound.set_volume(1.0)  # Volumen inicial del sonido de estrés
    player_image = load_image('assets/img.png')
    emoji_image = load_image('assets/emojis/emoji.png')
    gif_frames = load_gif_frames('assets/congratulations')

    # Configuración de la ventana
    WIDTH, HEIGHT = player_image.get_size()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Agus Simulator - Version 2.0")  # Cambiar el título de la ventana
    clock = pygame.time.Clock()

    while True:
        # Mostrar el menú inicial
        show_menu(screen)

        # Reinicializar variables del juego
        start_time = time.time()
        last_emoji_catch_time = start_time
        last_stress_sound_time = start_time  # Tiempo de la última reproducción del sonido de estrés
        emoji_count = 0
        emojis = []
        player = Player(WIDTH // 2, HEIGHT - 100)
        player.set_image(player_image)
        running = True

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
            if random.randint(1, max(2, 20 - int(elapsed_time // 5))) == 1:
                emojis.append(Emoji([random.randint(0, WIDTH - 20), 0], emoji_image))

            # Actualizar emojis
            fall_speed = 2 + int(elapsed_time // 5)
            for emoji in emojis[:]:
                emoji.fall(fall_speed)
                if emoji.isCaught(player.get_position(), player.get_size()):
                    player.grow(WIDTH, HEIGHT)
                    emojis.remove(emoji)
                    last_emoji_catch_time = time.time()
                    emoji_count += 1

            # Reproducir sonido de estrés cada 5 segundos
            if time.time() - last_stress_sound_time >= 10:
                stress_sound.play()
                last_stress_sound_time = time.time()

            # Verificar condiciones de victoria
            if player.get_size() >= WIDTH or player.get_size() >= HEIGHT:
                pygame.mixer.music.stop()  # Detener la música de fondo
                stress_sound.stop()  # Detener el sonido de estrés
                show_congratulations(screen, start_time, gif_frames, victory_sound, clock, FPS)
                running = False

            # Verificar final pacífico
            if time.time() - last_emoji_catch_time >= 30:
                pygame.mixer.music.stop()  # Detener la música de fondo
                stress_sound.stop()  # Detener el sonido de estrés
                show_peaceful_ending(screen, start_time, clock, FPS)
                running = False

            # Dibujar en pantalla con fondo restaurado
            screen.fill((160, 160, 160))  # Fondo gris original
            player.draw(screen)
            for emoji in emojis:
                emoji.draw(screen)
            draw_timer(screen, start_time, 10, 10)
            draw_emoji_count(screen, emoji_count, WIDTH - 250, 10)
            draw_peaceful_progress(screen, last_emoji_catch_time, WIDTH // 2 - 100, HEIGHT - 40, 200, 20)
            draw_fall_speed(screen, fall_speed, 10, HEIGHT - 40)
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()