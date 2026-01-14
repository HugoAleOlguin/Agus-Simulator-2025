"""
Menú de pausa del juego.
Se muestra al presionar ESC durante una partida.
"""
import pygame
import math
import time
from src.config import COLORS
from src.utils.settings import get_settings


def show_pause_menu(screen, clock) -> str:
    """
    Muestra el menú de pausa.
    
    Args:
        screen: Superficie de pygame
        clock: Reloj de pygame
    
    Returns:
        'continue' - Continuar jugando
        'restart' - Reiniciar partida
        'options' - Abrir opciones (se maneja externamente)
        'menu' - Volver al menú principal
    """
    # Configuración
    width, height = screen.get_size()
    options = ['Continuar', 'Reiniciar', 'Opciones', 'Volver al menú']
    selected = 0
    
    # Fuentes
    font_title = pygame.font.Font(None, 72)
    font_option = pygame.font.Font(None, 48)
    font_hint = pygame.font.Font(None, 28)
    
    # Guardar el estado actual de la pantalla
    background = screen.copy()
    
    # Crear overlay oscuro
    overlay = pygame.Surface((width, height))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(180)
    
    # Bajar volumen de música
    settings = get_settings()
    original_volume = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(original_volume * 0.3)
    
    running = True
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC = Continuar
                    pygame.mixer.music.set_volume(original_volume)
                    return 'continue'
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.set_volume(original_volume)
                    if selected == 0:
                        return 'continue'
                    elif selected == 1:
                        return 'restart'
                    elif selected == 2:
                        return 'options'
                    elif selected == 3:
                        return 'menu'
        
        # Dibujar
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))
        
        # Título con efecto de pulso
        pulse = (math.sin(current_time * 3) + 1) / 2 * 0.3 + 0.7
        title_color = (int(255 * pulse), int(255 * pulse), int(100 * pulse))
        title = font_title.render("⏸ PAUSA", True, title_color)
        title_rect = title.get_rect(center=(width // 2, height // 4))
        screen.blit(title, title_rect)
        
        # Opciones
        start_y = height // 2 - 50
        for i, option in enumerate(options):
            if i == selected:
                # Opción seleccionada con animación
                offset = math.sin(current_time * 5) * 3
                color = (255, 255, 0)
                prefix = "► "
            else:
                offset = 0
                color = (200, 200, 200)
                prefix = "  "
            
            text = font_option.render(prefix + option, True, color)
            text_rect = text.get_rect(center=(width // 2 + offset, start_y + i * 60))
            screen.blit(text, text_rect)
        
        # Hint en la parte inferior
        hint = font_hint.render("↑↓ Navegar   ENTER Seleccionar   ESC Continuar", True, (120, 120, 120))
        hint_rect = hint.get_rect(center=(width // 2, height - 30))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.mixer.music.set_volume(original_volume)
    return 'continue'


def show_options_menu(screen, clock) -> None:
    """
    Muestra el menú de opciones.
    
    Args:
        screen: Superficie de pygame
        clock: Reloj de pygame
    """
    settings = get_settings()
    width, height = screen.get_size()
    
    options = [
        {'name': 'Música', 'key': 'music_volume', 'type': 'slider'},
        {'name': 'Efectos', 'key': 'sfx_volume', 'type': 'slider'},
    ]
    selected = 0
    
    # Fuentes
    font_title = pygame.font.Font(None, 72)
    font_option = pygame.font.Font(None, 42)
    font_value = pygame.font.Font(None, 38)
    font_hint = pygame.font.Font(None, 28)
    
    # Guardar fondo
    background = screen.copy()
    
    # Overlay
    overlay = pygame.Surface((width, height))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(200)
    
    running = True
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings.save()
                    return
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    opt = options[selected]
                    if opt['type'] == 'slider':
                        current = settings.get(opt['key'])
                        delta = 0.1 if event.key == pygame.K_RIGHT else -0.1
                        new_value = max(0.0, min(1.0, current + delta))
                        settings.set(opt['key'], round(new_value, 1))
                        # Aplicar inmediatamente si es música
                        if opt['key'] == 'music_volume':
                            pygame.mixer.music.set_volume(new_value)
                    elif opt['type'] == 'toggle':
                        current = settings.get(opt['key'])
                        settings.set(opt['key'], not current)
                elif event.key == pygame.K_RETURN:
                    opt = options[selected]
                    if opt['type'] == 'toggle':
                        current = settings.get(opt['key'])
                        settings.set(opt['key'], not current)
        
        # Dibujar
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))
        
        # Título
        title = font_title.render("⚙ OPCIONES", True, (255, 255, 255))
        title_rect = title.get_rect(center=(width // 2, 80))
        screen.blit(title, title_rect)
        
        # Opciones
        start_y = 180
        for i, opt in enumerate(options):
            is_selected = i == selected
            y_pos = start_y + i * 80
            
            # Nombre de la opción
            name_color = (255, 255, 0) if is_selected else (200, 200, 200)
            prefix = "► " if is_selected else "  "
            name_text = font_option.render(prefix + opt['name'], True, name_color)
            name_rect = name_text.get_rect(midleft=(width // 4, y_pos))
            screen.blit(name_text, name_rect)
            
            # Valor
            value = settings.get(opt['key'])
            value_x = width * 3 // 4
            
            if opt['type'] == 'slider':
                # Dibujar barra de volumen
                bar_width = 150
                bar_height = 20
                bar_x = value_x - bar_width // 2
                bar_y = y_pos - bar_height // 2
                
                # Fondo de la barra
                pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=5)
                
                # Barra llena
                fill_width = int(bar_width * value)
                if fill_width > 0:
                    fill_color = (100, 255, 100) if is_selected else (80, 200, 80)
                    pygame.draw.rect(screen, fill_color, (bar_x, bar_y, fill_width, bar_height), border_radius=5)
                
                # Borde
                border_color = (255, 255, 0) if is_selected else (100, 100, 100)
                pygame.draw.rect(screen, border_color, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=5)
                
                # Porcentaje
                pct_text = font_value.render(f"{int(value * 100)}%", True, (255, 255, 255))
                pct_rect = pct_text.get_rect(midleft=(bar_x + bar_width + 15, y_pos))
                screen.blit(pct_text, pct_rect)
                
            elif opt['type'] == 'toggle':
                # Dibujar toggle ON/OFF
                toggle_text = "ON" if value else "OFF"
                toggle_color = (100, 255, 100) if value else (255, 100, 100)
                if is_selected:
                    toggle_color = (150, 255, 150) if value else (255, 150, 150)
                
                # Fondo del toggle
                toggle_width = 80
                toggle_height = 36
                toggle_x = value_x - toggle_width // 2
                toggle_y = y_pos - toggle_height // 2
                
                bg_color = (50, 120, 50) if value else (120, 50, 50)
                pygame.draw.rect(screen, bg_color, (toggle_x, toggle_y, toggle_width, toggle_height), border_radius=18)
                
                # Texto del toggle
                text = font_value.render(toggle_text, True, toggle_color)
                text_rect = text.get_rect(center=(value_x, y_pos))
                screen.blit(text, text_rect)
        
        # Hint
        hint = font_hint.render("↑↓ Navegar   ←→ Ajustar   ESC Guardar y volver", True, (120, 120, 120))
        hint_rect = hint.get_rect(center=(width // 2, height - 30))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    settings.save()
