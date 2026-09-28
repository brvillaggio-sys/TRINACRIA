#!/usr/bin/env python3
"""
File Integrity Checker
======================
Crea una baseline SHA-256 di una cartella e confronta lo stato attuale
per rilevare file modificati, eliminati o aggiunti.

Esempi:
  python file_integrity_checker.py --path ./cartella --baseline hashes.json --mode init
  python file_integrity_checker.py --path ./cartella --baseline hashes.json --mode check
"""

import argparse
import hashlib
import json
import os


def compute_sha256(path: str, block_size: int = 65536) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            hasher.update(block)
    return hasher.hexdigest()


def build_baseline(root_dir: str, baseline_file: str):
    baseline = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            try:
                baseline[full_path] = compute_sha256(full_path)
            except (PermissionError, OSError):
                continue
    with open(baseline_file, "w") as f:
        json.dump(baseline, f, indent=2)
    print(f"[*] Baseline creata con {len(baseline)} file -> {baseline_file}")


def check_baseline(root_dir: str, baseline_file: str):
    if not os.path.isfile(baseline_file):
        print(f"[!] Baseline non trovata: {baseline_file}. Esegui prima --mode init.")
        return

    with open(baseline_file, "r") as f:
        baseline = json.load(f)

    current_files = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            try:
                current_files[full_path] = compute_sha256(full_path)
            except (PermissionError, OSError):
                continue

    modified = [p for p in baseline if p in current_files and baseline[p] != current_files[p]]
    deleted = [p for p in baseline if p not in current_files]
    added = [p for p in current_files if p not in baseline]

    print(f"[*] File modificati : {len(modified)}")
    for p in modified:
        print(f"    MODIFICATO -> {p}")
    print(f"[*] File eliminati  : {len(deleted)}")
    for p in deleted:
        print(f"    ELIMINATO  -> {p}")
    print(f"[*] File aggiunti   : {len(added)}")
    for p in added:
        print(f"    NUOVO      -> {p}")

    if not (modified or deleted or added):
        print("[*] Nessuna alterazione rilevata: integrita' confermata.")


def main():
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    parser.add_argument("--path", required=True, help="Cartella da monitorare")
    parser.add_argument("--baseline", required=True, help="File JSON per baseline")
    parser.add_argument("--mode", choices=["init", "check"], required=True,
                        help="init=crea baseline, check=verifica integrita'")
    args = parser.parse_args()

    if args.mode == "init":
        build_baseline(args.path, args.baseline)
    else:
        check_baseline(args.path, args.baseline)


if __name__ == "__main__":
    main()