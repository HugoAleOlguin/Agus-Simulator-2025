"""
Sistema de configuración del juego.
Maneja opciones como volumen con persistencia en AppData.
"""
import os
import json
import pygame


def get_appdata_dir():
    """Obtiene el directorio de AppData para el juego."""
    if os.name == 'nt':  # Windows
        appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
        save_dir = os.path.join(appdata, 'AgusSimulator')
    else:  # Linux/Mac
        save_dir = os.path.expanduser('~/.agussimulator')
    return save_dir


def get_settings_path():
    """Obtiene la ruta del archivo de configuración."""
    return os.path.join(get_appdata_dir(), 'settings.json')


class Settings:
    """Gestiona la configuración del juego."""
    
    # Valores por defecto
    DEFAULT = {
        'selected_skin': 'img.png',
        'music_volume': 0.7,
        'sfx_volume': 1.0,
    }
    
    _instance = None
    
    def __new__(cls):
        """Singleton para tener una única instancia de Settings."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.settings_path = get_settings_path()
        self.settings = self._load()
    
    def _load(self) -> dict:
        """Carga la configuración desde el archivo."""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge con defaults para asegurar todas las claves
                    return {**self.DEFAULT, **loaded}
        except Exception as e:
            print(f"[WARN] Error cargando configuración: {e}")
        return self.DEFAULT.copy()
    
    def save(self):
        """Guarda la configuración al archivo."""
        try:
            os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"[ERROR] Error guardando configuración: {e}")
    
    def get(self, key: str, default=None):
        """Obtiene un valor de configuración."""
        return self.settings.get(key, default or self.DEFAULT.get(key))
    
    def set(self, key: str, value):
        """Establece un valor de configuración."""
        self.settings[key] = value
    
    def apply_audio_settings(self):
        """Aplica la configuración de audio actual."""
        music_vol = self.get('music_volume')
        pygame.mixer.music.set_volume(music_vol)
    
    def get_music_volume(self) -> float:
        """Obtiene el volumen de música (0.0 - 1.0)."""
        return self.get('music_volume')
    
    def set_music_volume(self, volume: float):
        """Establece el volumen de música y lo aplica."""
        volume = max(0.0, min(1.0, volume))
        self.set('music_volume', volume)
        pygame.mixer.music.set_volume(volume)
    
    def get_sfx_volume(self) -> float:
        """Obtiene el volumen de efectos (0.0 - 1.0)."""
        return self.get('sfx_volume')
    
    def set_sfx_volume(self, volume: float):
        """Establece el volumen de efectos."""
        volume = max(0.0, min(1.0, volume))
        self.set('sfx_volume', volume)


# Instancia global para fácil acceso
def get_settings() -> Settings:
    """Obtiene la instancia global de Settings."""
    return Settings()
