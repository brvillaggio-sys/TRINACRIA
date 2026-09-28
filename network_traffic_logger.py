#!/usr/bin/env python3
"""
Network Traffic Logger
======================
Logga traffico di rete filtrando per IP e porta (richiede scapy o tcpdump).

Esempio:
  python network_traffic_logger.py --filter "tcp port 80" --output traffic.log
"""

import argparse
import subprocess
import signal
import sys
from pathlib import Path


def run_tcpdump(filter_expr: str, output_file: Path, timeout: int = 60):
    cmd = [
        "tcpdump", "-n", "-l",
        "-i", "any",
        filter_expr,
    ]
    print(f"[*] Avvio tcpdump: {' '.join(cmd)} > {output_file}")
    proc = subprocess.Popen(cmd, stdout=open(output_file, "w"), stderr=subprocess.DEVNULL)

    def handler(sig, frame):
        print("\n[*] Interruzione ricezione...")
        proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.terminate()
        print(f"[*] Sessione terminata dopo {timeout}s")


def main():
    parser = argparse.ArgumentParser(description="Network Traffic Logger")
    parser.add_argument("--filter", default="tcp", help="Filtro tcpdump (es. 'tcp port 80')")
    parser.add_argument("--output", default="traffic.log", help="File output log")
    parser.add_argument("--timeout", type=int, default=60, help="Durata sessione (secondi)")
    args = parser.parse_args()

    print("[!] Richiede privilegi elevati (sudo) per tcpdump")
    output = Path(args.output)
    run_tcpdump(args.filter, output, args.timeout)
    print(f"[*] Log salvato: {output}")


if __name__ == "__main__":
    main()