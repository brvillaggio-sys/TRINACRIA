#!/usr/bin/env python3
"""
Log Rotator
===========
Rotazione e archiviazione log con compressione gzip e rimozione vecchi file.

Esempio:
  python log_rotator.py --logdir /var/log/myapp --max-size 10 --keep 5
"""

import argparse
import gzip
import os
import shutil
import time
from datetime import datetime
from pathlib import Path


def rotate_log(log_path: Path, archive_dir: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"{log_path.stem}_{timestamp}.gz"
    archive_path = archive_dir / archive_name

    with open(log_path, "rb") as f_in:
        with gzip.open(archive_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Tronca il log originale
    with open(log_path, "w") as f:
        pass

    return archive_path


def cleanup_old(archive_dir: Path, keep: int):
    archives = sorted(archive_dir.glob("*.gz"))
    while len(archives) > keep:
        oldest = archives.pop(0)
        oldest.unlink()
        print(f"[*] Rimosso archivio vecchio: {oldest.name}")


def main():
    parser = argparse.ArgumentParser(description="Log Rotator")
    parser.add_argument("--logdir", required=True, help="Directory con file di log")
    parser.add_argument("--max-size", type=int, default=10, help="Max dimensione MB prima di rotazione")
    parser.add_argument("--keep", type=int, default=5, help="Numero di archivi da mantenere")
    args = parser.parse_args()

    logdir = Path(args.logdir)
    archive_dir = logdir / "archives"
    archive_dir.mkdir(exist_ok=True)

    max_bytes = args.max_size * 1024 * 1024
    print(f"[*] Log Rotator attivo su {logdir} (max: {args.max_size} MB, keep: {args.keep})")

    for log_file in logdir.glob("*.log"):
        size = log_file.stat().st_size
        if size >= max_bytes:
            print(f"[*] Rotazione: {log_file.name} ({size / 1024 / 1024:.2f} MB)")
            archive_path = rotate_log(log_file, archive_dir)
            print(f"    Archiviato: {archive_path.name}")
            cleanup_old(archive_dir, args.keep)
        else:
            print(f"    Skip: {log_file.name} ({size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()