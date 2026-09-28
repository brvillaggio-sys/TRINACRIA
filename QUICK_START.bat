@echo off
REM =============================================================================
REM Cyber Toolkit - Quick Start Script (Windows)
REM =============================================================================
REM Questo script automatizza l'installazione e la configurazione iniziale.
REM Utilizzo: QUICK_START.bat
REM =============================================================================

echo ==========================================
echo   Cyber Toolkit - Installazione Rapida
echo ==========================================
echo.

REM 1. Verifica Python
echo [1/5] Verifica Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Errore: Python non trovato. Installa Python 3.8+ prima di continuare.
    pause
    exit /b 1
)
echo     ✓ Python rilevato
echo.

REM 2. Crea ambiente virtuale
echo [2/5] Creazione ambiente virtuale...
if exist "venv" (
    echo     i Ambiente 'venv' gia' esistente, skip...
) else (
    python -m venv venv
    echo     ✓ Ambiente virtuale creato: venv\
)
echo.

REM 3. Attiva ambiente virtuale
echo [3/5] Attivazione ambiente virtuale...
call venv\Scripts\activate.bat
echo     ✓ Ambiente attivato
echo.

REM 4. Installa dipendenze
echo [4/5] Installazione dipendenze...
if exist "requirements.txt" (
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo     ✓ Dipendenze installate
) else (
    echo [!] Errore: requirements.txt non trovato.
    pause
    exit /b 1
)
echo.

REM 5. Inizializza Git (opzionale)
echo [5/5] Inizializzazione Git (opzionale)...
if exist ".git" (
    echo     i Repository Git gia' esistente, skip...
) else (
    git init
    git add .
    git commit -m "Initial commit: Cyber Toolkit"
    echo     ✓ Repository Git inizializzato
)
echo.

REM Completamento
echo ==========================================
echo   ✅ Installazione completata!
echo ==========================================
echo.
echo Prossimi passi:
echo   1. Attiva l'ambiente virtuale: venv\Scripts\activate
echo   2. Prova uno script: python port_scanner.py --target 127.0.0.1 --start 1 --end 1024
echo   3. Per push su GitHub:
echo      git remote add origin https://github.com/tuo-username/cyber-toolkit.git
echo      git push -u origin main
echo.
echo Documentazione: vedi README.md
echo ==========================================
echo.
pause