"""
Sistema de logros del juego.
Gestiona la persistencia y desbloqueo de logros.
"""
import os
import json
import pygame

# Definición de logros
ACHIEVEMENTS = {
    "first_blood": {
        "id": "first_blood",
        "name": "Ay...",
        "description": "Atrapa tu primer banderita",
        "secret": False
    },
    "survivor_30": {
        "id": "survivor_30",
        "name": "No tan hetero",
        "description": "30 segundos sin ser cancelado",
        "secret": False
    },
    "giant": {
        "id": "giant",
        "name": "Me gustan asi...",
        "description": "Se el mas grande en el modo clasico",
        "secret": False
    },
    "pacifist": {
        "id": "pacifist",
        "name": "Pacifista",
        "description": "Esquiva emojis por 60 segundos",
        "secret": False
    },
    "infinite_master": {
        "id": "infinite_master",
        "name": "Maestro Infinito",
        "description": "Alcanza 60 segundos en modo Infinito",
        "secret": False
    },
    "jesus_encounter": {
        "id": "jesus_encounter",
        "name": "JESUS??!!",
        "description": "Jesus te toco (literalmente)",
        "secret": False
    },
    "secret_ending": {
        "id": "secret_ending",
        "name": "???",
        "description": "???",
        "secret": True,
        "unlocked_name": "NASHE",
        "unlocked_description": "200 segundos. Estas bien?"
    }
}


def get_appdata_dir():
    """Obtiene el directorio de AppData para el juego."""
    if os.name == 'nt':  # Windows
        appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
        save_dir = os.path.join(appdata, 'AgusSimulator')
    else:  # Linux/Mac
        save_dir = os.path.expanduser('~/.agussimulator')
    return save_dir


class AchievementManager:
    def __init__(self):
        self.save_dir = get_appdata_dir()
        self.save_path = os.path.join(self.save_dir, 'achievements.json')
        self._ensure_save_directory()
        self.unlocked = self._load_achievements()
        self.pending_notifications = []  # Cola de notificaciones pendientes
        
    def _ensure_save_directory(self):
        if not os.path.exists(self.save_dir):
            try:
                os.makedirs(self.save_dir)
            except Exception as e:
                print(f"Error creando directorio: {e}")
    
    def _load_achievements(self):
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error cargando logros: {e}")
        return {}
    
    def _save_achievements(self):
        try:
            with open(self.save_path, 'w') as f:
                json.dump(self.unlocked, f, indent=2)
        except Exception as e:
            print(f"Error guardando logros: {e}")
    
    def unlock(self, achievement_id):
        """Desbloquea un logro y lo agrega a la cola de notificaciones."""
        if achievement_id not in self.unlocked:
            self.unlocked[achievement_id] = True
            self._save_achievements()
            # Agregar a cola de notificaciones
            if achievement_id in ACHIEVEMENTS:
                self.pending_notifications.append(achievement_id)
            return True
        return False
    
    def is_unlocked(self, achievement_id):
        return self.unlocked.get(achievement_id, False)
    
    def get_pending_notification(self):
        """Obtiene la siguiente notificación pendiente."""
        if self.pending_notifications:
            return self.pending_notifications.pop(0)
        return None
    
    def get_all_achievements(self):
        """Retorna todos los logros con su estado."""
        result = []
        for ach_id, ach_data in ACHIEVEMENTS.items():
            is_unlocked = self.is_unlocked(ach_id)
            result.append({
                **ach_data,
                "unlocked": is_unlocked
            })
        return result


class AchievementNotification:
    """Clase para mostrar notificaciones de logros in-game."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_notification = None
        self.notification_start_time = 0
        self.notification_duration = 2.5  # segundos
        self.slide_in_duration = 0.3
        self.slide_out_duration = 0.3
        
    def show(self, achievement_id):
        """Muestra una notificación para un logro."""
        import time
        if achievement_id in ACHIEVEMENTS:
            self.current_notification = ACHIEVEMENTS[achievement_id]
            self.notification_start_time = time.time()
    
    def update_and_draw(self, screen, current_time):
        """Actualiza y dibuja la notificación actual."""
        if self.current_notification is None:
            return
        
        elapsed = current_time - self.notification_start_time
        total_duration = self.notification_duration + self.slide_in_duration + self.slide_out_duration
        
        if elapsed > total_duration:
            self.current_notification = None
            return
        
        # Calcular posición (slide in/out desde arriba)
        if elapsed < self.slide_in_duration:
            progress = elapsed / self.slide_in_duration
            progress = 1 - (1 - progress) ** 2
            y_offset = -60 + (60 * progress)
        elif elapsed > self.notification_duration + self.slide_in_duration:
            progress = (elapsed - self.notification_duration - self.slide_in_duration) / self.slide_out_duration
            y_offset = 0 - (60 * progress)
        else:
            y_offset = 0
        
        # Panel compacto
        panel_width = 260
        panel_height = 50
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = 10 + int(y_offset)
        
        # Fondo
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (25, 25, 30, 240), (0, 0, panel_width, panel_height), border_radius=8)
        pygame.draw.rect(panel_surface, (200, 170, 50), (0, 0, panel_width, panel_height), width=2, border_radius=8)
        
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Nombre del logro
        font_name = pygame.font.Font(None, 26)
        ach = self.current_notification
        
        if ach.get('secret') and 'unlocked_name' in ach:
            name = ach['unlocked_name']
        else:
            name = ach['name']
        
        # Texto centrado
        name_text = font_name.render(f"Logro: {name}", True, (255, 220, 100))
        name_rect = name_text.get_rect(center=(panel_x + panel_width // 2, panel_y + panel_height // 2))
        screen.blit(name_text, name_rect)


# Instancia global
_achievement_manager = None

def get_achievement_manager():
    global _achievement_manager
    if _achievement_manager is None:
        _achievement_manager = AchievementManager()
    return _achievement_manager
