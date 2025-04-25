@echo off

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no está instalado o no está en el PATH. Por favor, instala Python y asegúrate de agregarlo al PATH.
    pause
    exit /b
)

REM Verificar si pip está instalado
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip no está instalado. Por favor, instala pip.
    pause
    exit /b
)

REM Verificar si pygame está instalado
python -m pip show pygame >nul 2>&1
if %errorlevel% neq 0 (
    echo Pygame no está instalado. Instalando pygame...
    python -m pip install pygame
    if %errorlevel% neq 0 (
        echo Error al instalar pygame. Verifica tu instalación de Python.
        pause
        exit /b
    )
)

REM Ejecutar el juego
echo Iniciando el juego...
python src\game.py
if %errorlevel% neq 0 (
    echo Hubo un error al ejecutar el juego.
    pause
    exit /b
)

pause