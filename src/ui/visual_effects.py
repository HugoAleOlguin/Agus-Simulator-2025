"""
Utilidades visuales para el juego.
Incluye transiciones y efectos visuales.
"""
import pygame
import time


class Transition:
    """Maneja transiciones suaves entre pantallas."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.alpha = 0
        self.target_alpha = 0
        self.speed = 10
        self.callback = None
    
    def fade_in(self, speed=10):
        """Inicia fade in (de negro a visible)."""
        self.alpha = 255
        self.target_alpha = 0
        self.speed = speed
    
    def fade_out(self, speed=10, callback=None):
        """Inicia fade out (de visible a negro)."""
        self.alpha = 0
        self.target_alpha = 255
        self.speed = speed
        self.callback = callback
    
    def update(self):
        """Actualiza la transición."""
        if self.alpha < self.target_alpha:
            self.alpha = min(self.alpha + self.speed, self.target_alpha)
        elif self.alpha > self.target_alpha:
            self.alpha = max(self.alpha - self.speed, self.target_alpha)
        
        if self.alpha == 255 and self.callback:
            callback = self.callback
            self.callback = None
            callback()
    
    def draw(self, screen):
        """Dibuja la capa de transición."""
        if self.alpha > 0:
            self.surface.fill((0, 0, 0))
            self.surface.set_alpha(self.alpha)
            screen.blit(self.surface, (0, 0))
    
    def is_active(self):
        """Retorna si hay una transición activa."""
        return self.alpha != self.target_alpha


class ParticleSystem:
    """Sistema de partículas mejorado."""
    
    MAX_PARTICLES = 150  # Límite máximo para evitar caída de FPS
    
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, color, count=15, speed_range=(2, 6), life=1.0, size_range=(2, 5)):
        """
        Emite partículas desde una posición.
        """
        import random
        import math
        
        # Limitar partículas nuevas si estamos cerca del máximo
        available_slots = self.MAX_PARTICLES - len(self.particles)
        count = min(count, available_slots)
        
        if count <= 0:
            return
        
        for _ in range(count):
            angle = random.uniform(0, 360)
            speed = random.uniform(*speed_range)
            size = random.uniform(*size_range)
            
            color_var = [
                max(0, min(255, c + random.randint(-20, 20)))
                for c in color
            ]
            
            self.particles.append({
                'x': x,
                'y': y,
                'dx': math.cos(math.radians(angle)) * speed,
                'dy': math.sin(math.radians(angle)) * speed,
                'life': life,
                'max_life': life,
                'color': tuple(color_var),
                'size': size,
                'gravity': 0.1
            })
    
    def emit_burst(self, x, y, color, count=30):
        """Emite una explosión de partículas."""
        self.emit(x, y, color, count=count, speed_range=(3, 8), life=1.2, size_range=(3, 7))
    
    def emit_trail(self, x, y, color, count=5):
        """Emite partículas tipo trail/estela."""
        self.emit(x, y, color, count=count, speed_range=(0.5, 2), life=0.5, size_range=(1, 3))
    
    def update(self, dt):
        """Actualiza todas las partículas."""
        for particle in self.particles:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['dy'] += particle['gravity']
            particle['dx'] *= 0.98
            particle['dy'] *= 0.98
            particle['life'] -= dt
        
        # Usar list comprehension en lugar de remove() para O(n) vs O(n²)
        self.particles = [p for p in self.particles if p['life'] > 0]
    
    def draw(self, screen):
        """Dibuja todas las partículas."""
        for particle in self.particles:
            life_ratio = particle['life'] / particle['max_life']
            alpha = int(255 * life_ratio)
            
            size = int(particle['size'] * life_ratio)
            if size < 1:
                size = 1
            
            color = particle['color']
            pos = (int(particle['x']), int(particle['y']))
            
            if size > 2:
                glow_color = (color[0] // 2, color[1] // 2, color[2] // 2)
                pygame.draw.circle(screen, glow_color, pos, size + 2)
            
            pygame.draw.circle(screen, color, pos, size)
    
    def clear(self):
        """Limpia todas las partículas."""
        self.particles.clear()


# Mantener estos para compatibilidad pero sin funcionalidad de FPS
class FPSCounter:
    """Contador de FPS (deshabilitado)."""
    def __init__(self):
        pass
    def update(self, clock):
        pass
    def draw(self, screen):
        pass
