"""
Sistema de menús del juego.
Incluye menú principal, selección de modos y selección de skins.
"""
import pygame
import sys
import os
import math
import time
from src.config import FPS, MENU_WIDTH, MENU_HEIGHT, COLORS

GAME_VERSION = "Version 4.0"


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
            alpha = math.sin(time.time() * 2 + i * 0.5) * 30 + 225
            color = tuple(max(0, min(255, c * alpha / 255)) for c in base_color)
            text_surface = tutorial_font.render(text, True, color)
            rect = text_surface.get_rect(center=(MENU_WIDTH // 2, start_y + i * 60))
            screen.blit(text_surface, rect)

        # Texto ENTER parpadeante
        enter_font = pygame.font.Font(None, 36)
        enter_alpha = (math.sin(time.time() * 4) + 1) / 2
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
        "¿De qué país son esas banderas?",
        "¿Emojis...?",
        "Puedes reiniciar cualquier partida con R",
        "Sí, hay un final secreto",
        "Pero no te voy a decir cómo conseguirlo",
        "¡Por algo es secreto...!",
        "¿Eh? ¡No me mires así!",
        "Vaya...",
        "JESÚS????",
        "Presiona L para ver tus logros",
    ]
    current_tip_index = 0
    last_tip_change_time = pygame.time.get_ticks()
    font_tips = pygame.font.Font(None, 30)

    while menu_running:
        current_time = time.time()
        screen.fill((0, 0, 0))

        # Título con color suave
        title_color = (255, 255, 0)
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
        
        # Botón de logros
        font_logros = pygame.font.Font(None, 32)
        logros_text = font_logros.render("[L] Logros", True, (200, 180, 100))
        logros_rect = logros_text.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT // 2 + 100))
        screen.blit(logros_text, logros_rect)

        # Tips con fade
        tip_alpha = int(180 + 75 * math.sin(current_time * 2))
        tip_text = font_tips.render(tips[current_tip_index], True, (200, 200, 200))
        tip_surface = pygame.Surface(tip_text.get_size(), pygame.SRCALPHA)
        tip_surface.fill((255, 255, 255, tip_alpha))
        tip_text.blit(tip_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        tip_rect = tip_text.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT - 30))
        screen.blit(tip_text, tip_rect)

        pygame.display.flip()

        # Cambiar el tip cada 3 segundos
        if pygame.time.get_ticks() - last_tip_change_time > 3000:
            current_tip_index = (current_tip_index + 1) % len(tips)
            last_tip_change_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_l:
                    from src.ui.achievements_menu import show_achievements_menu
                    show_achievements_menu(screen, pygame.time.Clock())
    
    return False


