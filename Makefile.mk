# =============================================================================
# Cyber Toolkit - Makefile
# =============================================================================
# Utilizzo:
#   make install    - Installa dipendenze e configura ambiente
#   make run        - Esegue uno script (es: make run SCRIPT=port_scanner)
#   make test       - Esegue test di base
#   make clean      - Pulisce file temporanei
#   make help       - Mostra questo aiuto
# =============================================================================

PYTHON := python3
PIP := pip3
VENV := venv
ACTIVATE := $(VENV)/bin/activate
REQUIREMENTS := requirements.txt

.PHONY: all install run test clean help

all: install

# Installa dipendenze e configura ambiente virtuale
install:
	@echo "==> Creazione ambiente virtuale..."
	@if [ ! -d "$(VENV)" ]; then $(PYTHON) -m venv $(VENV); fi
	@echo "==> Installazione dipendenze..."
	@. $(ACTIVATE) && $(PIP) install --upgrade pip
	@. $(ACTIVATE) && $(PIP) install -r $(REQUIREMENTS)
	@echo "==> ✅ Installazione completata!"
	@echo ""
	@echo "Per attivare l'ambiente: source $(ACTIVATE)"

# Esegue uno script (es: make run SCRIPT=port_scanner ARGS="--target 127.0.0.1")
run:
	@echo "==> Esecuzione script: $(SCRIPT).py $(ARGS)"
	@. $(ACTIVATE) && $(PYTHON) $(SCRIPT).py $(ARGS)

# Test di base (verifica che gli script principali siano eseguibili)
test:
	@echo "==> Esecuzione test di base..."
	@. $(ACTIVATE) && $(PYTHON) port_scanner.py --help
	@. $(ACTIVATE) && $(PYTHON) password_strength_checker.py --help
	@. $(ACTIVATE) && $(PYTHON) file_integrity_checker.py --help
	@echo "==> ✅ Tutti i test superati!"

# Pulisce file temporanei e cache
clean:
	@echo "==> Pulizia file temporanei..."
	@rm -rf __pycache__/
	@rm -rf *.pyc
	@rm -rf .pytest_cache/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf *.log
	@rm -rf *.enc
	@rm -rf *.dec
	@rm -rf backup_*.zip
	@echo "==> ✅ Pulizia completata!"

# Mostra aiuto
help:
	@echo "Cyber Toolkit - Makefile"
	@echo ""
	@echo "Comandi disponibili:"
	@echo "  make install   - Installa dipendenze e configura ambiente"
	@echo "  make run       - Esegue uno script (SCRIPT=nome ARGS=\"--arg1 --arg2\")"
	@echo "  make test      - Esegue test di base"
	@echo "  make clean     - Pulisce file temporanei"
	@echo "  make help      - Mostra questo aiuto"
	@echo ""
	@echo "Esempi:"
	@echo "  make run SCRIPT=port_scanner ARGS=\"--target 127.0.0.1 --start 1 --end 1024\""
	@echo "  make run SCRIPT=password_strength_checker ARGS=\"--password 'MiaPassword123!'\""