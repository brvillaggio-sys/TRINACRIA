#!/usr/bin/env python3
"""
Network Segmentation Enforcer
=============================
Verifica che le regole di segmentazione di rete siano attive (iptables/nftables).

Esempio:
  python network_segmentation_enforcer.py --policy policy.json
"""

import argparse
import json
import subprocess
from pathlib import Path


def get_iptables_rules() -> str:
    try:
        result = subprocess.run(
            ["iptables", "-L", "-n", "-v"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"[ERROR: {e}]"


def check_policy(rules: str, policy: dict) -> list:
    violations = []
    for rule in policy.get("required_rules", []):
        if rule not in rules:
            violations.append(f"[VIOLATION] Regola mancante: {rule}")
    return violations


def main():
    parser = argparse.ArgumentParser(description="Network Segmentation Enforcer")
    parser.add_argument("--policy", required=True, help="File JSON con policy di segmentazione")
    args = parser.parse_args()

    if not Path(args.policy).exists():
        print(f"[!] Policy non trovata: {args.policy}")
        return

    with open(args.policy) as f:
        policy = json.load(f)

    print("[*] Verifica segmentazione di rete")
    rules = get_iptables_rules()

    if rules.startswith("[ERROR"):
        print(f"    {rules}")
        print("[!] Richiede privilegi elevati (sudo) per iptables")
        return

    violations = check_policy(rules, policy)
    if violations:
        print(f"\n[!] VIOLAZIONI RILEVATE ({len(violations)}):")
        for v in violations:
            print(f"    {v}")
    else:
        print("[*] Tutte le regole di segmentazione sono attive")


if __name__ == "__main__":
    main()