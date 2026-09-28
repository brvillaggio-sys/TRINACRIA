#!/usr/bin/env python3
"""
Log Watcher - Rilevamento Brute-Force
=====================================
Analizza file di log (es. auth.log) per individuare tentativi di login falliti
e segnala gli IP che superano una soglia configurabile.

Esempio:
  python log_watcher_bruteforce.py --file auth.log --threshold 5
"""

import argparse
import os
import re
from collections import Counter, defaultdict

FAILED_LOGIN_PATTERN = re.compile(
    r"(?i)failed\s+password.*from\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)


def analyze_log_file(filepath: str, threshold: int = 5) -> dict:
    ip_counter = Counter()
    ip_timestamps = defaultdict(list)
    total_lines = 0
    matched_lines = 0

    with open(filepath, "r", errors="ignore") as f:
        for line in f:
            total_lines += 1
            match = FAILED_LOGIN_PATTERN.search(line)
            if match:
                matched_lines += 1
                ip = match.group("ip")
                ip_counter[ip] += 1
                ip_timestamps[ip].append(line.strip())

    suspicious = {ip: c for ip, c in ip_counter.items() if c >= threshold}
    return {
        "righe_totali": total_lines,
        "tentativi_falliti_totali": matched_lines,
        "ip_sospetti": suspicious,
        "dettaglio_ip": ip_timestamps,
    }


def main():
    parser = argparse.ArgumentParser(description="Log Watcher - Rilevamento Brute-Force")
    parser.add_argument("--file", required=True, help="File di log da analizzare")
    parser.add_argument("--threshold", type=int, default=5,
                        help="Soglia di tentativi falliti per segnalare un IP")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"[!] File non trovato: {args.file}")
        return

    print(f"[*] Analisi log '{args.file}' (soglia = {args.threshold} tentativi falliti) ...")
    result = analyze_log_file(args.file, args.threshold)

    print(f"    Righe analizzate      : {result['righe_totali']}")
    print(f"    Tentativi falliti     : {result['tentativi_falliti_totali']}")

    if result["ip_sospetti"]:
        print("[!] IP potenzialmente in brute-force:")
        for ip, count in sorted(result["ip_sospetti"].items(), key=lambda x: -x[1]):
            print(f"    {ip:<16} -> {count} tentativi falliti")
    else:
        print("    Nessun IP ha superato la soglia impostata.")


if __name__ == "__main__":
    main()