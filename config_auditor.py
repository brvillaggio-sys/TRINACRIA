#!/usr/bin/env python3
"""
Config Auditor
==============
Verifica configurazioni di sicurezza (SSH, firewall, ecc.) su Linux.

Esempio:
  python config_auditor.py --checks ssh,firewall
"""

import argparse
import os
import subprocess
from pathlib import Path


def check_ssh_config() -> dict:
    sshd_config = Path("/etc/ssh/sshd_config")
    results = {"file": str(sshd_config), "checks": []}
    if not sshd_config.exists():
        results["error"] = "File non trovato"
        return results

    with open(sshd_config) as f:
        content = f.read().lower()

    checks = [
        ("PermitRootLogin no", "permitrootlogin no" in content),
        ("PasswordAuthentication no", "passwordauthentication no" in content),
        ("PermitEmptyPasswords no", "permitemptypasswords no" in content),
        ("X11Forwarding no", "x11forwarding no" in content),
    ]
    for name, ok in checks:
        results["checks"].append({"name": name, "status": "OK" if ok else "WARNING"})

    return results


def check_firewall() -> dict:
    try:
        out = subprocess.run(["iptables", "-L", "-n"], capture_output=True, text=True, timeout=5)
        lines = out.stdout.splitlines()
        has_rules = any("ACCEPT" in l or "DROP" in l or "REJECT" in l for l in lines)
        return {"status": "OK" if has_rules else "WARNING", "note": "Regole firewall presenti" if has_rules else "Nessuna regola rilevata"}
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Config Auditor")
    parser.add_argument("--checks", nargs="+", choices=["ssh", "firewall"], default=["ssh", "firewall"])
    parser.add_argument("--output", help="File output JSON")
    args = parser.parse_args()

    if os.geteuid() != 0:
        print("[!] Avviso: eseguito senza root. Alcuni check potrebbero fallire.")

    report = {}
    print("[*] Audit configurazioni di sicurezza")

    if "ssh" in args.checks:
        print("\n[*] SSH Config:")
        ssh_result = check_ssh_config()
        for c in ssh_result.get("checks", []):
            status = c["status"]
            print(f"    {c['name']:<30} -> {status}")
        report["ssh"] = ssh_result

    if "firewall" in args.checks:
        print("\n[*] Firewall:")
        fw_result = check_firewall()
        print(f"    Status: {fw_result.get('status', 'ERROR')}")
        if "note" in fw_result:
            print(f"    Note: {fw_result['note']}")
        report["firewall"] = fw_result

    if args.output:
        import json
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n[*] Report salvato: {args.output}")


if __name__ == "__main__":
    main()