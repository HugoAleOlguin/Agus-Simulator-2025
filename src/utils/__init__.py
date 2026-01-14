"""
Utilidades para carga de recursos (imágenes, audio, etc.)
Funciona tanto en desarrollo como en versión compilada (PyInstaller).
"""
import os
import sys
import pygame


def get_asset_path(relative_path: str) -> str:
    """
    Obtiene la ruta absoluta de un asset.
    Funciona tanto en desarrollo como en versión compilada (PyInstaller).
    """
    # Determinar ruta base según el entorno
    if getattr(sys, 'frozen', False):
        # Ejecutable compilado con PyInstaller
        base_path = os.path.join(sys._MEIPASS, 'src', 'assets')
    else:
        # Desarrollo
        base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'src', 'assets'
        )
    
    full_path = os.path.join(base_path, relative_path)
    if os.path.exists(full_path):
        return full_path
    
    # Rutas alternativas de respaldo
    alt_paths = [
        os.path.join(os.getcwd(), 'src', 'assets', relative_path),
        os.path.join(os.getcwd(), 'assets', relative_path),
    ]
    
    for path in alt_paths:
        if os.path.exists(path):
            return path
    
    print(f"[WARN] Asset no encontrado: {relative_path}")
    return full_path


def load_image(name: str) -> pygame.Surface:
    """
    Carga una imagen y retorna una Surface de pygame.
    Si falla, retorna una Surface magenta de 50x50 px.
    """
    fullpath = get_asset_path(name)
    try:
        image = pygame.image.load(fullpath)
        # Convertir WEBP a formato compatible si es necesario
        if name.endswith('.webp'):
            surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            surface.blit(image, (0, 0))
            return surface
        return image
    except pygame.error as e:
        print(f"[ERROR] No se pudo cargar imagen: {fullpath} - {e}")
        surface = pygame.Surface((50, 50))
        surface.fill((255, 0, 255))  # Magenta para hacer obvio el error
        return surface


def load_audio(name: str) -> str:
    """
    Retorna la ruta absoluta de un archivo de audio.
    Lanza FileNotFoundError si no existe.
    """
    fullpath = get_asset_path(name)
    if not os.path.exists(fullpath):
        raise FileNotFoundError(f"Audio no encontrado: {name}")
    return fullpath


def load_music(name: str):
    """
    Retorna la ruta de un archivo de música para pygame.mixer.music.
    Retorna None si no existe.
    """
    fullpath = get_asset_path(name)
    return fullpath if os.path.exists(fullpath) else None


def load_gif_frames(name: str) -> list:
    """
    Carga todos los frames de un directorio (simulación de GIF).
    Retorna lista de Surfaces.
    """
    fullpath = get_asset_path(name)
    frames = []
    
    try:
        if os.path.isdir(fullpath):
            for filename in sorted(os.listdir(fullpath)):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    frame_path = os.path.join(fullpath, filename)
                    frame = pygame.image.load(frame_path)
                    frames.append(frame)
    except Exception as e:
        print(f"[ERROR] Error cargando frames de {name}: {e}")
    
    # Si no hay frames, crear uno de respaldo
    if not frames:
        backup = pygame.Surface((800, 600))
        backup.fill((0, 255, 0))
        frames = [backup]
    
    return frames


__all__ = ['load_image', 'load_audio', 'load_music', 'load_gif_frames', 'get_asset_path']
