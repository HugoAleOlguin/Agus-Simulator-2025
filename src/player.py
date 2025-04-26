import pygame

# Clase que representa al jugador
class Player:
    def __init__(self, x, y):
        self.x = x  # Posición inicial en el eje X
        self.y = y  # Posición inicial en el eje Y
        self.image = None  # Imagen del jugador (se asigna después)
        self.size = 50  # Tamaño inicial del jugador
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)  # Rectángulo del jugador

    # Asignar una imagen al jugador
    def set_image(self, image):
        self.image = image

    # Mover al jugador dentro de los límites de la ventana
    def move(self, dx, dy, window_width, window_height):
        self.x += dx
        self.y += dy
        # Limitar la posición del jugador dentro de la ventana
        self.x = max(0, min(self.x, window_width - self.size))
        self.y = max(0, min(self.y, window_height - self.size))
        self.rect.topleft = (self.x, self.y)  # Actualizar la posición del rectángulo

    # Dibujar al jugador en la pantalla
    def draw(self, screen):
        if self.image:  # Si hay una imagen asignada
            scaled_image = pygame.transform.scale(self.image, (self.size, self.size))  # Escalar la imagen
            screen.blit(scaled_image, (self.x, self.y))  # Dibujar la imagen
        else:  # Si no hay imagen, dibujar un rectángulo rojo
            pygame.draw.rect(screen, (255, 0, 0), self.rect)

    # Incrementar el tamaño del jugador
    def grow(self, max_width, max_height):
        new_size = self.size + 10  # Incrementar el tamaño en 10 unidades
        # Limitar el tamaño máximo al menor entre el ancho y el alto de la ventana
        if new_size > min(max_width, max_height):
            new_size = min(max_width, max_height)
        self.size = new_size
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)  # Actualizar el rectángulo del jugador

    # Obtener la posición del jugador
    def get_position(self):
        return (self.x, self.y)

    # Obtener el tamaño actual del jugador
    def get_size(self):
        return self.size

# $revision 1 hecha
# revision 2 completa