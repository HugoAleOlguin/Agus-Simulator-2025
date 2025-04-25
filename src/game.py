import pygame
import random
import time  # Importar módulo para medir el tiempo
from player import Player
from emoji import Emoji
from utils import load_image, load_gif_frames

# Inicializar Pygame
pygame.init()

# Cargar música de fondo y sonido de victoria
pygame.mixer.init()
pygame.mixer.music.load('assets/background.mp3')  # Ruta del archivo MP3
pygame.mixer.music.play(-1)  # Reproducir en bucle
victory_sound = pygame.mixer.Sound('assets/victory.mp3')  # Ruta del archivo mp3

# Cargar recursos
player_image = load_image('assets/img.png')  # Imagen del jugador
emoji_image = load_image('assets/emojis/emoji.png')  # Imagen del emoji

# Cargar frames del GIF de felicitaciones
gif_frames = load_gif_frames('assets/congratulations')  # Ruta de la carpeta con los frames del GIF

# Ajustar el tamaño de la ventana al tamaño de la imagen del jugador
player_image_width, player_image_height = player_image.get_size()
WIDTH = player_image_width
HEIGHT = player_image_height

# Constantes
FPS = 50  # Fotogramas por segundo

# Crear jugador
player = Player(WIDTH // 2, HEIGHT - 100)  # Posición inicial del jugador
player.set_image(player_image)  # Asignar imagen al jugador

# Lista de emojis
emojis = []

# Configuración de la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agus Simulator")  # Cambiar el título de la ventana
clock = pygame.time.Clock()

# Función para mostrar el menú inicial
def show_menu(screen):
    menu_running = True
    font = pygame.font.Font(None, 74)
    title_text = font.render("Agus Simulator", True, (255, 255, 255))
    play_text = font.render("Presiona ENTER...", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    while menu_running:
        screen.fill((0, 0, 0))  # Fondo negro
        screen.blit(title_text, title_rect)
        screen.blit(play_text, play_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Salir del juego
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Presionar ENTER
                menu_running = False

# Mostrar el menú inicial
show_menu(screen)

# Inicializar el temporizador
start_time = time.time()
last_emoji_catch_time = start_time  # Tiempo de la última captura de un emoji

# Función para mostrar el mensaje de "¡Felicidades!" con un GIF animado, confeti y tiempo final
def show_congratulations(screen):
    pygame.mixer.music.stop()  # Detener la música de fondo

    # Reproducir sonido de victoria en bucle
    victory_sound.play(-1)  # Repetir indefinidamente

    # Calcular el tiempo final
    elapsed_time = time.time() - start_time
    elapsed_time_text = f"Tiempo: {elapsed_time:.2f} segundos"

    # Configurar los mensajes
    font = pygame.font.Font(None, 74)
    text = font.render("¡Felicidades!", True, (255, 255, 255))
    time_text = font.render(elapsed_time_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    # Generar confeti
    confetti = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])] for _ in range(100)]

    # Crear un bucle para mostrar el GIF, el mensaje y el tiempo
    for frame_index in range(15 * FPS):  # Mostrar por 15 segundos (15 * 60 frames)
        screen.fill((0, 0, 0))  # Fondo negro

        # Renderizar el frame actual del GIF
        gif_frame = gif_frames[frame_index % len(gif_frames)]  # Obtener el frame correspondiente
        screen.blit(gif_frame, (0, 0))

        # Dibujar los mensajes
        screen.blit(text, text_rect)
        screen.blit(time_text, time_rect)

        # Dibujar confeti
        for c in confetti:
            pygame.draw.circle(screen, c[2], (c[0], c[1]), 5)  # Dibujar confeti
            c[1] += 5  # Mover confeti hacia abajo
            if c[1] > HEIGHT:
                c[1] = 0  # Reiniciar confeti en la parte superior

        pygame.display.flip()
        clock.tick(FPS)

    victory_sound.stop()  # Detener el sonido de victoria después de 15 segundos

# Función para mostrar el segundo final
def show_peaceful_ending(screen):
    pygame.mixer.music.stop()  # Detener la música de fondo

    # Configurar el mensaje
    font = pygame.font.Font(None, 74)
    text = font.render("¡Final Pacífico!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Mostrar el mensaje
    for frame_index in range(5 * FPS):  # Mostrar por 5 segundos
        screen.fill((0, 0, 0))  # Fondo negro
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(FPS)

# Bucle principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Salir del juego
            running = False

    # Actualizar posición del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Mover a la izquierda
        player.move(-5, 0, WIDTH, HEIGHT)
    if keys[pygame.K_d]:  # Mover a la derecha
        player.move(5, 0, WIDTH, HEIGHT)
    if keys[pygame.K_w]:  # Mover hacia arriba
        player.move(0, -5, WIDTH, HEIGHT)
    if keys[pygame.K_s]:  # Mover hacia abajo
        player.move(0, 5, WIDTH, HEIGHT)

    # Generar emojis con mayor frecuencia a medida que pasa el tiempo
    elapsed_time = time.time() - start_time
    emoji_spawn_chance = max(2, 20 - int(elapsed_time // 5))  # Aumentar la frecuencia cada 5 segundos
    if random.randint(1, emoji_spawn_chance) == 1:
        position = [random.randint(0, WIDTH - 20), 0]  # Posición inicial (x, y)
        emojis.append(Emoji(position, emoji_image))  # Crear y agregar emoji

    # Actualizar emojis
    fall_speed = 2 + int(elapsed_time // 10)  # Incrementar la velocidad de caída cada 10 segundos
    for emoji in emojis[:]:
        emoji.fall(fall_speed)  # Velocidad de caída dinámica
        if emoji.isCaught(player.get_position(), player.get_size()):  # Verificar si el jugador atrapó el emoji
            player.grow(WIDTH, HEIGHT)  # Crecer al jugador con límites de la ventana
            emojis.remove(emoji)  # Eliminar emoji atrapado
            last_emoji_catch_time = time.time()  # Actualizar el tiempo de la última captura

    # Verificar si el jugador abarca toda la ventana
    player_size = player.get_size()  # Obtener el tamaño del jugador
    if player_size >= WIDTH or player_size >= HEIGHT:  # Verificar si el jugador cubre toda la ventana
        show_congratulations(screen)
        running = False  # Salir del bucle principal

    # Verificar si han pasado 30 segundos sin tocar ningún emoji
    if time.time() - last_emoji_catch_time >= 30:
        show_peaceful_ending(screen)
        running = False  # Salir del bucle principal

    # Dibujar todo en la pantalla
    screen.fill((160, 160, 160))  # Limpiar la pantalla (color blanco)
    player.draw(screen)  # Dibujar al jugador
    for emoji in emojis:
        emoji.draw(screen)  # Dibujar cada emoji

    pygame.display.flip()  # Actualizar la pantalla
    clock.tick(FPS)  # Controlar la velocidad del juego

pygame.quit()  # Salir de Pygame