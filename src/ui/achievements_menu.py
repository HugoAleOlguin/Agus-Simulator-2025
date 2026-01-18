"""
Menú de visualización de logros con navegación.
"""
import pygame
import math
import time
from src.utils.achievements import get_achievement_manager, ACHIEVEMENTS
from src.config import MENU_WIDTH, MENU_HEIGHT


def show_achievements_menu(screen, clock):
    """Muestra el menú de logros con navegación."""
    running = True
    achievement_manager = get_achievement_manager()
    achievements = achievement_manager.get_all_achievements()
    
    # Fuentes
    font_title = pygame.font.Font(None, 64)
    font_name = pygame.font.Font(None, 32)
    font_desc = pygame.font.Font(None, 24)
    font_hint = pygame.font.Font(None, 26)
    font_counter = pygame.font.Font(None, 30)
    
    # Estado de selección
    selected_index = 0
    target_scroll = 0
    current_scroll = 0.0
    
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_index = min(len(achievements) - 1, selected_index + 1)
        
        # Scroll suave para seguir la selección
        item_height = 80
        visible_start = 130
        visible_height = MENU_HEIGHT - 200
        selected_y = selected_index * item_height
        
        # Ajustar scroll para mantener selección visible
        if selected_y - target_scroll < 0:
            target_scroll = selected_y
        elif selected_y - target_scroll > visible_height - item_height:
            target_scroll = selected_y - visible_height + item_height
        
        # Interpolación suave
        current_scroll += (target_scroll - current_scroll) * 0.2
        
        # Fondo
        screen.fill((18, 18, 22))
        
        # Título
        title_color = (220, 200, 80)
        title = font_title.render("LOGROS", True, title_color)
        title_rect = title.get_rect(center=(MENU_WIDTH // 2, 45))
        screen.blit(title, title_rect)
        
        # Barra de progreso
        unlocked_count = sum(1 for a in achievements if a['unlocked'])
        progress = unlocked_count / len(achievements) if achievements else 0
        
        bar_width = 280
        bar_height = 16
        bar_x = (MENU_WIDTH - bar_width) // 2
        bar_y = 80
        
        pygame.draw.rect(screen, (40, 40, 45), (bar_x, bar_y, bar_width, bar_height), border_radius=8)
        if progress > 0:
            progress_color = (180, 160, 60) if progress < 1 else (100, 200, 100)
            pygame.draw.rect(screen, progress_color, (bar_x, bar_y, int(bar_width * progress), bar_height), border_radius=8)
        pygame.draw.rect(screen, (60, 60, 65), (bar_x, bar_y, bar_width, bar_height), width=1, border_radius=8)
        
        counter = font_counter.render(f"{unlocked_count}/{len(achievements)}", True, (200, 200, 200))
        counter_rect = counter.get_rect(center=(MENU_WIDTH // 2, bar_y + bar_height // 2))
        screen.blit(counter, counter_rect)
        
        # Línea divisora
        pygame.draw.line(screen, (50, 50, 55), (60, 115), (MENU_WIDTH - 60, 115), 1)
        
        # Área de logros
        y_start = visible_start - int(current_scroll)
        
        for i, ach in enumerate(achievements):
            y_pos = y_start + i * item_height
            
            # Solo dibujar si visible
            if y_pos < visible_start - item_height or y_pos > MENU_HEIGHT - 60:
                continue
            
            is_selected = (i == selected_index)
            is_unlocked = ach['unlocked']
            
            # Colores según estado
            if is_selected:
                if is_unlocked:
                    bg_color = (50, 48, 35)
                    border_color = (200, 180, 80)
                    name_color = (255, 255, 255)
                    desc_color = (200, 200, 180)
                else:
                    bg_color = (40, 40, 50)
                    border_color = (120, 120, 140)
                    name_color = (180, 180, 190)
                    desc_color = (120, 120, 130)
            else:
                if is_unlocked:
                    bg_color = (35, 34, 28)
                    border_color = (100, 90, 50)
                    name_color = (220, 220, 200)
                    desc_color = (150, 150, 140)
                else:
                    bg_color = (28, 28, 32)
                    border_color = (45, 45, 50)
                    name_color = (80, 80, 85)
                    desc_color = (55, 55, 60)
            
            # Panel
            panel_rect = pygame.Rect(50, y_pos, MENU_WIDTH - 100, item_height - 8)
            pygame.draw.rect(screen, bg_color, panel_rect, border_radius=8)
            
            # Borde (más grueso si seleccionado)
            border_width = 2 if is_selected else 1
            pygame.draw.rect(screen, border_color, panel_rect, width=border_width, border_radius=8)
            
            # Indicador de selección (flecha sutil)
            if is_selected:
                arrow_x = 60
                arrow_y = y_pos + (item_height - 8) // 2
                pygame.draw.polygon(screen, border_color, [
                    (arrow_x, arrow_y - 6),
                    (arrow_x + 8, arrow_y),
                    (arrow_x, arrow_y + 6)
                ])
            
            # Barra lateral para desbloqueados
            if is_unlocked:
                accent_rect = pygame.Rect(50, y_pos, 4, item_height - 8)
                pygame.draw.rect(screen, (200, 170, 50), accent_rect, border_radius=2)
            
            # Contenido
            if ach['secret'] and not is_unlocked:
                name = "???"
                desc = "Logro secreto"
            elif ach['secret'] and is_unlocked:
                name = ach.get('unlocked_name', ach['name'])
                desc = ach.get('unlocked_description', ach['description'])
            else:
                name = ach['name']
                desc = ach['description']
            
            # Nombre
            name_text = font_name.render(name, True, name_color)
            screen.blit(name_text, (80, y_pos + 12))
            
            # Descripción
            desc_text = font_desc.render(desc, True, desc_color)
            screen.blit(desc_text, (80, y_pos + 42))
            
            # Estado (solo para seleccionado)
            if is_selected:
                if is_unlocked:
                    status_text = "Desbloqueado"
                    status_color = (150, 200, 100)
                else:
                    status_text = "Bloqueado"
                    status_color = (100, 100, 110)
                
                status = font_desc.render(status_text, True, status_color)
                status_rect = status.get_rect(right=MENU_WIDTH - 70, centery=y_pos + (item_height - 8) // 2)
                screen.blit(status, status_rect)
        
        # Instrucciones
        hint = font_hint.render("[W/S] Navegar   [ESC] Volver", True, (80, 80, 85))
        hint_rect = hint.get_rect(center=(MENU_WIDTH // 2, MENU_HEIGHT - 25))
        screen.blit(hint, hint_rect)
        
        pygame.display.flip()
        clock.tick(60)
