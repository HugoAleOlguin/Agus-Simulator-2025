import os
import pygame

def get_asset_path(name):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_dir, 'src', 'assets', name)

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
