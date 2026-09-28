#!/bin/bash
# =============================================================================
# Cyber Toolkit - Quick Start Script
# =============================================================================
# Questo script automatizza l'installazione e la configurazione iniziale.
# Utilizzo: bash QUICK_START.sh
# =============================================================================

set -e  # Esce immediatamente in caso di errore

echo "=========================================="
echo "  Cyber Toolkit - Installazione Rapida"
echo "=========================================="
echo ""

# 1. Verifica Python
echo "[1/5] Verifica Python..."
if ! command -v python3 &> /dev/null; then
    echo "[!] Errore: Python3 non trovato. Installa Python 3.8+ prima di continuare."
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "    ✓ $PYTHON_VERSION rilevato"
echo ""

# 2. Crea ambiente virtuale
echo "[2/5] Creazione ambiente virtuale..."
if [ -d "venv" ]; then
    echo "    ℹ Ambiente 'venv' già esistente, skip..."
else
    python3 -m venv venv
    echo "    ✓ Ambiente virtuale creato: venv/"
fi
echo ""

# 3. Attiva ambiente virtuale
echo "[3/5] Attivazione ambiente virtuale..."
source venv/bin/activate
echo "    ✓ Ambiente attivato"
echo ""

# 4. Installa dipendenze
echo "[4/5] Installazione dipendenze..."
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "    ✓ Dipendenze installate"
else
    echo "[!] Errore: requirements.txt non trovato."
    exit 1
fi
echo ""

# 5. Inizializza Git (opzionale)
echo "[5/5] Inizializzazione Git (opzionale)..."
if [ -d ".git" ]; then
    echo "    ℹ Repository Git già esistente, skip..."
else
    git init
    git add .
    git commit -m "Initial commit: Cyber Toolkit"
    echo "    ✓ Repository Git inizializzato"
fi
echo ""

# Completamento
echo "=========================================="
echo "  ✅ Installazione completata!"
echo "=========================================="
echo ""
echo "Prossimi passi:"
echo "  1. Attiva l'ambiente virtuale: source venv/bin/activate"
echo "  2. Prova uno script: python port_scanner.py --target 127.0.0.1 --start 1 --end 1024"
echo "  3. Per push su GitHub:"
echo "     git remote add origin https://github.com/tuo-username/cyber-toolkit.git"
echo "     git push -u origin main"
echo ""
echo "Documentazione: vedi README.md"
echo "=========================================="