import pygame  # Importar pygame para usar sus funciones de dibujo

class Emoji:
    def __init__(self, position, image):
        self.position = [float(position[0]), float(position[1])]  # Coordenadas (x, y) como flotantes
        self.image = image
        self.size = 30.0  # Tamaño inicial como flotante
        self.growth_rate = 0.05  # Tasa de crecimiento constante

    def fall(self, speed):
        self.position[1] += speed  # Mover el emoji hacia abajo
        self.size += self.growth_rate  # Incrementar el tamaño constantemente

    def isCaught(self, player_position, player_size):
        player_rect = pygame.Rect(player_position[0], player_position[1], player_size, player_size)
        emoji_rect = pygame.Rect(self.position[0], self.position[1], int(self.size), int(self.size))
        return emoji_rect.colliderect(player_rect)

    def draw(self, screen):
        scaled_image = pygame.transform.scale(self.image, (int(self.size), int(self.size)))  # Escalar la imagen
        screen.blit(scaled_image, (int(self.position[0]), int(self.position[1])))  # Dibujar la imagen
