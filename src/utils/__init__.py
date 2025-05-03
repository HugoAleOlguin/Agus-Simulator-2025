import os
import sys
import pygame

def get_absolute_path(relative_path):
    """Obtiene la ruta absoluta para assets tanto en desarrollo como compilado"""
    try:
        if getattr(sys, 'frozen', False):
            base_path = os.path.join(sys._MEIPASS, 'src', 'assets')
        else:
            base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src', 'assets')
        
        full_path = os.path.join(base_path, relative_path)
        if os.path.exists(full_path):
            return full_path
            
        # Intentar rutas alternativas si no se encuentra
        alt_paths = [
            os.path.join(os.getcwd(), 'src', 'assets', relative_path),
            os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else os.getcwd(), relative_path)
        ]
        
        for path in alt_paths:
            if os.path.exists(path):
                return path
                
        print(f"No se pudo encontrar el asset: {relative_path}")
        print(f"Rutas intentadas:\n" + "\n".join([full_path] + alt_paths))
        return full_path
        
    except Exception as e:
        print(f"Error resolviendo ruta para {relative_path}: {e}")
        return None

def get_asset_path(name):
    path = get_absolute_path(name)
    if not path or not os.path.exists(path):
        print(f"Asset no encontrado: {name}")
        # Intentar buscar en rutas alternativas
        alt_paths = [
            os.path.join(os.getcwd(), 'src', 'assets', name),
            os.path.join(os.getcwd(), 'assets', name),
            os.path.join(os.path.dirname(sys.executable), 'src', 'assets', name)
        ]
        for alt_path in alt_paths:
            if os.path.exists(alt_path):
                print(f"Asset encontrado en ruta alternativa: {alt_path}")
                return alt_path
    return path

def load_image(name):
    fullpath = get_asset_path(name)
    try:
        image = pygame.image.load(fullpath)
        return image
    except pygame.error as e:
        print(f'Warning: Cannot load image: {fullpath}')
        surface = pygame.Surface((50, 50))
        surface.fill((255, 0, 255))
        return surface

def load_audio(name):
    fullpath = get_asset_path(name)
    try:
        return pygame.mixer.Sound(fullpath)
    except pygame.error as e:
        print(f'Warning: Cannot load sound: {fullpath}')
        return None

def load_music(name):
    fullpath = get_asset_path(name)
    return fullpath if os.path.exists(fullpath) else None

def load_gif_frames(name):
    fullpath = get_asset_path(name)
    frames = []
    try:
        if os.path.isdir(fullpath):
            for filename in sorted(os.listdir(fullpath)):
                if filename.endswith(('.png', '.jpg', '.webp')):
                    frame_path = os.path.join(fullpath, filename)
                    frame = pygame.image.load(frame_path)
                    frames.append(frame)
    except Exception as e:
        print(f"Error loading gif frames: {e}")
        # Create backup frame
        backup = pygame.Surface((800, 600))
        backup.fill((0, 255, 0))
        frames = [backup]
    return frames

__all__ = ['load_image', 'load_audio', 'load_music', 'load_gif_frames']
