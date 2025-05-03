import pygame
import time
import random
import math
import sys  # Agregar esta importación

from src.modes.base_mode import BaseMode
from src.utils.save_system import SaveSystem
from src.entities.player import Player
from src.entities.emoji import Emoji
from src.utils import load_image, load_music
from src.effects.starfield import StarField

class InfiniteMode(BaseMode):
    def __init__(self, screen, clock, WIDTH, HEIGHT, player_image, emoji_image, resources):
        super().__init__(screen, clock, WIDTH, HEIGHT, player_image, emoji_image, resources)
        self.name = "Modo Infinito"
        self.player = Player(WIDTH // 2, HEIGHT - 100)
        self.player.set_image(player_image)
        self.emojis = []
        self.hearts = []  # Lista para corazones cayendo
        self.lives = 3  # Reducido a 3 vidas
        self.hurt_effect = 0  # Contador para efecto de daño
        self.save_system = SaveSystem()
        self.best_time = self.save_system.get_record('infinite_mode')
        self.start_time = time.time()
        self.starfield = StarField(WIDTH, HEIGHT)
        self.particles = []
        self.game_over_particles = []  # Para explosión final
        self.space_music = load_music('music/space_sound/Sci-Fi 6 Loop.ogg')

        # Pre-renderizar superficies comunes
        self.hud_surface = pygame.Surface((WIDTH, 100))
        self.hud_surface.fill((0, 0, 0))
        self.hud_surface.set_alpha(50)
        
        # Convertir imágenes al formato de la pantalla
        self.player_image = player_image.convert_alpha()
        self.emoji_image = emoji_image.convert_alpha()
        self.heart_image = load_image('heart.png').convert_alpha()
        
        # Optimizar fuentes
        self.font = pygame.font.Font(None, 35)
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)

    def create_particles(self, x, y, color, count=20):
        for _ in range(count):
            angle = random.uniform(0, 360)
            speed = random.uniform(2, 5)
            self.particles.append({
                'x': x,
                'y': y,
                'dx': math.cos(math.radians(angle)) * speed,
                'dy': math.sin(math.radians(angle)) * speed,
                'life': 1.0,
                'color': color
            })

    def update_particles(self, dt):
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= dt * 2
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self):
        for particle in self.particles:
            alpha = int(255 * particle['life'])
            color = (*particle['color'], alpha)
            pos = (int(particle['x']), int(particle['y']))
            size = int(3 * particle['life'])
            pygame.draw.circle(self.screen, color, pos, size)

    def draw_hud(self):
        # Fondo semi-transparente para HUD
        self.screen.blit(self.hud_surface, (0, 0))

        current_time = time.time() - self.start_time
        
        # Panel izquierdo
        time_text = f"Tiempo: {current_time:.2f}"
        text = self.font.render(time_text, True, (255, 255, 255))
        self.screen.blit(text, (20, 20))
        
        record_text = f"Record: {self.best_time:.2f}"
        text = self.font.render(record_text, True, (255, 215, 0))
        self.screen.blit(text, (20, 50))
        
        # Panel central - Vidas
        heart_size = 40
        heart_x = (self.WIDTH - (heart_size * 3 + 20)) // 2
        for i in range(self.lives):
            scaled_heart = pygame.transform.scale(self.heart_image, (heart_size, heart_size))
            self.screen.blit(scaled_heart, (heart_x + i * (heart_size + 10), 20))
        
        # Panel derecho - Velocidad y dificultad
        velocity = 2 + (current_time/20)  # Aumenta más rápido
        vel_text = f"Velocidad: {velocity:.1f}x"
        vel_color = (min(255, velocity * 40), max(0, 255 - velocity * 20), 0)
        text = self.font.render(vel_text, True, vel_color)
        self.screen.blit(text, (self.WIDTH - 200, 20))

    def show_game_over(self, final_time):
        # Crear explosión final
        for _ in range(50):
            angle = random.uniform(0, 360)
            speed = random.uniform(3, 8)
            self.game_over_particles.append({
                'x': self.player.x + self.player.get_size()//2,
                'y': self.player.y + self.player.get_size()//2,
                'dx': math.cos(math.radians(angle)) * speed,
                'dy': math.sin(math.radians(angle)) * speed,
                'life': 2.0,
                'color': (255, random.randint(0, 255), 0)
            })
        
        showing_end = True
        while showing_end:
            dt = self.clock.tick(60) / 1000
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # Usar sys.exit() en lugar de exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True  # Reiniciar
                    if event.key == pygame.K_ESCAPE:
                        # Restaurar música original
                        pygame.mixer.music.load(load_music('music/background.ogg'))
                        pygame.mixer.music.play(-1)
                        return False  # Volver al menú

            # Update
            self.starfield.update()
            
            # Update partículas de explosión
            for p in self.game_over_particles[:]:
                p['x'] += p['dx']
                p['y'] += p['dy']
                p['life'] -= dt
                if p['life'] <= 0:
                    self.game_over_particles.remove(p)

            # Draw
            self.screen.fill((0, 0, 0))
            self.starfield.draw(self.screen)
            
            # Dibujar partículas de explosión
            for p in self.game_over_particles:
                alpha = int(255 * min(1.0, p['life']))
                pygame.draw.circle(self.screen, (*p['color'], alpha), 
                                (int(p['x']), int(p['y'])), 
                                int(3 * p['life']))

            # Texto del final
            text_alpha = abs(math.sin(time.time() * 3)) * 255
            game_over = self.font_big.render("PERDISTE PAPU", True, (255, 0, 0))
            game_over.set_alpha(int(text_alpha))
            text_rect = game_over.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 50))
            self.screen.blit(game_over, text_rect)
            
            # Tiempo final
            score = self.font_big.render(f"{final_time:.2f} segudos", True, (255, 255, 255))
            score_rect = score.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + 20))
            self.screen.blit(score, score_rect)
            
            # Instrucciones principales
            instructions = self.font_small.render("R - Reintentar    ESC - Menú", True, (200, 200, 200))
            inst_rect = instructions.get_rect(center=(self.WIDTH//2, self.HEIGHT - 50))
            self.screen.blit(instructions, inst_rect)
            
            # Texto para resetear récord (semi-transparente)
            reset_text = self.font_small.render("Presiona F para resetear récord", True, (150, 150, 150))
            reset_text.set_alpha(128)  # 50% transparente
            reset_rect = reset_text.get_rect(center=(self.WIDTH//2, self.HEIGHT - 20))
            self.screen.blit(reset_text, reset_rect)
            
            pygame.display.flip()

            # Manejar reset de récord
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                self.save_system.reset_records()
                self.best_time = 0

    def reset_game(self):
        self.lives = 3
        self.player.x = self.WIDTH // 2
        self.player.y = self.HEIGHT - 100
        self.emojis.clear()
        self.hearts.clear()
        self.particles.clear()
        self.game_over_particles.clear()
        self.start_time = time.time()
        self.hurt_effect = 0

    def run_mode(self):
        # Iniciar música del modo infinito
        pygame.mixer.music.load(self.space_music)
        pygame.mixer.music.play(-1)  # -1 para loop infinito
        
        running = True
        self.reset_game()
        
        try:
            while running:
                current_time = time.time() - self.start_time
                dt = self.clock.tick(60) / 1000  # Delta time
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.save_system.save_record('infinite_mode', current_time)
                            # Restaurar música original
                            pygame.mixer.music.load(load_music('music/background.ogg'))
                            pygame.mixer.music.play(-1)
                            running = False
                        if event.key == pygame.K_r:
                            self.reset_game()  # Reiniciar en cualquier momento con R
                
                # Input
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]: self.player.move(-5, 0, self.WIDTH, self.HEIGHT)
                if keys[pygame.K_d]: self.player.move(5, 0, self.WIDTH, self.HEIGHT)
                if keys[pygame.K_w]: self.player.move(0, -5, self.WIDTH, self.HEIGHT)
                if keys[pygame.K_s]: self.player.move(0, 5, self.WIDTH, self.HEIGHT)
                
                # Actualizar efecto de daño
                if self.hurt_effect > 0:
                    self.hurt_effect = max(0, self.hurt_effect - dt)
                    if self.hurt_effect > 0:
                        hurt_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
                        hurt_surface.fill((255, 0, 0))
                        hurt_surface.set_alpha(int(100 * self.hurt_effect))
                        self.screen.blit(hurt_surface, (0, 0))

                # Spawn emoji con dificultad aumentada
                spawn_chance = max(20, 60 - int(current_time / 1))
                if random.randint(1, spawn_chance) == 1:
                    x = random.randint(0, self.WIDTH - 30)
                    emoji = Emoji([x, -30], self.emoji_image)
                    self.emojis.append(emoji)
                
                # Spawn corazón (0.1% de probabilidad)
                if random.randint(1, 1000) == 1:
                    x = random.randint(0, self.WIDTH - 30)
                    heart = Emoji([x, -30], self.heart_image)
                    self.hearts.append(heart)
                
                # Update emojis con velocidad aumentada
                for emoji in self.emojis[:]:
                    emoji.fall(2 + current_time/20)  # Más rápido que antes
                    if emoji.position[1] > self.HEIGHT:
                        self.emojis.remove(emoji)
                    elif emoji.isCaught(self.player.get_position(), self.player.get_size()):
                        self.lives -= 1
                        self.hurt_effect = 1.0  # Iniciar efecto de daño
                        self.create_particles(
                            self.player.x + self.player.get_size()//2,
                            self.player.y + self.player.get_size()//2,
                            (255, 0, 0)
                        )
                        self.emojis.remove(emoji)
                        if self.lives <= 0:
                            self.save_system.save_record('infinite_mode', current_time)
                            if self.show_game_over(current_time):
                                self.reset_game()  # Reiniciar desde game over
                                continue
                            running = False  # Volver al menú si presiona ESC
                
                # Update corazones (velocidad constante)
                for heart in self.hearts[:]:
                    heart.fall(2)  # Velocidad constante
                    if heart.position[1] > self.HEIGHT:
                        self.hearts.remove(heart)
                    elif heart.isCaught(self.player.get_position(), self.player.get_size()):
                        self.lives = min(self.lives + 1, 3)  # Máximo 3 vidas
                        self.create_particles(
                            self.player.x + self.player.get_size()//2,
                            self.player.y + self.player.get_size()//2,
                            (255, 192, 203)
                        )
                        self.hearts.remove(heart)
                
                # Draw
                self.screen.fill((0, 0, 0))
                self.starfield.update()
                self.starfield.draw(self.screen)
                self.update_particles(dt)
                self.player.draw(self.screen)
                for emoji in self.emojis:
                    emoji.draw(self.screen)
                for heart in self.hearts:
                    heart.draw(self.screen)
                self.draw_particles()
                self.draw_hud()
                
                pygame.display.flip()
        except Exception as e:
            print(f"Error en modo infinito: {e}")
        finally:
            pygame.mixer.music.stop()
