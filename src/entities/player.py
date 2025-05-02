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
        # Limitar el movimiento del jugador dentro de los límites de la pantalla
        new_x = max(0, min(self.x + dx, window_width - self.size))
        new_y = max(0, min(self.y + dy, window_height - self.size))

        # Solo actualizar la posición si el jugador puede moverse
        if new_x != self.x or new_y != self.y:
            self.x = new_x
            self.y = new_y
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
        growth_amount = 10  # Reducido de 20 a 10 para un crecimiento más gradual
        new_size = self.size + growth_amount

        # Permitir crecer hasta el tamaño de la pantalla
        new_size = min(new_size, max_height)

        # Actualizar tamaño y posición
        self.size = new_size
        
        # Mantener al jugador dentro de la pantalla
        self.x = max(0, min(self.x, max_width - self.size))
        self.y = max(0, min(self.y, max_height - self.size))
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    # Obtener la posición del jugador
    def get_position(self):
        return (self.x, self.y)

    # Obtener el tamaño actual del jugador
    def get_size(self):
        return self.size