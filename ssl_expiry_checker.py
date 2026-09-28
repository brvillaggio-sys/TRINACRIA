#!/usr/bin/env python3
"""
SSL Expiry Checker
==================
Controlla la scadenza di certificati SSL/TLS per uno o più domini.

Esempio:
  python ssl_expiry_checker.py --domains example.com api.example.com --threshold 30
"""

import argparse
import socket
import ssl
from datetime import datetime
from pathlib import Path


def check_ssl_expiry(domain: str, port: int = 443, timeout: float = 5.0) -> dict:
    context = ssl.create_default_context()
    with socket.create_connection((domain, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
            not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
            not_before = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
            days_left = (not_after - datetime.utcnow()).days
            return {
                "domain": domain,
                "not_before": not_before.isoformat(),
                "not_after": not_after.isoformat(),
                "days_left": days_left,
                "issuer": dict(x[0] for x in cert["issuer"]),
                "subject": dict(x[0] for x in cert["subject"]),
            }


def main():
    parser = argparse.ArgumentParser(description="SSL Expiry Checker")
    parser.add_argument("--domains", nargs="+", required=True, help="Domini da controllare")
    parser.add_argument("--threshold", type=int, default=30, help="Giorni soglia per alert")
    args = parser.parse_args()

    log_file = Path("ssl_expiry.log")
    print(f"[*] Controllo scadenza certificati (soglia: {args.threshold} giorni)")

    results = []
    for domain in args.domains:
        try:
            info = check_ssl_expiry(domain)
            results.append(info)
            status = "OK" if info["days_left"] > args.threshold else "WARNING"
            print(f"    [{status}] {domain}: scade tra {info['days_left']} giorni ({info['not_after']})")
        except Exception as e:
            print(f"    [ERROR] {domain}: {e}")
            results.append({"domain": domain, "error": str(e)})

    with open(log_file, "a") as f:
        for r in results:
            f.write(f"[{datetime.now().isoformat()}] {r}\n")

    alerts = [r for r in results if r.get("days_left", 999) <= args.threshold]
    if alerts:
        print(f"\n[!] {len(alerts)} certificati in scadenza entro {args.threshold} giorni!")
        for a in alerts:
            print(f"    - {a['domain']}: {a['days_left']} giorni rimanenti")


if __name__ == "__main__":
    main()