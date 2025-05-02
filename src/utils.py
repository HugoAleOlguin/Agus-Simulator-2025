import os
import pygame

def get_asset_path(relative_path):
    """Busca un asset en múltiples ubicaciones posibles"""
    # Lista de posibles ubicaciones de assets
    base_paths = [
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'),  # ../assets
        os.path.join(os.path.dirname(__file__), 'assets'),  # ./assets
    ]
    
    for base_path in base_paths:
        full_path = os.path.join(base_path, relative_path)
        if os.path.exists(full_path):
            print(f"Asset encontrado en: {full_path}")
            return full_path
            
    print(f"No se encontró el asset: {relative_path}")
    print(f"Rutas buscadas:")
    for base_path in base_paths:
        print(f"- {os.path.join(base_path, relative_path)}")
    return None

def load_image(relative_path):
    """Carga una imagen con mejor manejo de errores"""
    full_path = get_asset_path(relative_path)
    if not full_path:
        return None
        
    try:
        image = pygame.image.load(full_path)
        if relative_path.endswith('.webp'):
            # Convertir WEBP a formato compatible
            surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            surface.blit(image, (0, 0))
            return surface
        return image
    except Exception as e:
        print(f"Error cargando imagen: {e}")
        return None

def load_audio(relative_path):
    """Carga un archivo de audio con mejor manejo de errores"""
    full_path = get_asset_path(relative_path)
    if not full_path:
        raise FileNotFoundError(f"No se encontró el archivo de audio: {relative_path}")
    return full_path

def load_gif_frames(relative_path):
    full_path = get_asset_path(relative_path)
    if not full_path:
        print(f"No se encontró la carpeta: {relative_path}")
        return []
        
    frames = []
    try:
        for filename in sorted(os.listdir(full_path)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                frame_path = os.path.join(full_path, filename)
                try:
                    frame = pygame.image.load(frame_path)
                    frames.append(frame)
                except Exception as e:
                    print(f"Error cargando frame {filename}: {e}")
                    
        if not frames:
            print(f"No se encontraron imágenes válidas en: {relative_path}")
            backup_frame = pygame.Surface((800, 600))
            backup_frame.fill((0, 255, 0))
            frames = [backup_frame]
            
    except Exception as e:
        print(f"Error accediendo a la carpeta de frames: {e}")
        return []
        
    return frames