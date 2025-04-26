import pygame
import time

# $revision 1 hecha

# Función para dibujar el temporizador en tiempo real
def draw_timer(screen, start_time, x, y):
    elapsed_time = time.time() - start_time  # Calcular el tiempo transcurrido
    font = pygame.font.Font(None, 36)  # Fuente para el texto
    timer_text = font.render(f"Tiempo: {elapsed_time:.2f} s", True, (255, 255, 255))  # Formatear el texto del temporizador
    screen.blit(timer_text, (x, y))  # Dibujar el temporizador en la posición especificada

# Función para dibujar una barra de progreso para el final pacífico
def draw_peaceful_progress(screen, last_emoji_catch_time, x, y, width, height):
    elapsed_since_last_catch = time.time() - last_emoji_catch_time  # Tiempo desde la última captura
    max_time = 30  # Tiempo necesario para alcanzar el final pacífico
    progress = min(elapsed_since_last_catch / max_time, 1)  # Progreso como porcentaje (máximo 1)

    # Dibujar el fondo de la barra
    pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))  # Fondo gris oscuro
    # Dibujar la barra de progreso
    pygame.draw.rect(screen, (0, 255, 0), (x, y, int(progress * width), height))  # Barra verde
    # Dibujar el borde de la barra
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)  # Borde blanco

# Función para mostrar la velocidad de caída de los emojis
def draw_fall_speed(screen, fall_speed, x, y):
    font = pygame.font.Font(None, 36)  # Fuente para el texto
    speed_text = font.render(f"Velocidad: {fall_speed} px/s", True, (255, 255, 255))  # Formatear el texto de velocidad
    screen.blit(speed_text, (x, y))  # Dibujar el texto en la posición especificada

# Función para mostrar el contador de emojis atrapados
def draw_emoji_count(screen, emoji_count, x, y):
    font = pygame.font.Font(None, 36)  # Fuente para el texto
    count_text = font.render(f"Emojis atrapados: {emoji_count}", True, (255, 255, 255))  # Formatear el texto del contador
    screen.blit(count_text, (x, y))  # Dibujar el texto en la posición especificada
