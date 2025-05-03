import os
import sys

def get_base_path():
    """Obtiene la ruta base correcta tanto para desarrollo como para la versión compilada"""
    if getattr(sys, 'frozen', False):
        # Ejecutable compilado
        return os.path.dirname(sys.executable)
    # Desarrollo
    return os.path.dirname(os.path.abspath(__file__))

def setup_environment():
    """Configura el entorno de ejecución"""
    base_path = get_base_path()
    src_path = os.path.join(base_path, 'src')
    
    # Asegurar que src esté en el path
    if src_path not in sys.path:
        sys.path.append(src_path)
    
    # Establecer el directorio de trabajo
    os.chdir(base_path)
    return base_path

if __name__ == "__main__":
    try:
        base_path = setup_environment()
        print("Directorio de trabajo:", base_path)
        
        from src.core.game import main
        main()
    except ImportError as e:
        print("Error de importación:", e)
        print("Asegúrate de que todos los archivos necesarios estén en su lugar")
        input("Presiona Enter para salir...")
    except Exception as e:
        print("Error:", e)
        print("Ruta actual:", os.getcwd())
        input("Presiona Enter para salir...")
