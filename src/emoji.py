import pygame  # Importar pygame para usar sus funciones de dibujo

class Emoji:
    def __init__(self, position, image):
        self.position = position  # Coordenadas (x, y)
        self.image = image  # Imagen del emoji
        self.size = 30  # Tamaño del emoji

    def fall(self, speed):
        self.position[1] += speed  # Mover el emoji hacia abajo
        self.size += 0.01  # Incrementar ligeramente el tamaño del emoji con cada caída

    def isCaught(self, player_position, player_size):
        # player_size es un entero que representa el ancho y alto del jugador (cuadrado)
        player_rect = pygame.Rect(player_position[0], player_position[1], player_size, player_size)
        emoji_rect = pygame.Rect(self.position[0], self.position[1], self.size, self.size)
        return emoji_rect.colliderect(player_rect)

    def draw(self, screen):
        scaled_image = pygame.transform.scale(self.image, (int(self.size), int(self.size)))  # Escalar la imagen del emoji
        screen.blit(scaled_image, self.position)