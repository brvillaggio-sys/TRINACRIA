#!/usr/bin/env python3
"""
Social Scraper (OSINT)
======================
Estrae metadati pubblici da profili social (solo dati accessibili via API/web scraping etico).
Nota: rispettare sempre ToS delle piattaforme e normative privacy.

Esempio:
  python social_scraper.py --platform twitter --username example_user
"""

import argparse
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def fetch_twitter_profile(username: str) -> dict:
    # Nota: Twitter/X richiede autenticazione per API complete.
    # Questo è un placeholder per struttura estensibile.
    return {
        "platform": "twitter",
        "username": username,
        "note": "API Twitter richiedono autenticazione. Implementare con tweepy o API v2.",
    }


def fetch_github_profile(username: str) -> dict:
    if not HAS_REQUESTS:
        return {"error": "requests non installato"}
    try:
        resp = requests.get(f"https://api.github.com/users/{username}", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {
            "platform": "github",
            "username": username,
            "name": data.get("name"),
            "bio": data.get("bio"),
            "public_repos": data.get("public_repos"),
            "followers": data.get("followers"),
            "created_at": data.get("created_at"),
            "url": data.get("html_url"),
        }
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Social Scraper (OSINT)")
    parser.add_argument("--platform", choices=["twitter", "github", "linkedin"], required=True)
    parser.add_argument("--username", required=True, help="Username da analizzare")
    parser.add_argument("--output", help="File output JSON")
    args = parser.parse_args()

    if not HAS_REQUESTS:
        print("[!] Installa requests: pip install requests")
        return

    print(f"[*] Analisi profilo {args.platform}: @{args.username}")

    if args.platform == "twitter":
        result = fetch_twitter_profile(args.username)
    elif args.platform == "github":
        result = fetch_github_profile(args.username)
    else:
        result = {"platform": args.platform, "note": "LinkedIn richiede autenticazione/autorizzazione."}

    for k, v in result.items():
        print(f"    {k}: {v}")

    if args.output:
        import json
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"[*] Report salvato: {args.output}")


if __name__ == "__main__":
    main()