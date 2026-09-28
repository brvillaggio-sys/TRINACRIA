#!/usr/bin/env python3
"""
User Audit
==========
Audit utenti di sistema (Linux): ultimi login, shell, privilegi sudo, ecc.
Richiede accesso a /etc/passwd, /etc/shadow (opzionale), last, sudo -l.

Esempio:
  python user_audit.py --output report.json
"""

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


def run_cmd(cmd: list) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"[ERROR: {e}]"


def parse_passwd() -> list:
    users = []
    try:
        with open("/etc/passwd") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 7:
                    users.append({
                        "username": parts[0],
                        "uid": parts[2],
                        "gid": parts[3],
                        "home": parts[5],
                        "shell": parts[6],
                    })
    except PermissionError:
        pass
    return users


def get_last_login(username: str) -> str:
    out = run_cmd(["last", "-n", "1", username])
    if "reboot" in out or not out:
        return "N/A"
    return out.split()[-3] if len(out.split()) >= 5 else "N/A"


def check_sudo_privs(username: str) -> str:
    out = run_cmd(["sudo", "-l", "-U", username])
    if "may run" in out.lower() or "(ALL)" in out:
        return "PRIVILEGIATO"
    return "STANDARD"


def main():
    parser = argparse.ArgumentParser(description="User Audit")
    parser.add_argument("--output", default="user_audit.json", help="File output JSON")
    args = parser.parse_args()

    if os.geteuid() != 0:
        print("[!] Avviso: eseguito senza root. Alcuni dati potrebbero essere limitati.")

    users = parse_passwd()
    report = []
    print(f"[*] Audit utenti di sistema ({len(users)} trovati)")

    for u in users:
        if int(u["uid"]) < 1000 and u["username"] != "root":
            continue  # Salta utenti di sistema
        last_login = get_last_login(u["username"])
        sudo_status = check_sudo_privs(u["username"])
        entry = {
            "username": u["username"],
            "uid": u["uid"],
            "shell": u["shell"],
            "home": u["home"],
            "last_login": last_login,
            "sudo_status": sudo_status,
        }
        report.append(entry)
        print(f"    {u['username']:<15} | Shell: {u['shell']:<10} | Sudo: {sudo_status}")

    with open(args.output, "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "users": report}, f, indent=2)

    print(f"[*] Report salvato: {args.output}")


if __name__ == "__main__":
    main()