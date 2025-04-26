# Agus Simulator - Detalles del Juego

---

## Características

### Jugabilidad
- **Movimiento del Jugador**: Controlado con las teclas `W`, `A`, `S`, `D`.
- **Objetivo**: Atrapar emojis para crecer en tamaño o evitar no atrapar emojis durante 30 segundos.

### Visuales
- **Fondo Dinámico**: El juego mantiene un fondo gris consistente (`(160, 160, 160)`).
- **Escalado de Emojis**: Los emojis aumentan ligeramente de tamaño mientras caen.
- **HUD**: Muestra el temporizador, el contador de emojis, la velocidad de caída y una barra de progreso para el final pacífico.

### Audio
- **Música de Fondo**: Se reproduce continuamente durante el juego.
- **Sonido de Estrés**: Se reproduce cada 10 segundos para aumentar la intensidad.
- **Sonido de Victoria**: Se reproduce durante el final de victoria.

### Menú
- **Tips Rotativos**: Muestra consejos de juego cada 3 segundos.
- **Opciones**: Iniciar el juego o salir.

---

## Estructura de Archivos

### Archivos Batch
- **`Jugar.bat`**: Verifica que Python, pip y `pygame` estén instalados antes de iniciar el juego.
- **`Desinstalar.bat`**: Desinstala `pygame` y limpia las dependencias.

### Módulos de Python
1. **`game.py`**:
   - Bucle principal del juego.
   - Maneja el movimiento del jugador, la generación de emojis y la lógica del juego.
   - Gestiona los finales y los efectos de sonido.

2. **`menu.py`**:
   - Muestra el menú principal con tips rotativos.
   - Maneja la entrada del usuario para iniciar o salir del juego.

3. **`player.py`**:
   - Define la clase `Player`.
   - Maneja el movimiento, el crecimiento en tamaño y el renderizado.

4. **`emoji.py`**:
   - Define la clase `Emoji`.
   - Maneja el comportamiento de caída, la detección de colisiones y el renderizado.

5. **`endings.py`**:
   - Gestiona los finales de victoria y pacífico.
   - Muestra mensajes de felicitación con animaciones.

6. **`hud.py`**:
   - Dibuja el temporizador, el contador de emojis, la velocidad de caída y la barra de progreso pacífica.

7. **`utils.py`**:
   - Funciones utilitarias para cargar imágenes, emojis y frames de GIF.

8. **`config.py`**:
   - Almacena constantes globales como `FPS`.

---

## Recursos
- **Imágenes**:
  - `assets/img.png`: Imagen del jugador.
  - `assets/emojis/emoji.png`: Imagen del emoji.
  - `assets/congratulations`: Carpeta con frames del GIF para la animación de victoria.
- **Audio**:
  - `assets/background.mp3`: Música de fondo.
  - `assets/stress.mp3`: Efecto de sonido de estrés.
  - `assets/victory.mp3`: Efecto de sonido de victoria.

---

## Instalación y Ejecución

### Requisitos Previos
- Python instalado y agregado al PATH del sistema.
- Biblioteca `pygame` instalada.

### Ejecutar el Juego
1. Haz doble clic en `Jugar.bat` para iniciar el juego.
2. Sigue las instrucciones en pantalla para jugar.

### Desinstalación
1. Ejecuta `Desinstalar.bat` para eliminar `pygame` y limpiar las dependencias.

---

## Mejoras Futuras
- Agregar más tipos de emojis con comportamientos únicos.
- Introducir potenciadores u obstáculos.
- Implementar un sistema de puntuación.
- Agregar soporte multijugador.
