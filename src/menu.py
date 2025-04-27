import pygame
import sys

# Función para mostrar el menú inicial
def show_menu(screen):
    # $revision 1 hecha
    menu_running = True
    font_title = pygame.font.Font(None, 100)  # Fuente para el título
    font_instructions = pygame.font.Font(None, 50)  # Fuente para las instrucciones

    # Textos del menú
    title_text = font_title.render("Agus Simulator", True, (255, 255, 0))  # Título del juego en amarillo
    play_text = font_instructions.render("Presiona ENTER para jugar", True, (255, 255, 255))  # Instrucción para jugar
    exit_text = font_instructions.render("Presiona ESC para salir", True, (255, 255, 255))  # Instrucción para salir

    # Posiciones de los textos
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    play_rect = play_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    exit_rect = exit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    # Asegurarse de que la música sigue reproduciéndose
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)  # Reproducir en bucle si no está activa

    # Lista de tips
    tips = [
        "Usa W, A, S, D para moverte",
        "¿De que pais son esas banderas?",
        "Basado en hechos reales",
        "No duraras ni 20 segundos jugando este juego",
    ]
    current_tip_index = 0  # Índice del tip actual
    last_tip_change_time = pygame.time.get_ticks()  # Tiempo del último cambio de tip
    font_tips = pygame.font.Font(None, 30)  # Fuente más pequeña para los tips

    while menu_running:
        screen.fill((0, 0, 0))  # Fondo negro
        screen.blit(title_text, title_rect)  # Dibujar el título
        screen.blit(play_text, play_rect)  # Dibujar la instrucción para jugar
        screen.blit(exit_text, exit_rect)  # Dibujar la instrucción para salir

        # Dibujar el tip actual
        tip_text = font_tips.render(tips[current_tip_index], True, (200, 200, 200))  # Color gris claro
        tip_rect = tip_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 30))  # Posición abajo
        screen.blit(tip_text, tip_rect)

        pygame.display.flip()  # Actualizar la pantalla

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
                    menu_running = False
                    pygame.event.clear()  # Vaciar la cola de eventos para evitar propagación
                if event.key == pygame.K_ESCAPE:  # Presionar ESC para salir
                    pygame.quit()
                    exit()

def show_mode_selection_menu(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)

    options = [
        "1. Clásico",
        "2. Modo hetero (próximamente)",
        "3. Infinito (próximamente)"
    ]

    selected_mode = None
    while selected_mode is None:
        screen.fill((0, 0, 0))
        title = font.render("Selecciona un modo", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title, title_rect)

        for i, option in enumerate(options):
            text = small_font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 60))
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_mode = 1
                elif event.key in [pygame.K_2, pygame.K_3]:
                    # Mostrar mensaje de "próximamente" y volver al menú
                    show_coming_soon_message(screen)
                    selected_mode = None

    return selected_mode

def show_coming_soon_message(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 74)
    screen.fill((0, 0, 0))
    message = font.render("¡Próximamente!", True, (255, 255, 255))
    message_rect = message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(message, message_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Mostrar el mensaje durante 2 segundos
