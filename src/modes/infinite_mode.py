import pygame
import time
import random
import math
import sys

from src.modes.base_mode import BaseMode
from src.utils.save_system import SaveSystem
from src.entities.player import Player
from src.entities.emoji import Emoji
from src.utils import load_image, load_music
from src.utils.achievements import get_achievement_manager, AchievementNotification
from src.ui.pause_menu import show_pause_menu, show_options_menu
from src.ui.visual_effects import FPSCounter, ParticleSystem, Transition
from src.effects.starfield import StarField

class InfiniteMode(BaseMode):
    def __init__(self, screen, clock, WIDTH, HEIGHT, player_image, emoji_image, resources):
        super().__init__(screen, clock, WIDTH, HEIGHT, player_image, emoji_image, resources)
        self.name = "Modo Infinito"
        self.player = Player(WIDTH // 2, HEIGHT - 100)
        self.player.set_image(player_image)
        self.emojis = []
        self.hearts = []
        self.lives = 3
        self.hurt_effect = 0
        self.save_system = SaveSystem()
        self.best_time = self.save_system.get_record('infinite_mode')
        self.start_time = time.time()
        self.starfield = StarField(WIDTH, HEIGHT)
        self.particles = []
        self.game_over_particles = []
        self.space_music = load_music('music/space_sound/Sci-Fi 6 Loop.ogg')

        # FPS Counter y sistema de partículas mejorado
        self.fps_counter = FPSCounter()
        self.particle_system = ParticleSystem()
        self.transition = Transition(WIDTH, HEIGHT)

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
        
        # Pre-escalar corazón del HUD (siempre es 40x40)
        self.hud_heart = pygame.transform.scale(self.heart_image, (40, 40))
        
        # Pre-crear superficie de daño (reutilizable)
        self.hurt_surface = pygame.Surface((WIDTH, HEIGHT))
        self.hurt_surface.fill((255, 0, 0))
        
        # Sistema de logros
        self.achievement_manager = get_achievement_manager()
        self.achievement_notification = AchievementNotification(WIDTH, HEIGHT)
        self.infinite_master_unlocked = False

    def create_particles(self, x, y, color, count=20):
        """Crea partículas usando el sistema mejorado."""
        self.particle_system.emit_burst(x, y, color, count)

    def update_particles(self, dt):
        """Actualiza el sistema de partículas."""
        self.particle_system.update(dt)

    def draw_particles(self):
        """Dibuja las partículas."""
        self.particle_system.draw(self.screen)

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
        
        # Panel central - Vidas (usando corazón pre-escalado)
        heart_size = 40
        heart_x = (self.WIDTH - (heart_size * 3 + 20)) // 2
        for i in range(self.lives):
            self.screen.blit(self.hud_heart, (heart_x + i * (heart_size + 10), 20))
        
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
                            # Pausar el juego
                            pause_start = time.time()
                            result = show_pause_menu(self.screen, self.clock)
                            pause_duration = time.time() - pause_start
                            # Compensar el tiempo de pausa
                            self.start_time += pause_duration
                            
                            if result == 'restart':
                                self.reset_game()
                            elif result == 'options':
                                show_options_menu(self.screen, self.clock)
                            elif result == 'menu':
                                self.save_system.save_record('infinite_mode', current_time)
                                running = False
                        elif event.key == pygame.K_r:
                            self.reset_game()

                
                # Input (WASD y flechas)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.player.move(-5, 0, self.WIDTH, self.HEIGHT)
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.player.move(5, 0, self.WIDTH, self.HEIGHT)
                if keys[pygame.K_w] or keys[pygame.K_UP]: self.player.move(0, -5, self.WIDTH, self.HEIGHT)
                if keys[pygame.K_s] or keys[pygame.K_DOWN]: self.player.move(0, 5, self.WIDTH, self.HEIGHT)
                
                # Actualizar efecto de daño (usando superficie pre-creada)
                if self.hurt_effect > 0:
                    self.hurt_effect = max(0, self.hurt_effect - dt)
                    if self.hurt_effect > 0:
                        self.hurt_surface.set_alpha(int(100 * self.hurt_effect))
                        self.screen.blit(self.hurt_surface, (0, 0))

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
                emojis_to_keep = []
                game_over = False
                for emoji in self.emojis:
                    emoji.fall(2 + current_time/20)
                    if emoji.position[1] > self.HEIGHT:
                        continue  # No mantener
                    elif emoji.isCaught(self.player.get_position(), self.player.get_size()):
                        self.lives -= 1
                        self.hurt_effect = 1.0
                        self.create_particles(
                            self.player.x + self.player.get_size()//2,
                            self.player.y + self.player.get_size()//2,
                            (255, 0, 0)
                        )
                        if self.lives <= 0:
                            self.save_system.save_record('infinite_mode', current_time)
                            if self.show_game_over(current_time):
                                self.reset_game()
                                game_over = True
                                break
                            running = False
                            game_over = True
                            break
                    else:
                        emojis_to_keep.append(emoji)
                
                if game_over:
                    continue
                self.emojis = emojis_to_keep
                
                # Update corazones (velocidad constante)
                hearts_to_keep = []
                for heart in self.hearts:
                    heart.fall(2)
                    if heart.position[1] > self.HEIGHT:
                        continue
                    elif heart.isCaught(self.player.get_position(), self.player.get_size()):
                        self.lives = min(self.lives + 1, 3)
                        self.create_particles(
                            self.player.x + self.player.get_size()//2,
                            self.player.y + self.player.get_size()//2,
                            (255, 192, 203)
                        )
                    else:
                        hearts_to_keep.append(heart)
                self.hearts = hearts_to_keep
                
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
                
                # FPS Counter
                self.fps_counter.update(self.clock)
                self.fps_counter.draw(self.screen)
                
                # Transición
                self.transition.update()
                self.transition.draw(self.screen)
                
                # Logro: Maestro Infinito (60 segundos)
                if not self.infinite_master_unlocked and current_time >= 60:
                    self.achievement_manager.unlock("infinite_master")
                    self.infinite_master_unlocked = True
                
                # Notificaciones de logros
                pending = self.achievement_manager.get_pending_notification()
                if pending:
                    self.achievement_notification.show(pending)
                self.achievement_notification.update_and_draw(self.screen, time.time())
                
                pygame.display.flip()
        except Exception as e:
            print(f"Error en modo infinito: {e}")
        finally:
            # Restaurar música de fondo al salir
            try:
                background_music = load_music('music/background.ogg')
                if background_music:
                    pygame.mixer.music.load(background_music)
                    pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"Error restaurando música: {e}")
