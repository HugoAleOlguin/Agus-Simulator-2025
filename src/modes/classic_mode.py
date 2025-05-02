import os
import time
import random
import math
import pygame

from src.entities.emoji import Emoji
from src.entities.player import Player
from src.ui.hud import draw_timer, draw_emoji_count, draw_peaceful_progress, draw_fall_speed
from src.utils import load_image, load_gif_frames, load_audio
from src.effects.background import SimpleBackground
from config import FPS
from .base_mode import BaseMode

class ClassicMode(BaseMode):
    def __init__(self, screen, clock, WIDTH, HEIGHT, player_image, emoji_image, resources):
        super().__init__(screen, clock, WIDTH, HEIGHT, player_image, emoji_image, resources)
        # Cargar recursos usando rutas relativas
        self.victory_frames = load_gif_frames('endings/congratulations')
        self.dodge_image = load_image('endings/budagus.webp')
        self.secret_image = load_image('endings/secret.jpeg')
        # Cargar sonidos
        self.victory_sound = pygame.mixer.Sound(load_audio('music/victory.ogg'))
        self.dodge_sound = pygame.mixer.Sound(load_audio('music/budagus.ogg'))
        self.secret_sound = pygame.mixer.Sound(load_audio('music/secret.ogg'))
        
        # Verificar que tengamos frames de victoria
        if not self.victory_frames:
            print("Advertencia: No se encontraron frames para la animación de victoria")
            # Crear un frame de respaldo
            backup_frame = pygame.Surface((WIDTH, HEIGHT))
            backup_frame.fill((0, 255, 0))  # Verde como respaldo
            self.victory_frames = [backup_frame]
        
        self.secret_unlocked = False  # Nueva bandera para el final secreto
        self.background = SimpleBackground(WIDTH, HEIGHT)

    def check_endings(self, player, last_catch_time, start_time):
        current_time = time.time()
        
        # Verificar desbloqueo del final secreto sin interrumpir
        if current_time - start_time >= 200.0:
            self.secret_unlocked = True
            
        # Victoria por tamaño
        if player.get_size() >= self.HEIGHT * 1.0:
            if self.secret_unlocked:
                self.show_secret_ending(current_time - start_time)
            else:
                self.show_victory_ending(current_time - start_time)
            return True
            
        # Final de esquivar
        if current_time - last_catch_time >= 60.0:
            if self.secret_unlocked:
                self.show_secret_ending(current_time - start_time)
            else:
                self.show_dodge_ending(current_time - start_time)
            return True
            
        return False

    def show_victory_ending(self, total_time):
        pygame.mixer.music.stop()
        self.resources['stress_sound'].stop()
        self.victory_sound.play(-1)  # -1 significa reproducción en bucle
        
        running = True
        frame_index = 0
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.victory_sound.stop()
                        pygame.mixer.music.play(-1)  # Reiniciar música
                        return
                    elif event.key == pygame.K_r:
                        self.victory_sound.stop()
                        pygame.mixer.music.play(-1)  # Reiniciar música
                        self.run_mode()
                        return

            # Mostrar frame actual
            self.screen.fill((0, 0, 0))
            if self.victory_frames:  # Verificar que tengamos frames
                frame = self.victory_frames[frame_index % len(self.victory_frames)]  # Usar módulo para evitar índice fuera de rango
            else:
                frame = pygame.Surface((self.WIDTH, self.HEIGHT))
                frame.fill((0, 255, 0))  # Frame verde de respaldo
            
            # Escalar para ocupar toda la pantalla
            scaled_frame = pygame.transform.scale(frame, (self.WIDTH, self.HEIGHT))
            self.screen.blit(scaled_frame, (0, 0))
            
            # Texto con contorno
            self._draw_text_with_outline(
                "¡Te tragaste todo!\n"
                f"Tardaste {total_time:.1f}s en salir del clóset\n"
                "ENTER para volver al menú",
                self.HEIGHT - 120,
                font_size=36  # Texto más pequeño
            )

            # Texto de reinicio
            restart_text = "Presiona R para intentar de nuevo"
            font_small = pygame.font.Font(None, 32)
            restart_surface = font_small.render(restart_text, True, (200, 200, 200))
            self.screen.blit(restart_surface, (10, 10))
            
            pygame.display.flip()
            frame_index = (frame_index + 1) % len(self.victory_frames)
            clock.tick(30)

    def show_dodge_ending(self, total_time):
        pygame.mixer.music.stop()
        self.resources['stress_sound'].stop()
        self.dodge_sound.play(-1)  # -1 significa reproducción en bucle
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.dodge_sound.stop()
                        pygame.mixer.music.play(-1)  # Reiniciar música
                        return
                    elif event.key == pygame.K_r:
                        self.dodge_sound.stop()
                        pygame.mixer.music.play(-1)  # Reiniciar música
                        self.run_mode()
                        return

            self.screen.fill((0, 0, 0))
            
            # Escalar imagen para ocupar toda la pantalla
            scaled_image = pygame.transform.scale(self.dodge_image, (self.WIDTH, self.HEIGHT))
            self.screen.blit(scaled_image, (0, 0))
            
            # Texto con contorno
            self._draw_text_with_outline(
                f"¡{total_time:.2f} segundos siendo heterosexual!\n"
                "¡ALELUYA HERMANO!\n"
                "ENTER para volver al menú",
                self.HEIGHT - 120,
                font_size=36
            )

            # Texto de reinicio
            restart_text = "Presiona R para intentar de nuevo"
            font_small = pygame.font.Font(None, 32)
            restart_surface = font_small.render(restart_text, True, (200, 200, 200))
            self.screen.blit(restart_surface, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(60)

    def show_secret_ending(self, total_time):
        pygame.mixer.music.stop()
        self.resources['stress_sound'].stop()
        self.secret_sound.play(-1)  # Reproducir en bucle
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.secret_sound.stop()
                    pygame.mixer.music.play(-1)  # Reiniciar música
                    return

            self.screen.fill((0, 0, 0))
            
            # Escalar imagen para ocupar toda la pantalla
            scaled_image = pygame.transform.scale(self.secret_image, (self.WIDTH, self.HEIGHT))
            self.screen.blit(scaled_image, (0, 0))
            
            # Texto con efecto parpadeante
            color = (255, 0, 0) if (pygame.time.get_ticks() // 500) % 2 else (200, 0, 0)
            self._draw_text_with_outline(
                f"Jugaste {total_time:.2f} segundos\n"
                "Anda a un infinito enfermo...",
                self.HEIGHT - 120,
                color
            )
            
            pygame.display.flip()
            self.clock.tick(60)

    def _draw_text_with_outline(self, text, y_pos, color=(255, 255, 255), font_size=48):
        font = pygame.font.Font(None, font_size)
        y_offset = 0
        
        for line in text.split('\n'):
            # Contorno negro
            for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2)]:
                text_surface = font.render(line, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(self.WIDTH//2 + dx, y_pos + y_offset + dy))
                self.screen.blit(text_surface, text_rect)
            
            # Texto principal con el color especificado
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(self.WIDTH//2, y_pos + y_offset))
            self.screen.blit(text_surface, text_rect)
            
            y_offset += font.get_linesize()

    def run_mode(self):
        start_time = time.time()
        last_emoji_catch_time = start_time
        emoji_count = 0
        emojis = []
        player = Player(self.WIDTH // 2, self.HEIGHT - 100)
        player.set_image(self.player_image)
        running = True
        self.secret_unlocked = False  # Inicializar bandera de secreto
        MAX_EMOJIS = 25

        while running:
            current_time = time.time()
            dt = self.clock.tick(60) / 1000.0
            elapsed_time = current_time - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return self.run_mode()  # Reiniciar partida en cualquier momento

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]: player.move(-5, 0, self.WIDTH, self.HEIGHT)
            if keys[pygame.K_d]: player.move(5, 0, self.WIDTH, self.HEIGHT)
            if keys[pygame.K_w]: player.move(0, -5, self.WIDTH, self.HEIGHT)
            if keys[pygame.K_s]: player.move(0, 5, self.WIDTH, self.HEIGHT)

            # Verificar tiempo para final secreto sin interrumpir
            if elapsed_time >= 200.0:
                self.secret_unlocked = True

            if self.check_endings(player, last_emoji_catch_time, start_time):
                return

            # Generar emojis con frecuencia aumentada
            spawn_chance = max(2, 30 - int(elapsed_time // 10))  # Aumenta frecuencia con el tiempo
            if len(emojis) < MAX_EMOJIS and random.randint(1, spawn_chance) == 1:
                emojis.append(Emoji([random.randint(0, self.WIDTH - 20), 0], self.emoji_image))

            # Actualizar emojis con velocidad aumentada
            fall_speed = 2 + (elapsed_time / 10)  # Velocidad base + incremento gradual
            for emoji in emojis[:]:
                emoji.fall(fall_speed)
                if emoji.isCaught(player.get_position(), player.get_size()):
                    player.grow(self.WIDTH, self.HEIGHT)
                    emojis.remove(emoji)
                    last_emoji_catch_time = time.time()
                    emoji_count += 1
                elif emoji.position[1] > self.HEIGHT:
                    emojis.remove(emoji)

            # Actualizar y dibujar fondo
            self.background.update(dt)
            self.background.draw(self.screen)

            # Render
            player.draw(self.screen)
            for emoji in emojis:
                emoji.draw(self.screen)

            # HUD mejorado
            # Fondo semitransparente para el HUD
            hud_surface = pygame.Surface((self.WIDTH, 50)) # Ajustar el tamaño del HUD
            hud_surface.fill((0, 0, 0)) # 
            hud_surface.set_alpha(5) # Ajustar la opacidad
            self.screen.blit(hud_surface, (0, 0)) # Ajustar la posición del HUD
            
            # HUD superior con información principal
            draw_timer(self.screen, start_time, 10, 15)
            draw_emoji_count(self.screen, emoji_count, self.WIDTH - 250, 15)

            # HUD inferior con barra de progreso
            bottom_hud = pygame.Surface((self.WIDTH, 50))
            bottom_hud.fill((0, 0, 0))
            bottom_hud.set_alpha(5)
            self.screen.blit(bottom_hud, (0, self.HEIGHT - 50))

            # Barra de progreso y velocidad
            draw_peaceful_progress(
                self.screen, 
                last_emoji_catch_time, 
                self.WIDTH // 2 - 100, 
                self.HEIGHT - 35, 
                200, 
                20
            )
            
            # Velocidad con color basado en el valor
            speed_color = (
                min(255, fall_speed * 25),
                max(0, 255 - fall_speed * 25),
                0
            )
            draw_fall_speed(self.screen, fall_speed, 10, self.HEIGHT - 35, speed_color)

            # Indicador de final secreto (si está desbloqueado)
            if self.secret_unlocked:
                secret_text = "bro..."
                secret_color = (255, 215, 0) if (pygame.time.get_ticks() // 500) % 2 else (255, 165, 0)
                font = pygame.font.Font(None, 36)
                text = font.render(secret_text, True, secret_color)
                text_rect = text.get_rect(center=(self.WIDTH // 2, 25))
                self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

