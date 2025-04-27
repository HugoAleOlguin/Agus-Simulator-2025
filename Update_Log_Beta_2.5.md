# Update Log - Agus Simulator Beta 2.5

## **Novedades y Mejoras**
1. **Menú inicial mejorado**:
   - Se añadieron tips rotativos que cambian cada 3 segundos.
   - Ejemplos de tips:
     - "Usa W, A, S, D para moverte."
     - "¿De qué país son esas banderas?"
     - "Basado en hechos reales."
     - "No durarás ni 20 segundos jugando este juego."

2. **Selección de modos**:
   - Se añadió un menú para seleccionar el modo de juego:
     - **Clásico**: ¡Atrapa o esquiva banderas!
     - **Modo Hetero**: Próximamente.
     - **Modo Infinito**: Próximamente.
   - Los modos no implementados muestran un mensaje de "¡Próximamente!" y regresan al menú.

3. **Efectos de sonido**:
   - Se añadió música de fondo (`background.mp3`) que se reproduce continuamente durante el juego.
   - Se añadió un sonido de estrés (`stress.mp3`) que se reproduce cada 10 segundos para aumentar la intensidad.
   - Se añadió un sonido de victoria (`victory.mp3`) que se reproduce al alcanzar el final de victoria.
   - Se añadió una canción especial (`budagus.mp3`) para el final de esquivar.
   - Se añadió una canción secreta (`secret.mp3`) para el final secreto.

4. **HUD dinámico**:
   - Temporizador en tiempo real que muestra el tiempo transcurrido.
   - Contador de emojis atrapados.
   - Velocidad de caída de los emojis.
   - Barra de progreso para el final pacífico.

5. **Finales mejorados**:
   - **Final de victoria**: Se muestra un GIF animado con un mensaje de felicitación y el tiempo final.
   - **Final de esquivar**: Se muestra una imagen (`budagus.png`) redimensionada para cubrir toda la pantalla, con mensajes en la parte inferior y una canción especial.
   - **Final secreto**: Se muestra un mensaje especial con una canción secreta.

6. **Mecánicas de juego mejoradas**:
   - Los emojis ahora crecen ligeramente mientras caen.
   - El jugador crece al atrapar emojis, con un límite máximo basado en el tamaño de la ventana.
   - La velocidad de caída de los emojis aumenta con el tiempo.

7. **Optimización del código**:
   - Se reorganizó y simplificó el código en varios archivos para mejorar la legibilidad y el mantenimiento.
   - Se añadieron funciones reutilizables, como `render_multiline_text` y `render_text_with_outline`.

8. **Persistencia del programa**:
   - El programa ya no se cierra automáticamente al terminar una partida. Ahora regresa al menú principal para jugar nuevamente.

---

## **Cambios desde la versión anterior**
- **Menú inicial**:
  - Antes solo mostraba "Presiona ENTER para jugar". Ahora incluye tips rotativos y opciones claras para jugar o salir.
- **Finales**:
  - Antes no había finales específicos. Ahora hay tres finales distintos con imágenes, GIFs y canciones.
- **Sonidos**:
  - Antes no había música ni efectos de sonido. Ahora hay música de fondo, sonidos de estrés y canciones para los finales.
- **HUD**:
  - Antes no había indicadores en pantalla. Ahora hay un temporizador, contador de emojis, velocidad de caída y barra de progreso.
- **Selección de modos**:
  - Antes no había modos de juego. Ahora hay un menú para seleccionar modos, aunque algunos están marcados como "próximamente".

---

## **Notas**
- Asegúrate de tener todos los archivos de audio e imágenes en sus respectivas carpetas:
  - `assets/music/`
  - `assets/endings/`
  - `assets/emojis/`
- Esta versión requiere `pygame` instalado para ejecutarse correctamente.
- ¡Gracias por jugar Agus Simulator Beta 2.5!
