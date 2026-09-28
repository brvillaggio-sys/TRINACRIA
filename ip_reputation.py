#!/usr/bin/env python3
"""
IP Reputation Checker (OSINT)
=============================
Controlla reputazione di un IP: blacklist, ASN, geolocalizzazione (API-free).

Esempio:
  python ip_reputation.py --ip 8.8.8.8
"""

import argparse
import socket
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError


def reverse_dns(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "N/A"


def get_ip_info(ip: str) -> dict:
    # Usa API pubbliche free (es. ipapi, ip-api.com)
    try:
        with urlopen(f"http://ip-api.com/{ip}?fields=status,message,country,regionName,city,isp,org,as", timeout=5) as resp:
            import json
            data = json.loads(resp.read().decode())
            if data.get("status") != "success":
                return {"error": data.get("message", "Unknown error")}
            return {
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "isp": data.get("isp"),
                "org": data.get("org"),
                "as": data.get("as"),
            }
    except URLError as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="IP Reputation Checker (OSINT)")
    parser.add_argument("--ip", required=True, help="Indirizzo IP da analizzare")
    parser.add_argument("--output", help="File output JSON")
    args = parser.parse_args()

    print(f"[*] Analisi IP: {args.ip}")

    rdns = reverse_dns(args.ip)
    info = get_ip_info(args.ip)

    print(f"    Reverse DNS: {rdns}")
    if "error" in info:
        print(f"    [!] Errore info IP: {info['error']}")
    else:
        print(f"    Paese: {info.get('country')}")
        print(f"    Città: {info.get('city')}")
        print(f"    ISP: {info.get('isp')}")
        print(f"    ASN: {info.get('as')}")

    report = {
        "ip": args.ip,
        "reverse_dns": rdns,
        "info": info,
    }

    if args.output:
        import json
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"[*] Report salvato: {args.output}")


if __name__ == "__main__":
    main()