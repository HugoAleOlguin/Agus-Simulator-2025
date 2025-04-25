import os  # Importar os para verificar la existencia de archivos
import pygame

def load_image(filepath):
    if not os.path.exists(filepath):  # Verificar si el archivo existe
        print(f"Advertencia: No se encontró el archivo: {filepath}. Se usará una imagen generada.")
        # Crear una superficie de color como respaldo
        image = pygame.Surface((20, 20))  # Tamaño 20x20
        image.fill((128, 128, 128))  # Color gris
        return image
    image = pygame.image.load(filepath)
    return image

def load_emojis(good_emoji_path, bad_emoji_path):
    with open(good_emoji_path, 'r') as file:
        good_emojis = file.read().splitlines()
    
    with open(bad_emoji_path, 'r') as file:
        bad_emojis = file.read().splitlines()
    
    return good_emojis, bad_emojis

def load_gif_frames(folder_path):
    """Carga los frames de un GIF desde una carpeta."""
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.png'):  # Asegurarse de que sean imágenes PNG
            frame = pygame.image.load(os.path.join(folder_path, filename))
            frames.append(frame)
    return frames