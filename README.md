# 🎮 Agus Simulator 2025

Un juego arcade desarrollado en Python con Pygame donde debes atrapar (o esquivar) emojis para descubrir diferentes finales.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1+-green?logo=pygame)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Instalación

### Requisitos
- Python 3.x (agregado al PATH del sistema)
- Biblioteca `pygame`

### Ejecución Rápida
```bash
# Opción 1: Doble clic en Jugar.bat

# Opción 2: Manual
pip install pygame
python main.py
```

### Desinstalación
Ejecuta `Desinstalar.bat` para eliminar pygame y limpiar dependencias.

---

## 🎯 Cómo Jugar

| Tecla | Acción |
|-------|--------|
| `W` | Mover arriba |
| `A` | Mover izquierda |
| `S` | Mover abajo |
| `D` | Mover derecha |
| `ESC` | Salir/Volver |
| `DEL` | Resetear récord (en Game Over) |

---

## 🕹️ Modos de Juego

### 🏆 Modo Clásico
Atrapa emojis para crecer o esquívalos durante 30 segundos para el final pacífico.

### ♾️ Modo Infinito
- 3 vidas con corazones
- Fondo espacial dinámico con estrellas y planetas
- Dificultad progresiva
- Sistema de récords persistente

### 🌈 Modo Hetero
Modo especial con sistema de cancelación instantánea.

---

## 🏁 Finales

| Final | Cómo desbloquearlo |
|-------|-------------------|
| 🎉 **Victoria** | Atrapa suficientes emojis |
| 🕊️ **Pacífico** | Esquiva emojis por 30 segundos |
| 🔮 **Secreto** | ¿Podrás descubrirlo? |

---

## 📁 Estructura del Proyecto

```
Agus-Simulator-2025/
├── main.py              # Punto de entrada
├── src/
│   ├── core/            # Lógica principal del juego
│   ├── modes/           # Modos de juego (clásico, infinito, hetero)
│   ├── entities/        # Jugador, emojis, etc.
│   ├── ui/              # Menús y HUD
│   ├── effects/         # Partículas y efectos visuales
│   ├── utils/           # Funciones auxiliares
│   └── assets/          # Recursos (imágenes, música)
│       ├── emojis/
│       ├── endings/
│       ├── music/
│       └── space/
├── Jugar.bat            # Script para iniciar el juego
├── Desinstalar.bat      # Script de desinstalación
├── requirements.txt     # Dependencias
└── CHANGELOG.md         # Historial de versiones
```

---

## 📋 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para el historial completo de versiones.

**Última versión: 3.0** - Modo Infinito, efectos de partículas, sistema de récords y más.

---

## 🔮 Próximas Mejoras

- [ ] Modo multijugador local
- [ ] Nuevos tipos de emojis
- [ ] Sistema de logros
- [ ] Más efectos visuales

---

## 📝 Licencia

Este proyecto es de código abierto. ¡Diviértete jugando! 🎮

---

*¡Gracias por jugar Agus Simulator!*
