#!/usr/bin/env python3
"""
Service Monitor
===============
Monitoraggio stato servizi di rete (HTTP, HTTPS, SSH, MySQL, PostgreSQL, ecc.)
con logging e alert su fallimento.

Esempio:
  python service_monitor.py --config services.json --interval 60
"""

import argparse
import json
import socket
import time
from datetime import datetime
from pathlib import Path

DEFAULT_SERVICES = [
    {"name": "Web Server", "host": "127.0.0.1", "port": 80, "type": "tcp"},
    {"name": "HTTPS", "host": "127.0.0.1", "port": 443, "type": "tcp"},
    {"name": "SSH", "host": "127.0.0.1", "port": 22, "type": "tcp"},
    {"name": "MySQL", "host": "127.0.0.1", "port": 3306, "type": "tcp"},
]


def check_service(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.error:
        return False


def main():
    parser = argparse.ArgumentParser(description="Service Monitor")
    parser.add_argument("--config", help="File JSON con lista servizi")
    parser.add_argument("--interval", type=int, default=60, help="Intervallo controllo (secondi)")
    parser.add_argument("--once", action="store_true", help="Esegui una volta sola")
    args = parser.parse_args()

    if args.config and Path(args.config).exists():
        with open(args.config) as f:
            services = json.load(f)
    else:
        services = DEFAULT_SERVICES
        print("[*] Nessun config fornito, uso servizi di default")

    log_file = Path("service_monitor.log")
    print(f"[*] Monitoraggio attivo (intervallo: {args.interval}s). Log: {log_file}")

    try:
        while True:
            timestamp = datetime.now().isoformat()
            for svc in services:
                name = svc.get("name", f"{svc['host']}:{svc['port']}")
                ok = check_service(svc["host"], svc["port"])
                status = "UP" if ok else "DOWN"
                entry = f"[{timestamp}] {name} -> {status}\n"
                print(entry.strip())
                with open(log_file, "a") as f:
                    f.write(entry)
                if not ok:
                    print(f"    [!] ALERT: {name} non raggiungibile!")

            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[*] Monitoraggio interrotto.")


if __name__ == "__main__":
    main()