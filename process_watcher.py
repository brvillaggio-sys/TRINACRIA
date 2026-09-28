#!/usr/bin/env python3
"""
Process Watcher
===============
Monitora processi critici e li riavvia automaticamente se terminati.

Esempio:
  python process_watcher.py --processes nginx,postgres --interval 30
"""

import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path


def is_process_running(name: str) -> bool:
    try:
        result = subprocess.run(
            ["pgrep", "-x", name],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def start_process(name: str) -> bool:
    try:
        subprocess.Popen([name])
        return True
    except Exception as e:
        print(f"    [!] Errore avvio {name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Process Watcher")
    parser.add_argument("--processes", nargs="+", required=True, help="Nomi processi da monitorare")
    parser.add_argument("--interval", type=int, default=30, help="Intervallo controllo (secondi)")
    parser.add_argument("--once", action="store_true", help="Esegui una volta sola")
    args = parser.parse_args()

    log_file = Path("process_watcher.log")
    print(f"[*] Monitoraggio processi: {', '.join(args.processes)}")

    try:
        while True:
            timestamp = datetime.now().isoformat()
            for proc in args.processes:
                if not is_process_running(proc):
                    entry = f"[{timestamp}] {proc} -> DOWN (riavvio in corso)\n"
                    print(entry.strip())
                    with open(log_file, "a") as f:
                        f.write(entry)
                    if start_process(proc):
                        print(f"    [*] {proc} riavviato")
                    else:
                        print(f"    [!] {proc} riavvio fallito")
                else:
                    print(f"    [OK] {proc} -> RUNNING")

            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[*] Monitoraggio interrotto.")


if __name__ == "__main__":
    main()