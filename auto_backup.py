#!/usr/bin/env python3
"""
Auto Backup
===========
Backup automatizzato di directory con compressione ZIP, hash SHA-256 e rotazione.

Esempio:
  python auto_backup.py --source /home/user/dati --dest /backup --keep 5
"""

import argparse
import hashlib
import os
import shutil
import time
from datetime import datetime
from pathlib import Path


def compute_sha256(path: str) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            hasher.update(block)
    return hasher.hexdigest()


def rotate_backups(dest_dir: Path, keep: int):
    backups = sorted(dest_dir.glob("backup_*.zip"))
    while len(backups) > keep:
        oldest = backups.pop(0)
        oldest.unlink()
        print(f"[*] Rimosso backup vecchio: {oldest.name}")


def main():
    parser = argparse.ArgumentParser(description="Auto Backup con compressione e rotazione")
    parser.add_argument("--source", required=True, help="Directory o file da backuppare")
    parser.add_argument("--dest", required=True, help="Directory di destinazione")
    parser.add_argument("--keep", type=int, default=5, help="Numero di backup da mantenere")
    args = parser.parse_args()

    source = Path(args.source)
    dest = Path(args.dest)
    dest.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        print(f"[!] Sorgente non trovata: {source}")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.zip"
    backup_path = dest / backup_name

    print(f"[*] Creazione backup: {source} -> {backup_path}")
    t0 = time.time()

    if source.is_dir():
        shutil.make_archive(str(backup_path.with_suffix("")), "zip", source.parent, source.name)
    else:
        shutil.make_archive(str(backup_path.with_suffix("")), "zip", source.parent, source.name)

    # Calcola hash
    sha256 = compute_sha256(str(backup_path))
    hash_file = dest / f"{backup_name}.sha256"
    with open(hash_file, "w") as f:
        f.write(f"{sha256}  {backup_name}\n")

    elapsed = time.time() - t0
    print(f"[*] Backup completato in {elapsed:.2f}s")
    print(f"    File: {backup_path.name}")
    print(f"    SHA-256: {sha256}")

    # Rotazione
    rotate_backups(dest, args.keep)


if __name__ == "__main__":
    main()