# 📋 Changelog - Agus Simulator

Todos los cambios notables de este proyecto están documentados aquí.

---

## [3.0] - 2025

### 🎮 Nuevos Modos de Juego

#### Modo Infinito
- Sistema de 3 vidas con corazones visuales
- Fondo espacial dinámico con estrellas en múltiples capas
- Planetas y objetos espaciales que aparecen aleatoriamente (Baren, Black hole, Ice, Lava, Terran)
- Sistema de partículas para efectos visuales:
  - Explosiones rojas al perder vida
  - Partículas rosas al recoger corazón
  - Explosión final en game over
- Música espacial única ("Sci-Fi 6 Loop")
- HUD mejorado con vidas, tiempo actual/récord e indicador de velocidad con colores
- Dificultad progresiva: velocidad aumenta, mayor spawn de emojis, probabilidad reducida de corazones (0.1%)
- Sistema de récords persistente con opción para resetear (tecla DEL)

#### Modo Hetero Mejorado
- Nuevo fondo con degradado y efectos visuales
- Sistema de cancelación instantánea
- HUD mejorado con tiempo y velocidad
- Dificultad progresiva ajustada
- Final personalizado con mensaje de cancelación

#### Modo Clásico Refinado
- Diseño simplificado y optimizado
- Finales mejorados: victoria más satisfactoria, esquivar más humorístico, secreto mejorado

### 🔧 Mejoras Técnicas
- Sistema de guardado con récords persistente en JSON
- Sistema de partículas personalizado
- Efectos de daño con flash rojo y transiciones suaves
- Sistema de música por modo con transiciones suaves
- Mejor gestión de memoria y código más modular

### 🐛 Correcciones
- Bug de música no reiniciando
- Colisiones imprecisas
- Detección de récords
- Spawn de objetos espaciales
- Reinicio de modo infinito

---

## [2.5 Beta] - 2025

### ✨ Novedades

#### Menú Inicial
- Tips rotativos que cambian cada 3 segundos
- Opciones claras para jugar o salir

#### Selección de Modos
- Menú para seleccionar modo de juego: Clásico, Hetero (próximamente), Infinito (próximamente)

#### Efectos de Sonido
- Música de fondo (`background.mp3`)
- Sonido de estrés cada 10 segundos (`stress.mp3`)
- Sonido de victoria (`victory.mp3`)
- Canción especial para esquivar (`budagus.mp3`)
- Canción secreta (`secret.mp3`)

#### Finales
- **Victoria**: GIF animado con mensaje de felicitación
- **Esquivar**: Imagen `budagus.png` a pantalla completa con mensajes y canción especial
- **Secreto**: Mensaje especial con canción secreta

#### Mecánicas
- Emojis crecen mientras caen
- Jugador crece al atrapar emojis (con límite máximo)
- Velocidad de caída aumenta con el tiempo

### 🔧 Mejoras
- Código reorganizado y simplificado
- Funciones reutilizables: `render_multiline_text`, `render_text_with_outline`
- El juego regresa al menú principal en vez de cerrarse

---

## [2.0] - 2025

### ✨ Primera versión completa

#### Menú
- Tips rotativos cada 3 segundos
- Opciones de Jugar y Salir

#### Efectos de Sonido
- Música de fondo continua
- Sonido de estrés cada 10 segundos
- Sonido de victoria

#### HUD
- Temporizador en tiempo real
- Contador de emojis atrapados
- Velocidad de caída
- Barra de progreso para final pacífico

#### Finales
- **Victoria**: GIF animado con felicitación y tiempo final
- **Pacífico**: Mensaje por evitar emojis durante 30 segundos

#### Mecánicas
- Emojis crecen mientras caen
- Jugador crece al atrapar emojis
- Fondo gris consistente

### 🆕 Cambios desde v1.0
- Antes: Solo mensaje "Presiona ENTER para jugar"
- Antes: Sin efectos de sonido ni música
- Antes: Sin HUD
- Antes: Sin mecánicas de crecimiento
- Antes: Se cerraba automáticamente al terminar

---

## [1.0] - 2025 (Versión inicial)

- Menú simple con "Presiona ENTER para jugar"
- Movimiento con W, A, S, D
- Emojis que caen
- Sin finales ni música