def show_mode_selection_menu(screen, skin_manager=None):
    """
    Muestra el menú de selección de modos con selector de skins integrado.
    """
    pygame.font.init()
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    desc_font = pygame.font.Font(None, 36)
    skin_font = pygame.font.Font(None, 32)

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

    # Cargar skins disponibles
    skins = skin_manager.get_available_skins() if skin_manager else []
    current_skin_index = 0
    
    # Encontrar el índice de la skin actual
    current_skin_name = skin_manager.get_selected_skin() if skin_manager else 'img.png'
    for i, skin in enumerate(skins):
        if skin['filename'] == current_skin_name:
            current_skin_index = i
            break
    
    # Pre-cargar previews de skins
    skin_previews = {}
    for skin in skins:
        skin_previews[skin['filename']] = skin_manager.load_skin_preview(skin['path'], 70)

    selected = 0
    clock = pygame.time.Clock()
    
    while True:
        current_time = time.time()
        screen.fill((0, 0, 0))
        
        # Título con sombra y efecto
        title_pulse = abs(math.sin(current_time * 2)) * 0.2 + 0.8
        title_color = (int(255 * title_pulse), int(255 * title_pulse), int(255 * title_pulse))
        title_shadow = font.render("Selecciona un modo", True, (30, 30, 30))
        title = font.render("Selecciona un modo", True, title_color)
        title_rect = title.get_rect(center=(MENU_WIDTH // 2, 60))
        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title, title_rect)

        # Modos de juego con mejor estilo
        for i, mode in enumerate(available_modes):
            # Efecto de selección
            if i == selected:
                # Indicador de selección (flecha)
                select_arrow = small_font.render("►", True, (255, 220, 0))
                arrow_offset = int(math.sin(current_time * 5) * 3)
                screen.blit(select_arrow, (70 + arrow_offset, 130 + i * 70))
                
                color = (255, 255, 0)
                # Fondo sutil para el seleccionado
                highlight_rect = pygame.Rect(100, 125 + i * 70, MENU_WIDTH - 200, 50)
                pygame.draw.rect(screen, (40, 40, 20), highlight_rect, border_radius=8)
            else:
                color = (180, 180, 180)
            
            # Título del modo
            mode_title = modes_info[mode]["title"]
            text = small_font.render(mode_title, True, color)
            text_rect = text.get_rect(center=(MENU_WIDTH // 2, 140 + i * 70))
            
            # Sombra
            if i == selected:
                shadow = small_font.render(mode_title, True, (50, 50, 0))
                screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text, text_rect)

            # Descripción
            desc_color = (220, 220, 220) if i == selected else (120, 120, 120)
            desc = desc_font.render(modes_info[mode]["desc"], True, desc_color)
            desc_rect = desc.get_rect(center=(MENU_WIDTH // 2, 140 + i * 70 + 28))
            screen.blit(desc, desc_rect)

        # === SELECTOR DE SKINS MEJORADO ===
        skin_section_y = 480
        
        # Línea separadora con gradiente
        for i in range(3):
            alpha = 80 - i * 20
            pygame.draw.line(screen, (alpha, alpha, alpha), 
                           (100, skin_section_y - 35 + i), 
                           (MENU_WIDTH - 100, skin_section_y - 35 + i), 1)
        
        # Título de skins con sombra e indicador de controles
        skin_title = skin_font.render("<  Skin del jugador  >", True, (255, 255, 255))
        skin_title_shadow = skin_font.render("<  Skin del jugador  >", True, (50, 50, 50))
        skin_title_rect = skin_title.get_rect(center=(MENU_WIDTH // 2, skin_section_y))
        screen.blit(skin_title_shadow, (skin_title_rect.x + 2, skin_title_rect.y + 2))
        screen.blit(skin_title, skin_title_rect)
        
        if skins:
            preview_y = skin_section_y + 70
            center_x = MENU_WIDTH // 2
            
            # Posiciones para carrusel de 3 items
            positions = [
                (center_x - 130, 50, 0.5),   # Izquierda (pequeño)
                (center_x, 100, 1.0),         # Centro (grande)
                (center_x + 130, 50, 0.5),   # Derecha (pequeño)
            ]
            
            # Índices para mostrar (anterior, actual, siguiente)
            indices = [
                (current_skin_index - 1) % len(skins),
                current_skin_index,
                (current_skin_index + 1) % len(skins)
            ]
            
            # Dibujar las 3 skins del carrusel
            for i, (pos_x, size, scale) in enumerate(positions):
                skin_idx = indices[i]
                skin = skins[skin_idx]
                preview = skin_previews.get(skin['filename'])
                
                if preview:
                    # Escalar según posición
                    scaled_size = int(size * scale)
                    scaled_preview = pygame.transform.smoothscale(preview, (scaled_size, scaled_size))
                    preview_rect = scaled_preview.get_rect(center=(pos_x, preview_y))
                    
                    if i == 1:  # Skin central (seleccionada)
                        # Borde brillante simple (sin cuadrados múltiples)
                        glow_intensity = int(abs(math.sin(current_time * 3)) * 55) + 200
                        border_color = (glow_intensity, int(glow_intensity * 0.85), 0)
                        pygame.draw.rect(screen, border_color, preview_rect.inflate(8, 8), 
                                       border_radius=6, width=3)
                    else:
                        # Borde sutil para los laterales + opacidad
                        pygame.draw.rect(screen, (60, 60, 60), preview_rect.inflate(4, 4), 
                                       border_radius=4, width=1)
                    
                    screen.blit(scaled_preview, preview_rect)
            
            # Nombre de la skin
            name_font = pygame.font.Font(None, 34)
            current_skin = skins[current_skin_index]
            skin_name = current_skin['name'].upper()
            if current_skin['is_custom']:
                skin_name += " ★"
            
            name_shadow = name_font.render(skin_name, True, (30, 30, 30))
            name_text = name_font.render(skin_name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(MENU_WIDTH // 2, preview_y + 70))
            screen.blit(name_shadow, (name_rect.x + 2, name_rect.y + 2))
            screen.blit(name_text, name_rect)
            
            # Indicador de posición (puntos)
            indicator_y = preview_y + 95
            dot_spacing = 15
            total_dots_width = len(skins) * dot_spacing
            start_x = center_x - total_dots_width // 2
            
            for i in range(len(skins)):
                dot_x = start_x + i * dot_spacing + 5
                if i == current_skin_index:
                    pygame.draw.circle(screen, (255, 220, 0), (dot_x, indicator_y), 5)
                else:
                    pygame.draw.circle(screen, (80, 80, 80), (dot_x, indicator_y), 3)
        
        # === GUÍA DE CONTROLES ===
        controls_y = MENU_HEIGHT - 60
        controls_font = pygame.font.Font(None, 26)
        
        # Guía de modos (izquierda)
        modes_guide = controls_font.render("[W/S]  Seleccionar modo", True, (150, 150, 150))
        screen.blit(modes_guide, (80, controls_y))
        
        # Guía de skins (derecha)
        skins_guide = controls_font.render("[A/D]  Cambiar skin", True, (150, 150, 150))
        skins_guide_rect = skins_guide.get_rect(right=MENU_WIDTH - 80, top=controls_y)
        screen.blit(skins_guide, skins_guide_rect)
        
        # Instrucciones principales
        instructions_y = MENU_HEIGHT - 30
        inst_font = pygame.font.Font(None, 28)
        inst_text = "I Importar foto   ENTER Jugar   ESC Volver"
        inst_surface = inst_font.render(inst_text, True, (100, 100, 100))
        inst_rect = inst_surface.get_rect(center=(MENU_WIDTH // 2, instructions_y))
        screen.blit(inst_surface, inst_rect)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected = (selected - 1) % len(available_modes)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected = (selected + 1) % len(available_modes)
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and skins:
                    # Cambiar skin hacia la izquierda
                    current_skin_index = (current_skin_index - 1) % len(skins)
                    skin_manager.save_selected_skin(skins[current_skin_index]['filename'])
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and skins:
                    # Cambiar skin hacia la derecha
                    current_skin_index = (current_skin_index + 1) % len(skins)
                    skin_manager.save_selected_skin(skins[current_skin_index]['filename'])
                elif event.key == pygame.K_i:
                    # Importar skin personalizada
                    from src.utils.skin_manager import open_file_dialog
                    file_path = open_file_dialog()
                    if file_path:
                        new_filename = skin_manager.import_custom_skin(file_path)
                        if new_filename:
                            # Recargar lista de skins
                            skins = skin_manager.get_available_skins()
                            # Pre-cargar nuevo preview
                            for skin in skins:
                                if skin['filename'] not in skin_previews:
                                    skin_previews[skin['filename']] = skin_manager.load_skin_preview(skin['path'], 70)
                            # Seleccionar la nueva skin
                            for i, skin in enumerate(skins):
                                if skin['filename'] == new_filename:
                                    current_skin_index = i
                                    skin_manager.save_selected_skin(new_filename)
                                    break
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
                        show_nightmare_tutorial(screen)
                        continue
                    
                    if tutorial_shown:
                        return selected_mode
                    continue
                elif event.key == pygame.K_ESCAPE:
                    return None
