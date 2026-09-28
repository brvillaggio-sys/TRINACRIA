#!/usr/bin/env python3
"""
Email Harvester (OSINT)
=======================
Estrae indirizzi email da pagine web o file HTML/txt usando regex.

Esempio:
  python email_harvester.py --url https://example.com/contatti
  python email_harvester.py --file pagina.html
"""

import argparse
import re
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


def extract_from_text(text: str) -> list:
    return list(set(EMAIL_PATTERN.findall(text)))


def fetch_url(url: str) -> str:
    if not HAS_REQUESTS:
        raise ImportError("requests non installato")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text


def main():
    parser = argparse.ArgumentParser(description="Email Harvester (OSINT)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="URL da cui estrarre email")
    group.add_argument("--file", help="File HTML/txt da cui estrarre email")
    parser.add_argument("--output", help="File output con email trovate")
    args = parser.parse_args()

    if args.url:
        if not HAS_REQUESTS:
            print("[!] Installa requests: pip install requests")
            return
        print(f"[*] Fetch URL: {args.url}")
        try:
            content = fetch_url(args.url)
        except Exception as e:
            print(f"[!] Errore fetch: {e}")
            return
    else:
        if not Path(args.file).exists():
            print(f"[!] File non trovato: {args.file}")
            return
        print(f"[*] Lettura file: {args.file}")
        with open(args.file) as f:
            content = f.read()

    emails = extract_from_text(content)
    print(f"[*] Email trovate: {len(emails)}")
    for e in sorted(emails):
        print(f"    {e}")

    if args.output:
        with open(args.output, "w") as f:
            for e in sorted(emails):
                f.write(f"{e}\n")
        print(f"[*] Lista salvata: {args.output}")


if __name__ == "__main__":
    main()