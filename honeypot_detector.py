#!/usr/bin/env python3
"""
Honeypot Detector
=================
Rileva tentativi di accesso a porte/service fake (honeypot) e logga attacker.

Esempio:
  python honeypot_detector.py --ports 22,80,443,3389 --log honeypot.log
"""

import argparse
import socket
import threading
import time
from datetime import datetime
from pathlib import Path


class HoneypotPort:
    def __init__(self, port: int, log_file: Path):
        self.port = port
        self.log_file = log_file
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(5)
        self.running = True

    def log_connection(self, addr: tuple):
        entry = f"[{datetime.now().isoformat()}] Tentativo connessione porta {self.port} da {addr[0]}:{addr[1]}\n"
        with open(self.log_file, "a") as f:
            f.write(entry)
        print(f"    [!] {entry.strip()}")

    def run(self):
        print(f"[*] Honeypot attivo su porta {self.port}")
        while self.running:
            try:
                conn, addr = self.sock.accept()
                self.log_connection(addr)
                conn.close()
            except Exception:
                break

    def stop(self):
        self.running = False
        self.sock.close()


def main():
    parser = argparse.ArgumentParser(description="Honeypot Detector")
    parser.add_argument("--ports", type=str, required=True, help="Porte da ascoltare (es. 22,80,443)")
    parser.add_argument("--log", default="honeypot.log", help="File log")
    args = parser.parse_args()

    log_file = Path(args.log)
    ports = [int(p.strip()) for p in args.split(",")]

    print(f"[*] Avvio honeypot su porte: {ports}")
    print("[!] Richiede privilegi elevati per porte < 1024")

    honeypots = []
    threads = []
    for port in ports:
        hp = HoneypotPort(port, log_file)
        honeypots.append(hp)
        t = threading.Thread(target=hp.run, daemon=True)
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Arresto honeypot...")
        for hp in honeypots:
            hp.stop()


if __name__ == "__main__":
    main()