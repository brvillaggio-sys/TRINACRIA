#!/usr/bin/env python3
"""
Port Scanner Multithread
========================
Scansiona un range di porte TCP su un target specificato.
Uso etico: eseguire SOLO su sistemi/reti di cui si ha autorizzazione esplicita.

Esempio:
  python port_scanner.py --target 127.0.0.1 --start 1 --end 1024
"""

import argparse
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
}


def scan_port(target: str, port: int, timeout: float = 0.6) -> tuple | None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        if result == 0:
            service = COMMON_PORTS.get(port, "unknown")
            return port, service
    return None


def main():
    parser = argparse.ArgumentParser(description="Port Scanner Multithread")
    parser.add_argument("--target", required=True, help="IP o hostname target")
    parser.add_argument("--start", type=int, default=1, help="Porta iniziale")
    parser.add_argument("--end", type=int, default=1024, help="Porta finale")
    parser.add_argument("--workers", type=int, default=200, help="Thread massimi")
    parser.add_argument("--timeout", type=float, default=0.6, help="Timeout per socket")
    args = parser.parse_args()

    print(f"[*] Scansione di {args.target} sulle porte {args.start}-{args.end} ...")
    open_ports = []
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(scan_port, args.target, p, args.timeout): p
            for p in range(args.start, args.end + 1)
        }
        for future in as_completed(futures):
            res = future.result()
            if res:
                open_ports.append(res)

    open_ports.sort()
    elapsed = time.time() - t0
    print(f"[*] Scansione completata in {elapsed:.2f}s. Porte aperte trovate: {len(open_ports)}")
    for port, service in open_ports:
        print(f"    PORT {port:>5}/tcp  OPEN  -> {service}")
    if not open_ports:
        print("    Nessuna porta aperta rilevata nel range indicato.")


if __name__ == "__main__":
    main()