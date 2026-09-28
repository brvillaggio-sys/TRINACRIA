#!/usr/bin/env python3
"""
Auto Incident Responder
=======================
Risposta automatica a incidenti: isola host, blocca IP, notifica team.

Esempio:
  python auto_incident_responder.py --alert alert.json --action isolate|block|notify
"""

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


def isolate_host(ip: str) -> bool:
    # Isola host tramite iptables (DROP tutto il traffico)
    try:
        subprocess.run(
            ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
            check=True,
            timeout=5
        )
        subprocess.run(
            ["iptables", "-A", "OUTPUT", "-d", ip, "-j", "DROP"],
            check=True,
            timeout=5
        )
        return True
    except Exception as e:
        print(f"    [!] Errore isolamento {ip}: {e}")
        return False


def block_ip(ip: str) -> bool:
    try:
        subprocess.run(
            ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
            check=True,
            timeout=5
        )
        return True
    except Exception as e:
        print(f"    [!] Errore blocco {ip}: {e}")
        return False


def notify_team(message: str, channel: str = "security-alerts") -> bool:
    # Placeholder: integrare con Slack/Email/Telegram
    log_file = Path("incident_notifications.log")
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] [{channel}] {message}\n")
    print(f"    [*] Notifica inviata: {message}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Auto Incident Responder")
    parser.add_argument("--alert", required=True, help="File JSON con dettagli alert")
    parser.add_argument("--action", choices=["isolate", "block", "notify"], required=True)
    args = parser.parse_args()

    with open(args.alert) as f:
        alert = json.load(f)

    print(f"[*] Risposta automatica a incidente: {alert.get('type', 'UNKNOWN')}")

    if args.action == "isolate":
        ip = alert.get("ip")
        if ip and isolate_host(ip):
            notify_team(f"Host isolato: {ip}")
        else:
            print("[!] Isolamento fallito")

    elif args.action == "block":
        ip = alert.get("ip")
        if ip and block_ip(ip):
            notify_team(f"IP bloccato: {ip}")
        else:
            print("[!] Blocco IP fallito")

    elif args.action == "notify":
        message = alert.get("description", "Incidente di sicurezza rilevato")
        notify_team(message)


if __name__ == "__main__":
    main()