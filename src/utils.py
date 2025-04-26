import os  # Para verificar la existencia de archivos y manejar rutas
import pygame

# $revision 1 hecha

# Función para cargar una imagen desde un archivo
def load_image(filepath):
    if not os.path.exists(filepath):  # Verificar si el archivo existe
        print(f"Advertencia: No se encontró el archivo: {filepath}. Se usará una imagen generada.")
        # Crear una superficie de color como respaldo
        image = pygame.Surface((20, 20))  # Tamaño 20x20
        image.fill((128, 128, 128))  # Color gris
        return image
    image = pygame.image.load(filepath)  # Cargar la imagen desde el archivo
    return image

# Función para cargar emojis desde archivos de texto
def load_emojis(good_emoji_path, bad_emoji_path):
    with open(good_emoji_path, 'r') as file:
        good_emojis = file.read().splitlines()  # Leer emojis buenos línea por línea
    
    with open(bad_emoji_path, 'r') as file:
        bad_emojis = file.read().splitlines()  # Leer emojis malos línea por línea
    
    return good_emojis, bad_emojis

# Función para cargar los frames de un GIF desde una carpeta
def load_gif_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):  # Ordenar los archivos alfabéticamente
        if filename.endswith('.png'):  # Asegurarse de que sean imágenes PNG
            frame = pygame.image.load(os.path.join(folder_path, filename))  # Cargar cada frame
            frames.append(frame)
    return frames