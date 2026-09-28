#!/usr/bin/env python3
"""
Credential Leak Scanner
=======================
Scansiona file alla ricerca di credential esposte (API key, password, token).

Esempio:
  python credential_leak_scanner.py --scan /home/user/progetti --output report.json
"""

import argparse
import json
import re
from pathlib import Path

PATTERNS = {
    "AWS_ACCESS_KEY": re.compile(r"AKIA[0-9A-Z]{16}"),
    "AWS_SECRET_KEY": re.compile(r"[0-9A-Za-z/+=]{40}"),
    "GENERIC_API_KEY": re.compile(r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"]?([0-9A-Za-z]{20,})['\"]?"),
    "PASSWORD_ASSIGNMENT": re.compile(r"(?i)password\s*[=:]\s*['\"]?([^\s'\"]{6,})['\"]?"),
    "PRIVATE_KEY_HEADER": re.compile(r"-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----"),
    "GITHUB_TOKEN": re.compile(r"gh[pousr]_[0-9A-Za-z]{36,}"),
    "SLACK_TOKEN": re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"),
}

SKIP_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".ico", ".pdf", ".doc", ".docx", ".bin"}


def scan_file(file_path: Path) -> list:
    findings = []
    try:
        content = file_path.read_text(errors="ignore")
    except Exception:
        return findings

    for leak_type, pattern in PATTERNS.items():
        matches = pattern.findall(content)
        if matches:
            findings.append({
                "type": leak_type,
                "count": len(matches),
                "sample": str(matches[0][:20]) + "..." if len(str(matches[0])) > 20 else matches[0],
            })
    return findings


def main():
    parser = argparse.ArgumentParser(description="Credential Leak Scanner")
    parser.add_argument("--scan", required=True, help="Directory da scansionare")
    parser.add_argument("--output", help="File output JSON")
    args = parser.parse_args()

    scan_dir = Path(args.scan)
    print(f"[*] Scansione credential esposte: {scan_dir}")

    report = []
    for file_path in scan_dir.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() in SKIP_EXTENSIONS:
            continue

        findings = scan_file(file_path)
        if findings:
            entry = {
                "file": str(file_path),
                "findings": findings,
            }
            report.append(entry)
            print(f"    [!] {file_path.name}: {len(findings)} tipi di credential")
            for f in findings:
                print(f"        - {f['type']}: {f['count']} occorrenze (sample: {f['sample']})")

    print(f"\n[*] File con credential esposte: {len(report)}")
    if args.output:
        with open(args.output, "w") as f:
            json.dump({"scan_dir": str(scan_dir), "findings": report}, f, indent=2)
        print(f"[*] Report salvato: {args.output}")


if __name__ == "__main__":
    main()