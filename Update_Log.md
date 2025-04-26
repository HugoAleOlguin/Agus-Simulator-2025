# Update Log - Agus Simulator Version 2.0

## **Novedades y Mejoras**
1. **Menú inicial mejorado**:
   - Se añadieron tips rotativos que cambian cada 3 segundos.
   - Ejemplos de tips:
     - "Usa W, A, S, D para moverte."
     - "¿De qué país son esas banderas?"
     - "Basado en hechos reales."
     - "No durarás ni 20 segundos jugando este juego."

2. **Efectos de sonido**:
   - Se añadió música de fondo (`background.mp3`) que se reproduce continuamente durante el juego.
   - Se añadió un sonido de estrés (`stress.mp3`) que se reproduce cada 10 segundos para aumentar la intensidad.
   - Se añadió un sonido de victoria (`victory.mp3`) que se reproduce al alcanzar el final de victoria.

3. **HUD dinámico**:
   - Temporizador en tiempo real que muestra el tiempo transcurrido.
   - Contador de emojis atrapados.
   - Velocidad de caída de los emojis.
   - Barra de progreso para el final pacífico.

4. **Finales mejorados**:
   - **Final de victoria**: Se muestra un GIF animado con un mensaje de felicitación y el tiempo final.
   - **Final pacífico**: Se muestra un mensaje indicando que el jugador evitó atrapar emojis durante 30 segundos.

5. **Fondo restaurado**:
   - El fondo del juego ahora es gris (`(160, 160, 160)`) para una experiencia visual consistente.

6. **Mecánicas de juego mejoradas**:
   - Los emojis ahora crecen ligeramente mientras caen.
   - El jugador crece al atrapar emojis, con un límite máximo basado en el tamaño de la ventana.

7. **Persistencia del programa**:
   - El programa ya no se cierra automáticamente al terminar una partida. Ahora regresa al menú principal para jugar nuevamente.

---

## **Cambios desde la versión anterior**
- En la versión anterior, solo existía un menú simple con el mensaje "Presiona ENTER para jugar".
- No había efectos de sonido ni música de fondo.
- No existía un HUD para mostrar información en tiempo real.
- El jugador solo podía esquivar emojis, y no había mecánicas de crecimiento.
- El programa se cerraba automáticamente al terminar una partida.

---

## **Notas**
- Asegúrate de tener todos los archivos de audio e imágenes en sus respectivas carpetas.
- Esta versión requiere `pygame` instalado para ejecutarse correctamente.
- ¡Gracias por jugar Agus Simulator!
