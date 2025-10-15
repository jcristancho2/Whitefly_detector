@echo off
REM start.bat - Script de inicio para Windows
SETLOCAL EnableDelayedExpansion

title Sistema de Detección de Mosca Blanca

echo.
echo ========================================
echo  Sistema de Detección de Mosca Blanca
echo ========================================
echo.

:MENU
echo.
echo Que deseas hacer?
echo.
echo 1) Configuracion inicial completa
echo 2) Solo instalar dependencias
echo 3) Verificar sistema
echo 4) Entrenar modelo
echo 5) Iniciar servidor
echo 6) Salir
echo.

set /p option="Selecciona una opcion (1-6): "

if "%option%"=="1" goto FULL_SETUP
if "%option%"=="2" goto INSTALL_DEPS
if "%option%"=="3" goto CHECK_SYSTEM
if "%option%"=="4" goto TRAIN_MODEL
if "%option%"=="5" goto START_SERVER
if "%option%"=="6" goto EXIT
goto MENU

:FULL_SETUP
echo.
echo [*] Configuracion inicial...
call :CHECK_PYTHON
call :SETUP_VENV
call :INSTALL_DEPS
call :CREATE_DIRS
call :CHECK_MODEL
echo.
echo [OK] Configuracion completada
echo.
set /p start_now="Iniciar servidor ahora? (s/n): "
if /i "%start_now%"=="s" goto START_SERVER
goto MENU

:CHECK_PYTHON
echo.
echo [*] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python encontrado
exit /b 0

:SETUP_VENV
echo.
echo [*] Configurando entorno virtual...
if not exist "venv" (
    python -m venv venv
    echo [OK] Entorno virtual creado
) else (
    echo [!] Entorno virtual ya existe
)
call venv\Scripts\activate.bat
exit /b 0

:INSTALL_DEPS
echo.
echo [*] Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [OK] Dependencias instaladas
exit /b 0

:CREATE_DIRS
echo.
echo [*] Creando directorios...
if not exist "models" mkdir models
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads

REM Crear estructura de dataset
for %%s in (train val test) do (
    if not exist "dataset\%%s" mkdir dataset\%%s
    if not exist "dataset\%%s\sin_plaga" mkdir dataset\%%s\sin_plaga
    if not exist "dataset\%%s\infestacion_leve" mkdir dataset\%%s\infestacion_leve
    if not exist "dataset\%%s\infestacion_severa" mkdir dataset\%%s\infestacion_severa
)
echo [OK] Directorios creados
exit /b 0

:CHECK_MODEL
echo.
echo [*] Verificando modelo...
if exist "models\whitefly_detector.h5" (
    echo [OK] Modelo encontrado
) else (
    echo [!] Modelo no encontrado
    echo.
    echo Necesitas entrenar el modelo primero con:
    echo python train_model.py
    echo.
    set /p train_now="Entrenar ahora? (s/n): "
    if /i "!train_now!"=="s" (
        python train_model.py
    )
)
exit /b 0

:CHECK_SYSTEM
echo.
echo [*] Verificando sistema...
python utils.py check
pause
goto MENU

:TRAIN_MODEL
echo.
echo [*] Entrenando modelo...
python train_model.py
pause
goto MENU

:START_SERVER
echo.
echo [*] Iniciando servidor...
echo.
echo    API disponible en: http://localhost:8000
echo    Documentacion: http://localhost:8000/docs
echo.
echo    Presiona Ctrl+C para detener el servidor
echo.
uvicorn main:app --reload --host 0.0.0.0 --port 8000
goto MENU

:EXIT
echo.
echo Hasta luego!
exit /b 0