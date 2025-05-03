import pygame
import sys
import os
import math
import time
from src.config import FPS, MENU_WIDTH, MENU_HEIGHT, COLORS

GAME_VERSION = "Version 3.0"

def show_classic_tutorial(screen):
    title_text = ("MODO CLÁSICO", (255, 215, 0))
    tutorial_text = [
        ("En este modo eres libre de expresar tus opiniones", (255, 200, 100)),
        ("Agarra banderas.. o esquivalas", (100, 255, 100)),
        ("Usa W,A,S,D... Sí, como todos los juegos...", (200, 200, 255)),
        ("Descubre los 2 finales diferentes", (255, 180, 180)),
        ("O eran 3..? no me acuerdo", (200, 255, 200)),
    ]
    enter_text = ("Presiona ENTER para salir del clos... digo, para jugar", (150, 150, 150))
    return show_mode_tutorial(screen, title_text, tutorial_text, enter_text)

def show_hetero_tutorial(screen):
    title_text = ("MODO HETERO", (255, 255, 0))
    tutorial_text = [
        ("¿Te atreves a esquivar la inclusión?", (255, 100, 100)),
        ("La sociedad te persigue con... ¿emojis!!?", (255, 150, 150)),
        ("W,A,S,D - Para huir como un macho", (200, 200, 255)),
        ("Cada vez hay más diversidad... ¡CORRE!", (255, 180, 180)),
        ("¡No dejes que te conviertan!", (200, 255, 200)),
    ]
    enter_text = ("Presiona ENTER para demostrar tu heterosexualidad", (150, 150, 150))
    return show_mode_tutorial(screen, title_text, tutorial_text, enter_text)

def show_infinite_tutorial(screen):
    title_text = ("MODO INFINITO", (255, 128, 0))
    tutorial_text = [
        ("Esquiva emojis hasta que no puedas más", (255, 200, 100)),
        ("Cada vez irán más rápido", (255, 150, 150)),
        ("¡Supera tu récord anterior!", (200, 200, 255))
    ]
    enter_text = ("Presiona ENTER para comenzar", (150, 150, 150))
    return show_mode_tutorial(screen, title_text, tutorial_text, enter_text)

def show_nightmare_tutorial(screen):
    title_text = ("MODO PESADILLA", (255, 0, 0))
    tutorial_text = [
        ("???", (255, 0, 0)),
        ("Próximamente...", (200, 0, 0)),
    ]
    enter_text = ("Presiona ESC para volver", (100, 0, 0))
    return False

def show_mode_tutorial(screen, title_text, tutorial_text, enter_text):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

        screen.fill((0, 0, 0))
        
        # Título con efecto de brillo
        title_font = pygame.font.Font(None, 74)
        pulse = (math.sin(time.time() * 2) + 1) / 4
        title_color = tuple(max(0, min(255, c + 30 * pulse)) for c in title_text[1])
        text_surface = title_font.render(title_text[0], True, title_color)
        rect = text_surface.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 4))
        screen.blit(text_surface, rect)

        # Tutorial con efecto de fade
        tutorial_font = pygame.font.Font(None, 42)
        total_height = len(tutorial_text) * 60
        start_y = (MENU_HEIGHT - total_height) // 2 + 50

        for i, (text, base_color) in enumerate(tutorial_text):
            alpha = math.sin(time.time() * 2 + i * 0.5) * 30 + 225  # Efecto de fade individual
            color = tuple(max(0, min(255, c * alpha / 255)) for c in base_color)
            text_surface = tutorial_font.render(text, True, color)
            rect = text_surface.get_rect(center=(MENU_WIDTH // 2, start_y + i * 60))
            screen.blit(text_surface, rect)

        # Texto ENTER parpadeante
        enter_font = pygame.font.Font(None, 36)
        enter_alpha = (math.sin(time.time() * 4) + 1) / 2  # Parpadeo más rápido
        enter_color = tuple(max(0, min(255, c * enter_alpha)) for c in enter_text[1])
        enter_surface = enter_font.render(enter_text[0], True, enter_color)
        enter_rect = enter_surface.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT - 40))
        screen.blit(enter_surface, enter_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def show_menu(screen):
    menu_running = True
    font_title = pygame.font.Font(None, 100)
    font_instructions = pygame.font.Font(None, 50)
    font_version = pygame.font.Font(None, 36)

    # Textos del menú
    play_text = font_instructions.render("Presiona ENTER para jugar", True, (255, 255, 255))
    exit_text = font_instructions.render("Presiona ESC para salir", True, (255, 255, 255))
    version_text = font_version.render(GAME_VERSION, True, (150, 150, 150))

    # Posiciones de los textos
    play_rect = play_text.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 2))
    exit_rect = exit_text.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 2 + 50))
    version_rect = version_text.get_rect(topright=(MENU_WIDTH - 20, 20))

    # Lista de tips
    tips = [
        "Usa W, A, S, D para moverte",
        "¿De qué país son esas banderas?",  # Corregido "que" a "qué"
        "¿Emojis...?",
        "Puedes reiniciar cualquier partida con R",  # Corregido "resetera" a "reiniciar"
        "Sí, hay un final secreto",  # Corregido "Si" a "Sí"
        "Pero no te voy a decir cómo conseguirlo",  # Añadido tilde en "cómo"
        "¡Por algo es secreto...!",  # Mejorado el formato
        "¿Eh? ¡No me mires así!",  # Mejorado el formato
        "Vaya...",  # Corregido "valla" a "vaya"
    ]
    current_tip_index = 0  # Índice del tip actual
    last_tip_change_time = pygame.time.get_ticks()  # Tiempo del último cambio de tip
    font_tips = pygame.font.Font(None, 30)  # Fuente más pequeña para los tips

    while menu_running:
        current_time = time.time()
        screen.fill((0, 0, 0))

        # Título con color suave
        title_color = (255, 255, 0)  # Color fijo amarillo
        title_text = font_title.render("Agus Simulator", True, title_color)
        title_rect = title_text.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 3))
        screen.blit(title_text, title_rect)

        # Versión con brillo pulsante
        version_alpha = int(128 + 127 * math.sin(current_time * 2))
        version_color = (150, 150, 150)
        version_text = font_version.render(GAME_VERSION, True, version_color)
        screen.blit(version_text, version_rect)

        # Instrucciones con efecto de parpadeo suave
        alpha = int(200 + 55 * math.sin(current_time * 3))
        play_color = (255, 255, alpha)
        play_text = font_instructions.render("Presiona ENTER para jugar", True, play_color)
        exit_text = font_instructions.render("Presiona ESC para salir", True, (255, 255, alpha))
        screen.blit(play_text, play_rect)
        screen.blit(exit_text, exit_rect)

        # Tips con fade
        tip_alpha = int(180 + 75 * math.sin(current_time * 2))
        tip_text = font_tips.render(tips[current_tip_index], True, (200, 200, 200))
        tip_surface = pygame.Surface(tip_text.get_size(), pygame.SRCALPHA)
        tip_surface.fill((255, 255, 255, tip_alpha))
        tip_text.blit(tip_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        tip_rect = tip_text.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT - 30))
        screen.blit(tip_text, tip_rect)

        pygame.display.flip()

        # Cambiar el tip cada 5 segundos
        if pygame.time.get_ticks() - last_tip_change_time > 3000:  # 5000 ms = 5 segundos
            current_tip_index = (current_tip_index + 1) % len(tips)  # Cambiar al siguiente tip
            last_tip_change_time = pygame.time.get_ticks()  # Actualizar el tiempo del último cambio

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Salir del juego
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Presionar ENTER para jugar
                    return True  # Retornar True en lugar de solo cambiar menu_running
                if event.key == pygame.K_ESCAPE:  # Presionar ESC para salir
                    pygame.quit()
                    exit()
    
    return False  # Retornar False si se cierra la ventana

