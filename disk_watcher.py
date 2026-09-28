#!/usr/bin/env python3
"""
Disk Watcher
============
Monitora utilizzo disco e invia alert quando supera una soglia configurabile.

Esempio:
  python disk_watcher.py --threshold 85 --interval 300
"""

import argparse
import shutil
import time
from datetime import datetime
from pathlib import Path


def get_disk_usage(path: str = "/") -> dict:
    total, used, free = shutil.disk_usage(path)
    percent = (used / total) * 100
    return {
        "path": path,
        "total_gb": total / (1024**3),
        "used_gb": used / (1024**3),
        "free_gb": free / (1024**3),
        "percent": percent,
    }


def main():
    parser = argparse.ArgumentParser(description="Disk Watcher")
    parser.add_argument("--path", default="/", help="Mountpoint da monitorare")
    parser.add_argument("--threshold", type=float, default=85.0, help="Soglia percentuale alert")
    parser.add_argument("--interval", type=int, default=300, help="Intervallo controllo (secondi)")
    parser.add_argument("--once", action="store_true", help="Esegui una volta sola")
    args = parser.parse_args()

    log_file = Path("disk_watcher.log")
    print(f"[*] Monitoraggio disco: {args.path} (soglia: {args.threshold}%)")

    alerted = False
    try:
        while True:
            usage = get_disk_usage(args.path)
            timestamp = datetime.now().isoformat()
            entry = (
                f"[{timestamp}] {usage['path']} | "
                f"Usato: {usage['used_gb']:.2f} GB / {usage['total_gb']:.2f} GB "
                f"({usage['percent']:.1f}%) | Libero: {usage['free_gb']:.2f} GB\n"
            )
            print(entry.strip())
            with open(log_file, "a") as f:
                f.write(entry)

            if usage["percent"] >= args.threshold:
                if not alerted:
                    print(f"    [!] ALERT: Utilizzo disco >= {args.threshold}%!")
                    alerted = True
            else:
                alerted = False

            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[*] Monitoraggio interrotto.")


if __name__ == "__main__":
    main()