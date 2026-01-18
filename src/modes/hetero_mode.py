import time
import random
import math
import pygame

from src.entities.emoji import Emoji
from src.entities.player import Player
from src.ui.hud import draw_timer, draw_fall_speed
from src.ui.pause_menu import show_pause_menu, show_options_menu
from src.config import FPS
from src.utils import load_audio, load_image
from src.utils.achievements import get_achievement_manager, AchievementNotification
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
        
        # Power-up de ralentización de emojis
        self.slowdown_active = False
        self.slowdown_end_time = 0
        self.slowdown_fade_end_time = 0
        self.slowdown_multiplier = 1.0  # 1.0 = normal, 0.3 = lento
        
        # Sistema de logros
        self.achievement_manager = get_achievement_manager()
        self.achievement_notification = AchievementNotification(WIDTH, HEIGHT)
        self.survivor_unlocked = False

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
        powerups = []  # Lista de power-ups
        running = True
        MAX_EMOJIS = 15
        self.slowdown_active = False
        self.slowdown_end_time = 0
        self.slowdown_fade_end_time = 0
        self.slowdown_multiplier = 1.0

        while running:
            current_time = time.time()
            elapsed_time = current_time - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return self.run_mode()
                    elif event.key == pygame.K_ESCAPE:
                        # Pausar el juego
                        pause_start = time.time()
                        result = show_pause_menu(self.screen, self.clock)
                        pause_duration = time.time() - pause_start
                        start_time += pause_duration
                        # Compensar pausa en power-up
                        if self.slowdown_active:
                            self.slowdown_end_time += pause_duration
                            self.slowdown_fade_end_time += pause_duration
                        
                        if result == 'restart':
                            return self.run_mode()
                        elif result == 'options':
                            show_options_menu(self.screen, self.clock)
                        elif result == 'menu':
                            return

            # Actualizar estado de ralentización
            if self.slowdown_active:
                if current_time > self.slowdown_fade_end_time:
                    # Terminó completamente
                    self.slowdown_active = False
                    self.slowdown_multiplier = 1.0
                elif current_time > self.slowdown_end_time:
                    # Fase de transición suave (2 segundos de fade-out)
                    fade_progress = (current_time - self.slowdown_end_time) / 2.0
                    self.slowdown_multiplier = 0.3 + (0.7 * fade_progress)  # 0.3 -> 1.0
                else:
                    # Efecto completo
                    self.slowdown_multiplier = 0.3
            
            # Movimiento del jugador (WASD y flechas)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]: player.move(-5, 0, self.WIDTH, self.HEIGHT)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]: player.move(5, 0, self.WIDTH, self.HEIGHT)
            if keys[pygame.K_w] or keys[pygame.K_UP]: player.move(0, -5, self.WIDTH, self.HEIGHT)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]: player.move(0, 5, self.WIDTH, self.HEIGHT)

            # Generar emojis
            if len(emojis) < MAX_EMOJIS and random.randint(1, 10) == 1:
                emojis.append(Emoji([random.randint(0, self.WIDTH - 20), 0], self.emoji_image))
            
            # Spawn de power-up de ralentización (~0.3% de probabilidad, muy raro)
            if random.randint(1, 350) == 1 and len(powerups) < 1:
                powerup_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
                # Dibujar reloj de arena
                pygame.draw.polygon(powerup_surface, (100, 200, 255), 
                                   [(5, 0), (25, 0), (15, 15)])  # Triángulo superior
                pygame.draw.polygon(powerup_surface, (100, 200, 255), 
                                   [(5, 30), (25, 30), (15, 15)])  # Triángulo inferior
                powerups.append({
                    'x': random.randint(50, self.WIDTH - 50),
                    'y': -30,
                    'surface': powerup_surface
                })

            # Actualizar emojis con velocidad dinámica (afectada por slowdown)
            base_fall_speed = 2 + (elapsed_time / 10)
            fall_speed = base_fall_speed * self.slowdown_multiplier
            emojis_to_remove = []
            
            # Color de velocidad basado en el peligro
            danger_level = min(255, int(base_fall_speed * 25))
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
            
            # Actualizar power-ups
            powerups_to_keep = []
            for powerup in powerups:
                powerup['y'] += 2.5  # Velocidad fija lenta
                
                # Colisión con jugador
                player_rect = pygame.Rect(player.x, player.y, player.get_size(), player.get_size())
                powerup_rect = pygame.Rect(powerup['x'], powerup['y'], 30, 30)
                
                if player_rect.colliderect(powerup_rect):
                    self.slowdown_active = True
                    self.slowdown_end_time = current_time + 4.0  # 4 segundos de efecto completo
                    self.slowdown_fade_end_time = current_time + 6.0  # + 2 segundos de fade
                elif powerup['y'] <= self.HEIGHT:
                    powerups_to_keep.append(powerup)
            powerups = powerups_to_keep

            # Dibujar fondo
            self.draw_background(current_time)

            player.draw(self.screen)
            for emoji in emojis:
                emoji.draw(self.screen)
            
            # Dibujar power-ups con glow cyan
            for powerup in powerups:
                # Glow cyan pulsante
                glow_intensity = int(abs(math.sin(elapsed_time * 6)) * 80) + 100
                glow_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (100, 200, 255, glow_intensity), (25, 25), 20)
                self.screen.blit(glow_surface, (powerup['x'] - 10, powerup['y'] - 10))
                self.screen.blit(powerup['surface'], (powerup['x'], powerup['y']))
            
            # Indicador de slowdown activo
            if self.slowdown_active:
                if current_time <= self.slowdown_end_time:
                    remaining = self.slowdown_end_time - current_time
                    slowdown_text = f"SLOW! {remaining:.1f}s"
                    text_color = (100, 200, 255)
                else:
                    slowdown_text = "Normalizando..."
                    text_color = (150, 180, 200)
                
                slowdown_font = pygame.font.Font(None, 28)
                slowdown_surface = slowdown_font.render(slowdown_text, True, text_color)
                slowdown_rect = slowdown_surface.get_rect(center=(self.WIDTH // 2, 30))
                self.screen.blit(slowdown_surface, slowdown_rect)

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
            
            # Logro: Superviviente (30 segundos)
            if not self.survivor_unlocked and elapsed_time >= 30:
                self.achievement_manager.unlock("survivor_30")
                self.survivor_unlocked = True
            
            # Notificaciones de logros
            pending = self.achievement_manager.get_pending_notification()
            if pending:
                self.achievement_notification.show(pending)
            self.achievement_notification.update_and_draw(self.screen, time.time())

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
