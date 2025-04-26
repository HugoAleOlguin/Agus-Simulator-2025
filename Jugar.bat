@echo off

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ==========================================================
    echo [ERROR] Python no está instalado o no está en el PATH.
    echo Por favor, instala Python y asegúrate de agregarlo al PATH.
    echo ==========================================================
    pause
    exit /b
)

REM Verificar si pip está instalado
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ==========================================================
    echo [INFO] Pip no está instalado. Instalando pip...
    echo ==========================================================
    python -m ensurepip --default-pip
    if %errorlevel% neq 0 (
        echo ==========================================================
        echo [ERROR] Error al instalar pip. Verifica tu instalación de Python.
        echo ==========================================================
        pause
        exit /b
    )
    echo ==========================================================
    echo [INFO] Pip se instaló correctamente.
    echo ==========================================================
)

REM Verificar si pygame está instalado
python -m pip show pygame >nul 2>&1
if %errorlevel% neq 0 (
    echo ==========================================================
    echo [INFO] Pygame no está instalado. Instalando pygame...
    echo ==========================================================
    python -m pip install pygame
    if %errorlevel% neq 0 (
        echo ==========================================================
        echo [INFO] Se instalaron las dependencias necesarias.
        echo Por favor, cierra esta ventana y ejecuta nuevamente "Jugar.bat".
        echo ==========================================================
        pause
        exit /b
    )
    echo ==========================================================
    echo [INFO] Pygame se instaló correctamente.
    echo ==========================================================
)

REM Ejecutar el juego
echo ==========================================================
echo [INFO] Iniciando el juego...
echo ==========================================================
python src\game.py
if %errorlevel% neq 0 (
    echo ==========================================================
    echo [ERROR] Hubo un error al ejecutar el juego.
    echo ==========================================================
    pause
    exit /b
)

REM Cerrar automáticamente al finalizar el juego
exit