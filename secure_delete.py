#!/usr/bin/env python3
"""
Secure Delete (Cancellazione Sicura)
====================================
Elimina file sovrascrivendo dati multipli pass (DoD 5220.22-M style).

Esempio:
  python secure_delete.py --file dati.txt --passes 3
"""

import argparse
import os
import secrets
from pathlib import Path


def secure_delete(file_path: Path, passes: int = 3):
    size = file_path.stat().st_size
    with open(file_path, "r+b") as f:
        for i in range(passes):
            # Pass 1: zeri, Pass 2: ones, Pass 3+: random
            if i == 0:
                pattern = b"\x00" * size
            elif i == 1:
                pattern = b"\xFF" * size
            else:
                pattern = secrets.token_bytes(size)

            f.seek(0)
            f.write(pattern)
            f.flush()
            os.fsync(f.fileno())

    file_path.unlink()
    print(f"[*] File eliminato in modo sicuro: {file_path.name} ({passes} pass)")


def main():
    parser = argparse.ArgumentParser(description="Secure Delete (Cancellazione Sicura)")
    parser.add_argument("--file", required=True, help="File da eliminare in modo sicuro")
    parser.add_argument("--passes", type=int, default=3, help="Numero di pass di sovrascrittura")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"[!] File non trovato: {file_path}")
        return

    print(f"[!] ATTENZIONE: Questa operazione è IRREVERSIBILE")
    confirm = input(f"    Eliminare definitivamente {file_path.name}? (yes/no): ")
    if confirm.lower() != "yes":
        print("[*] Operazione annullata")
        return

    secure_delete(file_path, args.passes)


if __name__ == "__main__":
    main()