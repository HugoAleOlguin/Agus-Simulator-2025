import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = None  # Placeholder para la imagen del jugador
        self.size = 50  # Tamaño inicial del jugador
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)  # Rectángulo del jugador

    def set_image(self, image):
        self.image = image

    def move(self, dx, dy, window_width, window_height):
        # Actualizar la posición del jugador, limitando los bordes de la ventana
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, window_width - self.size))  # Limitar entre 0 y el ancho de la ventana
        self.y = max(0, min(self.y, window_height - self.size))  # Limitar entre 0 y el alto de la ventana
        self.rect.topleft = (self.x, self.y)  # Actualizar la posición del rectángulo

    def draw(self, screen):
        # Dibujar la imagen del jugador si está disponible, de lo contrario, dibujar un rectángulo
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (self.size, self.size))  # Escalar la imagen al tamaño actual
            screen.blit(scaled_image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)  # Dibujar un rectángulo rojo como marcador

    def grow(self, max_width, max_height):
        # Incrementar el tamaño del jugador
        new_size = self.size + 10

        # Limitar el tamaño máximo al de la ventana
        if new_size > min(max_width, max_height):  # El tamaño máximo es el menor entre el ancho y el alto de la ventana
            new_size = min(max_width, max_height)

        self.size = new_size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)  # Actualizar el rectángulo del jugador

    def get_position(self):
        # Retornar la posición del jugador
        return (self.x, self.y)

    def get_size(self):
        # Retornar el tamaño del jugador como un entero
        return self.size