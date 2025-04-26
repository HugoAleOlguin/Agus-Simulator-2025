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

REM Desinstalar pygame
python -m pip show pygame >nul 2>&1
if %errorlevel% equ 0 (
    echo Desinstalando pygame...
    python -m pip uninstall -y pygame
)

REM Confirmar desinstalación
echo Todas las dependencias específicas del juego han sido desinstaladas.
pause