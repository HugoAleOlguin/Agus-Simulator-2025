import os
import json

def get_appdata_dir():
    """Obtiene el directorio de AppData para el juego."""
    if os.name == 'nt':  # Windows
        appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
        save_dir = os.path.join(appdata, 'AgusSimulator')
    else:  # Linux/Mac
        save_dir = os.path.expanduser('~/.agussimulator')
    return save_dir

class SaveSystem:
    def __init__(self):
        self.save_dir = get_appdata_dir()
        self.save_path = os.path.join(self.save_dir, 'records.json')
        self._ensure_save_directory()
        self.records = self._load_records()

    def _ensure_save_directory(self):
        if not os.path.exists(self.save_dir):
            try:
                os.makedirs(self.save_dir)
            except Exception as e:
                print(f"Error creando directorio de guardado: {e}")
                self.save_dir = '.'  # Usar directorio actual como respaldo

    def _load_records(self):
        default_records = {
            "infinite_mode": 0,
            "classic_mode": 0,
            "hetero_mode": 0
        }
        
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, 'r') as f:
                    loaded_records = json.load(f)
                    # Asegurar que existan todas las claves necesarias
                    return {**default_records, **loaded_records}
        except Exception as e:
            print(f"Error cargando récords: {e}")
        
        return default_records

    def save_record(self, mode, time):
        current = self.records.get(mode, 0)
        if time > current:
            self.records[mode] = time
            try:
                with open(self.save_path, 'w') as f:
                    json.dump(self.records, f, indent=2)
                return True
            except Exception as e:
                print(f"Error guardando récord: {e}")
        return False

    def get_record(self, mode):
        return self.records.get(mode, 0)

    def reset_records(self):
        """Reiniciar todos los récords a 0"""
        self.records = {mode: 0 for mode in self.records}
        try:
            with open(self.save_path, 'w') as f:
                json.dump(self.records, f, indent=2)
            return True
        except Exception as e:
            print(f"Error reiniciando récords: {e}")
            return False
