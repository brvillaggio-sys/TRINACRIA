#!/usr/bin/env python3
"""
Subdomain Enumeration (OSINT)
=============================
Enumera subdomain da wordlist e verifica risoluzione DNS.

Esempio:
  python subdomain_enum.py --domain example.com --wordlist subdomains.txt
"""

import argparse
from pathlib import Path

try:
    import dns.resolver
    HAS_DNS = True
except ImportError:
    HAS_DNS = False


def load_wordlist(path: str) -> list:
    with open(path) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def check_subdomain(subdomain: str, domain: str) -> bool:
    if not HAS_DNS:
        return False
    try:
        dns.resolver.resolve(f"{subdomain}.{domain}", "A")
        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumeration (OSINT)")
    parser.add_argument("--domain", required=True, help="Dominio target")
    parser.add_argument("--wordlist", required=True, help="File wordlist subdomain")
    parser.add_argument("--output", help="File output con subdomain trovati")
    args = parser.parse_args()

    if not HAS_DNS:
        print("[!] Installa dnspython: pip install dnspython")
        return

    if not Path(args.wordlist).exists():
        print(f"[!] Wordlist non trovata: {args.wordlist}")
        return

    wordlist = load_wordlist(args.wordlist)
    print(f"[*] Enumerazione subdomain per {args.domain} ({len(wordlist)} entry)")

    found = []
    for sub in wordlist:
        if check_subdomain(sub, args.domain):
            found.append(f"{sub}.{args.domain}")
            print(f"    [+] TROVATO: {sub}.{args.domain}")

    print(f"\n[*] Subdomain trovati: {len(found)}")
    if args.output:
        with open(args.output, "w") as f:
            for sub in found:
                f.write(f"{sub}\n")
        print(f"[*] Lista salvata: {args.output}")


if __name__ == "__main__":
    main()