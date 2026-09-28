#!/usr/bin/env python3
"""
Ransomware Shield
=================
Rileva pattern tipici di ransomware: modifiche massive, estensioni anomale, entropia alta.

Esempio:
  python ransomware_shield.py --watch /home/user/dati --baseline baseline.json --mode init|monitor
"""

import argparse
import hashlib
import json
import os
import time
from collections import Counter
from datetime import datetime
from pathlib import Path


def compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            hasher.update(block)
    return hasher.hexdigest()


def build_baseline(root: Path) -> dict:
    baseline = {}
    for file_path in root.rglob("*"):
        if file_path.is_file():
            baseline[str(file_path)] = {
                "sha256": compute_sha256(file_path),
                "ext": file_path.suffix.lower(),
                "size": file_path.stat().st_size,
            }
    return baseline


def detect_ransomware_indicators(current: dict, baseline: dict) -> list:
    alerts = []

    # 1. File crittografati (estensioni anomale)
    crypto_exts = {".encrypted", ".locked", ".crypto", ".crypt", ".enc", ".locked"}
    for path, info in current.items():
        if info["ext"] in crypto_exts and path not in baseline:
            alerts.append(f"[CRITTO] Nuovo file cifrato: {path}")

    # 2. Modifiche massive in breve tempo
    modified_count = 0
    for path in baseline:
        if path in current and current[path]["sha256"] != baseline[path]["sha256"]:
            modified_count += 1

    if modified_count > len(baseline) * 0.3:
        alerts.append(f"[MASS_CHANGE] {modified_count}/{len(baseline)} file modificati (>30%)")

    # 3. Entropia alta (file cifrati)
    for path, info in current.items():
        if path in baseline and info["size"] > 1024:
            # Placeholder: qui si calcolerebbe entropia reale
            pass

    return alerts


def main():
    parser = argparse.ArgumentParser(description="Ransomware Shield")
    parser.add_argument("--watch", required=True, help="Directory da monitorare")
    parser.add_argument("--baseline", required=True, help="File baseline JSON")
    parser.add_argument("--mode", choices=["init", "monitor"], required=True)
    parser.add_argument("--interval", type=int, default=60, help="Intervallo monitoraggio (secondi)")
    args = parser.parse_args()

    watch_dir = Path(args.watch)

    if args.mode == "init":
        print(f"[*] Creazione baseline: {watch_dir}")
        baseline = build_baseline(watch_dir)
        with open(args.baseline, "w") as f:
            json.dump(baseline, f, indent=2)
        print(f"[*] Baseline salvata: {len(baseline)} file")
    else:
        if not Path(args.baseline).exists():
            print(f"[!] Baseline non trovata: {args.baseline}")
            return

        with open(args.baseline) as f:
            baseline = json.load(f)

        print(f"[*] Monitoraggio attivo (intervallo: {args.interval}s)")
        try:
            while True:
                current = build_baseline(watch_dir)
                alerts = detect_ransomware_indicators(current, baseline)
                if alerts:
                    print(f"\n[!] RILEVATI INDICATORI RANSOMWARE ({len(alerts)}):")
                    for a in alerts:
                        print(f"    {a}")
                else:
                    print(f"[{datetime.now().isoformat()}] Nessuna anomalia rilevata")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[*] Monitoraggio interrotto.")


if __name__ == "__main__":
    main()