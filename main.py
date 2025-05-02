import os
import sys

# Asegurar que src esté en el path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

if __name__ == "__main__":
    try:
        from src.core.game import main
        print("Directorio de trabajo:", project_root)
        main()
    except ImportError as e:
        print("Error de importación:", e)
        print("Asegúrate de que todos los archivos necesarios estén en su lugar")
        input("Presiona Enter para salir...")
    except Exception as e:
        print("Error:", e)
        input("Presiona Enter para salir...")
