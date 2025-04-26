import pygame
import time

def show_congratulations(screen, start_time, gif_frames, victory_sound, clock, FPS):
    pygame.mixer.music.stop()
    victory_sound.play(-1)
    elapsed_time = time.time() - start_time
    font = pygame.font.Font(None, 74)
    text = font.render("¡Felicidades!", True, (255, 255, 255))
    time_text = font.render(f"¡Tiempo final: {elapsed_time:.2f}!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    time_rect = time_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    for frame_index in range(15 * FPS):
        screen.fill((0, 0, 0))
        screen.blit(gif_frames[frame_index % len(gif_frames)], (0, 0))

        # Dibujar contorno negro para el texto
        for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:  # Esquinas del contorno
            screen.blit(font.render("¡Felicidades!", True, (0, 0, 0)), text_rect.move(offset))
            screen.blit(font.render(f"¡Tiempo final: {elapsed_time:.2f}!", True, (0, 0, 0)), time_rect.move(offset))

        # Dibujar texto principal
        screen.blit(text, text_rect)
        screen.blit(time_text, time_rect)
        pygame.display.flip()
        clock.tick(FPS)

    victory_sound.stop()
    pygame.event.clear()

def show_peaceful_ending(screen, start_time, clock, FPS):
    pygame.mixer.music.stop()
    elapsed_time = time.time() - start_time
    font = pygame.font.Font(None, 74)
    text = font.render("¡Final Pacífico!", True, (255, 255, 255))
    time_text = font.render(f"¡Tiempo final: {elapsed_time:.2f}!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    time_rect = time_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))

    for frame_index in range(5 * FPS):
        screen.fill((0, 0, 0))

        # Dibujar contorno negro para el texto
        for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:  # Esquinas del contorno
            screen.blit(font.render("¡Final Pacífico!", True, (0, 0, 0)), text_rect.move(offset))
            screen.blit(font.render(f"¡Tiempo final: {elapsed_time:.2f}!", True, (0, 0, 0)), time_rect.move(offset))

        # Dibujar texto principal
        screen.blit(text, text_rect)
        screen.blit(time_text, time_rect)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.event.clear()


