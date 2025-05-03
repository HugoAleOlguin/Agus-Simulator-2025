import time
import random
import math
import pygame

from src.entities.emoji import Emoji
from src.entities.player import Player
from src.ui.hud import draw_timer, draw_fall_speed
from src.config import FPS
from src.utils import load_audio, load_image
from src.modes.base_mode import BaseMode

class HeteroMode(BaseMode):
    def __init__(self, screen, clock, WIDTH, HEIGHT, player_image, emoji_image, resources):
        super().__init__(screen, clock, WIDTH, HEIGHT, player_image, emoji_image, resources)
        self.death_sound = pygame.mixer.Sound(load_audio('music/death.ogg'))
        self.death_image = load_image('endings/death.webp')
        if not self.death_image:
            print("Error cargando imagen de muerte, usando fondo negro")
        self.bg_time = 0
        self.wave_offset = 0

    def draw_background(self, current_time):
        # Colores base suaves
        top_color = (180, 180, 200)
        bottom_color = (160, 160, 180)
        
        # Dibujar degradado vertical
        for y in range(self.HEIGHT):
            factor = y / self.HEIGHT
            color = [
                int(top_color[i] * (1 - factor) + bottom_color[i] * factor)
                for i in range(3)
            ]
            pygame.draw.line(self.screen, color, (0, y), (self.WIDTH, y))

        # Dibujar ondas horizontales sutiles
        self.wave_offset += 0.02
        wave_color = (170, 170, 190, 30)
        wave_surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        
        for i in range(0, self.HEIGHT, 40):
            points = []
            for x in range(0, self.WIDTH, 5):
                y = i + math.sin(x * 0.02 + self.wave_offset) * 5
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(wave_surface, wave_color, False, points, 2)
        
        self.screen.blit(wave_surface, (0, 0))

    def show_death_ending(self, total_time):
        pygame.mixer.music.stop()
        if 'stress_sound' in self.resources:  # Corregido de 'death' a 'stress_sound'
            self.resources['stress_sound'].stop()
        self.death_sound.play(-1)  # -1 significa reproducción en bucle
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.death_sound.stop()
                        pygame.mixer.music.play(-1)  # Reiniciar música de fondo
                        return
                    elif event.key == pygame.K_r:
                        self.death_sound.stop()
                        pygame.mixer.music.play(-1)  # Reiniciar música de fondo
                        self.run_mode()
                        return

            self.screen.fill((0, 0, 0))  # Fondo negro como respaldo
            
            # Mostrar imagen de fondo si está disponible
            if self.death_image:
                scaled_image = pygame.transform.scale(self.death_image, (self.WIDTH, self.HEIGHT))
                self.screen.blit(scaled_image, (0, 0))
            
            # Texto de reinicio
            restart_text = "Presiona R para intentar de nuevo"
            font_small = pygame.font.Font(None, 32)
            restart_surface = font_small.render(restart_text, True, (200, 200, 200))
            self.screen.blit(restart_surface, (10, 10))
            
            # Texto con contorno
            self._draw_text_with_outline(
                "Te han cancelado\n"
                f"Duraste solo {total_time:.2f} segundos siendo heterosexual\n"
                "ENTER para volver al menú",
                self.HEIGHT - 120,
                36  # Tamaño de fuente más pequeño
            )
            
            pygame.display.flip()
            self.clock.tick(60)

    def run_mode(self):
        start_time = time.time()
        player = Player(self.WIDTH // 2, self.HEIGHT - 100)
        player.set_image(self.player_image)
        emojis = []
        running = True
        MAX_EMOJIS = 15

        while running:
            current_time = time.time()
            elapsed_time = current_time - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return self.run_mode()  # Reiniciar partida

            # Movimiento del jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]: player.move(-5, 0, self.WIDTH, self.HEIGHT)
            if keys[pygame.K_d]: player.move(5, 0, self.WIDTH, self.HEIGHT)
            if keys[pygame.K_w]: player.move(0, -5, self.WIDTH, self.HEIGHT)
            if keys[pygame.K_s]: player.move(0, 5, self.WIDTH, self.HEIGHT)

            # Generar emojis
            if len(emojis) < MAX_EMOJIS and random.randint(1, 10) == 1: # Ajustar la probabilidad
                emojis.append(Emoji([random.randint(0, self.WIDTH - 20), 0], self.emoji_image)) # Usar el emoji_image pasado

            # Actualizar emojis con velocidad dinámica
            fall_speed = 2 + (elapsed_time / 10)
            emojis_to_remove = []
            
            # Color de velocidad basado en el peligro
            danger_level = min(255, int(fall_speed * 25))
            speed_color = (danger_level, 255 - danger_level, 0)

            # Actualizar emojis
            for emoji in emojis:
                emoji.fall(fall_speed)
                if emoji.isCaught(player.get_position(), player.get_size()):
                    self.show_death_ending(elapsed_time)
                    return
                elif emoji.position[1] > self.HEIGHT:
                    emojis_to_remove.append(emoji)

            for emoji in emojis_to_remove:
                emojis.remove(emoji)

            # Dibujar fondo
            self.draw_background(current_time)

            player.draw(self.screen)
            for emoji in emojis:
                emoji.draw(self.screen)

            # HUD mejorado
            # Timer con sombra
            font = pygame.font.Font(None, 36)
            timer_text = f"Tiempo: {elapsed_time:.2f}s"
            shadow = font.render(timer_text, True, (0, 0, 0))
            text = font.render(timer_text, True, (255, 255, 255))
            self.screen.blit(shadow, (12, 12))
            self.screen.blit(text, (10, 10))

            # Velocidad con color de peligro
            speed_text = f"Velocidad: {fall_speed:.2f}"
            speed_shadow = font.render(speed_text, True, (0, 0, 0))
            speed_display = font.render(speed_text, True, speed_color)
            self.screen.blit(speed_shadow, (12, 42))
            self.screen.blit(speed_display, (10, 40))

            pygame.display.flip()
            self.clock.tick(FPS)

    def _draw_text_with_outline(self, text, y_pos, font_size=48):
        font = pygame.font.Font(None, font_size)
        y_offset = 0
        
        for line in text.split('\n'):
            # Contorno negro
            for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2)]:
                text_surface = font.render(line, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(self.WIDTH//2 + dx, y_pos + y_offset + dy))
                self.screen.blit(text_surface, text_rect)
            
            # Texto principal en blanco
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.WIDTH//2, y_pos + y_offset))
            self.screen.blit(text_surface, text_rect)
            
            y_offset += font.get_linesize()
