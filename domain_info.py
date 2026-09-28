#!/usr/bin/env python3
"""
Domain Info (OSINT)
===================
Raccolta informazioni su dominio: WHOIS (simulato), DNS, record MX/TXT, ecc.

Esempio:
  python domain_info.py --domain example.com
"""

import argparse
import socket
from pathlib import Path

try:
    import dns.resolver
    HAS_DNS = True
except ImportError:
    HAS_DNS = False


def resolve_dns(domain: str, qtype: str = "A") -> list:
    if not HAS_DNS:
        return [f"[!] python-dnspython non installato. Usa: pip install dnspython"]
    try:
        answers = dns.resolver.resolve(domain, qtype)
        return [r.to_text() for r in answers]
    except Exception as e:
        return [f"Errore: {e}"]


def get_whois_info(domain: str) -> dict:
    # Nota: WHOIS reale richiederebbe libreria 'whois' o chiamata a sistema
    # Qui simuliamo struttura per estensibilità futura
    return {
        "domain": domain,
        "note": "WHOIS completo richiede: pip install python-whois",
    }


def main():
    parser = argparse.ArgumentParser(description="Domain Info (OSINT)")
    parser.add_argument("--domain", required=True, help="Dominio da analizzare")
    parser.add_argument("--output", help="File output JSON (opzionale)")
    args = parser.parse_args()

    print(f"[*] Raccolta info per: {args.domain}")

    results = {
        "domain": args.domain,
        "A": resolve_dns(args.domain, "A"),
        "AAAA": resolve_dns(args.domain, "AAAA"),
        "MX": resolve_dns(args.domain, "MX"),
        "TXT": resolve_dns(args.domain, "TXT"),
        "NS": resolve_dns(args.domain, "NS"),
        "SOA": resolve_dns(args.domain, "SOA"),
        "whois": get_whois_info(args.domain),
    }

    for rec_type, values in results.items():
        if rec_type == "whois":
            continue
        print(f"    {rec_type}: {', '.join(values[:5])}")

    if args.output:
        import json
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"[*] Report salvato: {args.output}")

    if not HAS_DNS:
        print("\n[!] Installa dnspython per query DNS complete: pip install dnspython")


if __name__ == "__main__":
    main()