def show_mode_selection_menu(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    desc_font = pygame.font.Font(None, 36)

    modes_info = {
        "classic_mode": {
            "title": "Modo Clásico",
            "desc": "Aca no juzgamos...."
        },
        "hetero_mode": {
            "title": "Modo Hetero",
            "desc": "Solo para machos."
        },
        "infinite_mode": {
            "title": "Modo Infinito",
            "desc": "¿Cuánto aguantarás?"
        },
        "nightmare_mode": {
            "title": "MODO PESADILLA",
            "desc": "???"
        }
    }

    # Usar ruta absoluta para los modos
    if getattr(sys, 'frozen', False):
        modes_dir = os.path.join(sys._MEIPASS, 'src', 'modes')
    else:
        modes_dir = os.path.join(os.path.dirname(__file__), '..', 'modes')
    
    available_modes = [
        f.replace('.py', '') for f in os.listdir(modes_dir) 
        if f.endswith('_mode.py') 
        and f != 'base_mode.py'
        and os.path.exists(os.path.join(modes_dir, f))
        and f.replace('.py', '') in modes_info
    ]

    selected = 0
    while True:
        screen.fill((0, 0, 0))
        title = font.render("Selecciona un modo", True, (255, 255, 255))
        title_rect = title.get_rect(center=(MENU_WIDTH // 2, 100))  # Ajustar posición para el nuevo tamaño fijo
        screen.blit(title, title_rect)

        for i, mode in enumerate(available_modes):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text = small_font.render(modes_info[mode]["title"], True, color)
            text_rect = text.get_rect(center=(MENU_WIDTH // 2, 200 + i * 100))  # Ajustar posición para el nuevo tamaño fijo
            screen.blit(text, text_rect)

            # Mostrar descripción
            desc = desc_font.render(modes_info[mode]["desc"], True, (200, 200, 200))
            desc_rect = desc.get_rect(center=(MENU_WIDTH // 2, 200 + i * 100 + 30))  # Ajustar posición para el nuevo tamaño fijo
            screen.blit(desc, desc_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(available_modes)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(available_modes)
                elif event.key == pygame.K_RETURN:
                    selected_mode = available_modes[selected]
                    tutorial_shown = False
                    
                    if selected_mode == "classic_mode":
                        tutorial_shown = show_classic_tutorial(screen)
                    elif selected_mode == "hetero_mode":
                        tutorial_shown = show_hetero_tutorial(screen)
                    elif selected_mode == "infinite_mode":
                        tutorial_shown = show_infinite_tutorial(screen)
                    elif selected_mode == "nightmare_mode":
                        show_nightmare_tutorial(screen)  # No guardamos el resultado
                        continue  # Siempre volvemos al menú
                    
                    if tutorial_shown:
                        return selected_mode
                    # Si el tutorial fue cancelado (ESC), continúa en el menú de selección
                    continue
                elif event.key == pygame.K_ESCAPE:
                    return None
