#!/usr/bin/env python3
"""
File Quarantine System
======================
Isola file sospetti (per estensione, entropia, hash) in area quarantena cifrata.

Esempio:
  python file_quarantine.py --scan /home/user/Downloads --quarantine /quarantine --threshold 7.5
"""

import argparse
import hashlib
import math
import os
import shutil
from pathlib import Path

SUSPICIOUS_EXTENSIONS = {".exe", ".dll", ".bat", ".ps1", ".vbs", ".js", ".msi", ".scr", ".cmd"}


def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counter = Counter(data)
    length = len(data)
    entropy = -sum((c / length) * math.log2(c / length) for c in counter.values())
    return entropy


def compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main():
    from collections import Counter

    parser = argparse.ArgumentParser(description="File Quarantine System")
    parser.add_argument("--scan", required=True, help="Directory da scansionare")
    parser.add_argument("--quarantine", required=True, help="Directory quarantena")
    parser.add_argument("--threshold", type=float, default=7.5, help="Soglia entropia per sospetto")
    args = parser.parse_args()

    scan_dir = Path(args.scan)
    quarantine_dir = Path(args.quarantine)
    quarantine_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Scansione: {scan_dir} (soglia entropia: {args.threshold})")

    quarantined = []
    for file_path in scan_dir.rglob("*"):
        if not file_path.is_file():
            continue

        # Check estensione
        if file_path.suffix.lower() in SUSPICIOUS_EXTENSIONS:
            reason = "ESTENSIONE_SOSPETTA"
        else:
            # Check entropia
            try:
                data = file_path.read_bytes()
                entropy = calculate_entropy(data)
                if entropy > args.threshold:
                    reason = f"ENTROPIA_ALTA ({entropy:.2f})"
                else:
                    continue
            except Exception:
                continue

        # Quarantena
        sha256 = compute_sha256(file_path)
        dest = quarantine_dir / f"{sha256[:16]}_{file_path.name}"
        shutil.copy2(file_path, dest)
        quarantined.append((str(file_path), reason, sha256))
        print(f"    [!] Quarantena: {file_path.name} -> {reason}")

    # Manifest
    manifest = quarantine_dir / "manifest.json"
    import json
    with open(manifest, "w") as f:
        json.dump({
            "scan_dir": str(scan_dir),
            "threshold": args.threshold,
            "files": [
                {"original": p, "reason": r, "sha256": h}
                for p, r, h in quarantined
            ]
        }, f, indent=2)

    print(f"\n[*] File in quarantena: {len(quarantined)}")
    print(f"[*] Manifest: {manifest}")


if __name__ == "__main__":
    main()