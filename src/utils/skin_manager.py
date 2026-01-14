"""
Sistema de gestión de skins para el jugador.
Permite seleccionar skins predeterminadas o importar imágenes personalizadas.
"""
import os
import sys
import json
import shutil
import pygame


def get_data_path():
    """Obtiene la ruta del directorio de datos."""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base, 'data')


def get_skins_path():
    """Obtiene la ruta del directorio de skins predeterminadas."""
    if getattr(sys, 'frozen', False):
        base = os.path.join(sys._MEIPASS, 'src', 'assets', 'skins')
    else:
        base = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'src', 'assets', 'skins'
        )
    return base


class SkinManager:
    """Gestiona las skins del jugador."""
    
    def __init__(self):
        self.skins_dir = get_skins_path()
        self.data_dir = get_data_path()
        self.custom_skins_dir = os.path.join(self.data_dir, 'custom_skins')
        self.settings_path = os.path.join(self.data_dir, 'settings.json')
        
        # Crear directorio de skins personalizadas si no existe
        if not os.path.exists(self.custom_skins_dir):
            os.makedirs(self.custom_skins_dir)
        
        self.current_skin = self.get_selected_skin()
    
    def get_available_skins(self) -> list:
        """
        Retorna lista de skins disponibles.
        Cada elemento es un dict con: name, path, is_custom
        """
        skins = []
        
        # Skins predeterminadas
        if os.path.exists(self.skins_dir):
            for filename in sorted(os.listdir(self.skins_dir)):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    skins.append({
                        'name': os.path.splitext(filename)[0],
                        'filename': filename,
                        'path': os.path.join(self.skins_dir, filename),
                        'is_custom': False
                    })
        
        # Skins personalizadas
        if os.path.exists(self.custom_skins_dir):
            for filename in sorted(os.listdir(self.custom_skins_dir)):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    skins.append({
                        'name': os.path.splitext(filename)[0],
                        'filename': filename,
                        'path': os.path.join(self.custom_skins_dir, filename),
                        'is_custom': True
                    })
        
        return skins
    
    def load_skin_image(self, skin_filename: str) -> pygame.Surface:
        """Carga y retorna una skin como Surface de pygame."""
        # Buscar en skins predeterminadas
        path = os.path.join(self.skins_dir, skin_filename)
        if not os.path.exists(path):
            # Buscar en skins personalizadas
            path = os.path.join(self.custom_skins_dir, skin_filename)
        
        if not os.path.exists(path):
            # Usar skin por defecto
            path = os.path.join(self.skins_dir, 'img.png')
        
        try:
            image = pygame.image.load(path)
            return image
        except pygame.error as e:
            print(f"[ERROR] No se pudo cargar skin: {path} - {e}")
            # Crear superficie de respaldo
            surface = pygame.Surface((400, 400))
            surface.fill((255, 0, 255))
            return surface
    
    def load_skin_preview(self, skin_path: str, size: int = 80) -> pygame.Surface:
        """Carga una preview de la skin en tamaño reducido."""
        try:
            image = pygame.image.load(skin_path)
            # Convertir a formato de 32-bit para compatibilidad con smoothscale
            image = image.convert_alpha()
            # Escalar manteniendo aspecto
            orig_w, orig_h = image.get_size()
            scale = min(size / orig_w, size / orig_h)
            new_size = (int(orig_w * scale), int(orig_h * scale))
            return pygame.transform.smoothscale(image, new_size)
        except Exception as e:
            print(f"[ERROR] No se pudo cargar preview: {skin_path} - {e}")
            surface = pygame.Surface((size, size))
            surface.fill((255, 0, 255))
            return surface
    
    def import_custom_skin(self, file_path: str) -> str:
        """
        Importa una imagen como skin personalizada.
        Retorna el nombre del archivo si fue exitoso, None si falló.
        """
        if not os.path.exists(file_path):
            return None
        
        try:
            # Copiar archivo al directorio de skins personalizadas
            filename = os.path.basename(file_path)
            # Evitar sobrescribir
            base, ext = os.path.splitext(filename)
            dest_path = os.path.join(self.custom_skins_dir, filename)
            counter = 1
            while os.path.exists(dest_path):
                filename = f"{base}_{counter}{ext}"
                dest_path = os.path.join(self.custom_skins_dir, filename)
                counter += 1
            
            shutil.copy2(file_path, dest_path)
            return filename
        except Exception as e:
            print(f"[ERROR] No se pudo importar skin: {e}")
            return None
    
    def save_selected_skin(self, skin_filename: str):
        """Guarda la skin seleccionada en settings.json."""
        settings = self._load_settings()
        settings['selected_skin'] = skin_filename
        self._save_settings(settings)
        self.current_skin = skin_filename
    
    def get_selected_skin(self) -> str:
        """Obtiene la skin guardada o la default."""
        settings = self._load_settings()
        return settings.get('selected_skin', 'img.png')
    
    def _load_settings(self) -> dict:
        """Carga settings.json."""
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[WARN] Error cargando settings: {e}")
        return {}
    
    def _save_settings(self, settings: dict):
        """Guarda settings.json."""
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"[ERROR] Error guardando settings: {e}")


def open_file_dialog() -> str:
    """
    Abre un diálogo para seleccionar una imagen.
    Retorna la ruta del archivo seleccionado o None.
    """
    try:
        from tkinter import Tk, filedialog
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)  # Mantener diálogo al frente
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen para skin",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.webp *.bmp *.gif"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )
        root.destroy()
        return file_path if file_path else None
    except Exception as e:
        print(f"[ERROR] No se pudo abrir diálogo de archivos: {e}")
        return None
