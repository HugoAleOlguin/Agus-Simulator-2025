import pygame  # Importar pygame para usar sus funciones de dibujo

class Emoji:
    # Cache global de imágenes escaladas (compartido entre instancias)
    _scaled_cache = {}
    
    def __init__(self, position, image):
        self.position = [float(position[0]), float(position[1])]  # Coordenadas (x, y) como flotantes
        self.image = image
        self.size = 30.0  # Tamaño inicial como flotante
        self.growth_rate = 0.05  # Tasa de crecimiento constante
        self._cached_size = 0  # Tamaño de la última imagen cacheada
        self._cached_image = None  # Imagen cacheada

    def fall(self, speed):
        self.position[1] += speed  # Mover el emoji hacia abajo
        self.size += self.growth_rate  # Incrementar el tamaño constantemente

    def isCaught(self, player_position, player_size):
        player_rect = pygame.Rect(player_position[0], player_position[1], player_size, player_size)
        emoji_rect = pygame.Rect(self.position[0], self.position[1], int(self.size), int(self.size))
        return emoji_rect.colliderect(player_rect)

    def draw(self, screen):
        current_size = int(self.size)
        # Solo re-escalar si el tamaño cambió (cada 2 píxeles para reducir escalados)
        if abs(current_size - self._cached_size) >= 2 or self._cached_image is None:
            self._cached_size = current_size
            self._cached_image = pygame.transform.scale(self.image, (current_size, current_size))
        screen.blit(self._cached_image, (int(self.position[0]), int(self.position[1])))
