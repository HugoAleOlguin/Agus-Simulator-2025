import pygame
import time

def show_biggest_ally_ending(screen, start_time, gif_frames, victory_sound, clock, FPS):
    pygame.mixer.music.stop()
    victory_sound.play(-1)
    elapsed_time = time.time() - start_time
    font = pygame.font.Font(None, 74)
    text = font.render("¡Eres el mayor aliade!", True, (255, 255, 255))
    time_text = font.render("¡Te comiste todo", True, (255, 255, 255))
    time_text_2 = font.render(f"en {elapsed_time:.2f} segundos!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    time_rect = time_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
    time_rect_2 = time_text_2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 90))

    for frame_index in range(15 * FPS):
        screen.fill((0, 0, 0))
        screen.blit(gif_frames[frame_index % len(gif_frames)], (0, 0))

        # Dibujar contorno negro para el texto
        for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            screen.blit(font.render("¡Eres el mayor aliade!", True, (0, 0, 0)), text_rect.move(offset))
            screen.blit(font.render("¡Te comiste todo", True, (0, 0, 0)), time_rect.move(offset))
            screen.blit(font.render(f"en {elapsed_time:.2f} segundos!", True, (0, 0, 0)), time_rect_2.move(offset))

        # Dibujar texto principal
        screen.blit(text, text_rect)
        screen.blit(time_text, time_rect)
        screen.blit(time_text_2, time_rect_2)
        pygame.display.flip()
        clock.tick(FPS)

    victory_sound.stop()
    pygame.event.clear()

def show_dodger_ending(screen, start_time, dodger_image, budagus_sound, clock, FPS):
    pygame.mixer.music.stop()
    budagus_sound.play()  # Reproducir la canción una vez
    elapsed_time = time.time() - start_time
    font = pygame.font.Font(None, 74)
    text = font.render("¡Esquivaste todo", True, (255, 255, 255))
    time_text_2 = font.render("durante 30 segundos!", True, (255, 255, 255))
    joke_text = font.render("El Agus lo aprueba...", True, (255, 255, 255))

    # Posicionar los textos en la parte inferior
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 200))
    time_rect = time_text_2.get_rect(center=(screen.get_width() // 2, screen.get_height() - 150))
    joke_rect = joke_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))

    # Redimensionar la imagen para que cubra toda la ventana
    dodger_image = pygame.transform.scale(dodger_image, (screen.get_width(), screen.get_height()))

    # Obtener la duración de la canción
    song_duration = budagus_sound.get_length()
    start_time = time.time()

    while time.time() - start_time < song_duration:
        screen.fill((0, 0, 0))
        screen.blit(dodger_image, (0, 0))  # Dibujar la imagen redimensionada para cubrir toda la ventana

        # Dibujar contorno negro para los textos
        for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            screen.blit(font.render("¡Esquivaste todo", True, (0, 0, 0)), text_rect.move(offset))
            screen.blit(font.render("durante 30 segundos!", True, (0, 0, 0)), time_rect.move(offset))
            screen.blit(font.render("El Agus lo aprueba...", True, (0, 0, 0)), joke_rect.move(offset))

        # Dibujar texto principal
        screen.blit(text, text_rect)
        screen.blit(time_text_2, time_rect)
        screen.blit(joke_text, joke_rect)
        pygame.display.flip()
        clock.tick(FPS)

    budagus_sound.stop()  # Detener la canción al finalizar el ending
    pygame.event.clear()

def show_secret_ending(screen, start_time, secret_sound, clock, FPS):
    pygame.mixer.music.stop()
    secret_sound.play()  # Reproducir la canción del final secreto
    elapsed_time = time.time() - start_time
    font = pygame.font.Font(None, 74)
    text = font.render("¡FINAL SECRETO!", True, (255, 255, 255))
    time_text = font.render(f"¡Jugaste {elapsed_time:.2f} segundos!", True, (255, 255, 255))
    joke_text = font.render("Toca pasto, wachín...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 70))
    time_rect = time_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    joke_rect = joke_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 70))

    for frame_index in range(5 * FPS):
        screen.fill((0, 0, 0))

        # Dibujar contorno negro para el texto
        for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            screen.blit(font.render("¡FINAL SECRETO!", True, (0, 0, 0)), text_rect.move(offset))
            screen.blit(font.render(f"¡Jugaste {elapsed_time:.2f} segundos!", True, (0, 0, 0)), time_rect.move(offset))
            screen.blit(font.render("Toca pasto, wachín...", True, (0, 0, 0)), joke_rect.move(offset))

        # Dibujar texto principal
        screen.blit(text, text_rect)
        screen.blit(time_text, time_rect)
        screen.blit(joke_text, joke_rect)
        pygame.display.flip()
        clock.tick(FPS)

    secret_sound.stop()  # Detener la canción al finalizar el ending
    pygame.event.clear()


