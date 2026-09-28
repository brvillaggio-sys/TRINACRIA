#!/usr/bin/env python3
"""
Internal Reconnaissance (Red-Teaming Etico)
===========================================
Ricognizione interna di rete: host attivi, share SMB, utenti (SOLO ambienti autorizzati).

Esempio:
  python internal_recon.py --subnet 192.168.1.0/24
"""

import argparse
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def ping_host(ip: str) -> bool:
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            capture_output=True,
            timeout=2
        )
        return result.returncode == 0
    except Exception:
        return False


def check_port(ip: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((ip, port)) == 0
    except Exception:
        return False


def scan_subnet(subnet: str, max_workers: int = 100) -> list:
    # Esempio: 192.168.1.0/24 -> 192.168.1.1-254
    base = ".".join(subnet.split(".")[:3])
    hosts = [f"{base}.{i}" for i in range(1, 255)]
    live = []

    print(f"[*] Scansione subnet {subnet} ({len(hosts)} host)")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(ping_host, h): h for h in hosts}
        for future in as_completed(futures):
            if future.result():
                live.append(futures[future])

    return sorted(live)


def main():
    parser = argparse.ArgumentParser(description="Internal Reconnaissance (Red-Teaming Etico)")
    parser.add_argument("--subnet", required=True, help="Subnet da scansionare (es. 192.168.1.0/24)")
    parser.add_argument("--ports", type=int, nargs="+", default=[22, 80, 443, 445, 3389], help="Porte da controllare")
    parser.add_argument("--output", help="File output con host attivi")
    args = parser.parse_args()

    print("[!] USO ESCLUSIVO IN RETI INTERNE AUTORIZZATE")

    live_hosts = scan_subnet(args.subnet)
    print(f"[*] Host attivi trovati: {len(live_hosts)}")

    results = []
    for host in live_hosts:
        open_ports = []
        for port in args.ports:
            if check_port(host, port):
                open_ports.append(port)
        if open_ports:
            entry = f"{host}: {open_ports}"
            print(f"    {entry}")
            results.append(entry)

    if args.output:
        with open(args.output, "w") as f:
            for r in results:
                f.write(f"{r}\n")
        print(f"[*] Report salvato: {args.output}")


if __name__ == "__main__":
    main()