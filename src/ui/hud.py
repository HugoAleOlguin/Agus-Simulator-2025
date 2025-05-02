import pygame
import time

# $revision 1 hecha

# Función para dibujar el temporizador en tiempo real
def draw_timer(screen, start_time, x, y):
    elapsed_time = time.time() - start_time
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Tiempo: {elapsed_time:.1f}s", True, (255, 255, 255))
    
    # Sombra
    shadow = font.render(f"Tiempo: {elapsed_time:.1f}s", True, (0, 0, 0))
    screen.blit(shadow, (x + 2, y + 2))
    screen.blit(timer_text, (x, y))

# Función para dibujar una barra de progreso para el final pacífico
def draw_peaceful_progress(screen, last_emoji_catch_time, x, y, width, height):
    elapsed_since_last_catch = time.time() - last_emoji_catch_time
    max_time = 60
    progress = min(elapsed_since_last_catch / max_time, 1)
    
    # Color que cambia de verde a dorado
    progress_color = (
        min(255, int(progress * 255)),  # R
        max(215, int(255 - progress * 40)),  # G
        max(0, int(progress * 50))  # B
    )
    
    # Barra de fondo con borde
    pygame.draw.rect(screen, (50, 50, 50), (x-2, y-2, width+4, height+4))
    pygame.draw.rect(screen, (30, 30, 30), (x, y, width, height))
    
    # Barra de progreso con brillo
    progress_width = int(progress * width)
    if progress_width > 0:
        pygame.draw.rect(screen, progress_color, (x, y, progress_width, height))
        # Efecto de brillo
        brightness = pygame.Surface((2, height))
        brightness.fill((255, 255, 255))
        brightness.set_alpha(100)
        screen.blit(brightness, (x + progress_width - 2, y))

# Inicializar la variable estática
draw_peaceful_progress.last_progress = 0

# Función para mostrar la velocidad de caída de los emojis
def draw_fall_speed(screen, fall_speed, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(None, 36)
    speed_text = f"Velocidad: {fall_speed:.2f}"
    
    # Sombra y texto
    shadow = font.render(speed_text, True, (0, 0, 0))
    text = font.render(speed_text, True, color)
    
    screen.blit(shadow, (x + 2, y + 2))
    screen.blit(text, (x, y))

# Función para mostrar el contador de emojis atrapados
def draw_emoji_count(screen, emoji_count, x, y):
    font = pygame.font.Font(None, 36)
    text = f"Emojis: {emoji_count}"
    
    # Color basado en la cantidad
    color = (
        min(255, emoji_count * 10), 
        max(0, 255 - emoji_count * 5),
        0
    )
    
    count_text = font.render(text, True, color)
    shadow = font.render(text, True, (0, 0, 0))
    screen.blit(shadow, (x + 2, y + 2))
    screen.blit(count_text, (x, y))
