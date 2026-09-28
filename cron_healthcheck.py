#!/usr/bin/env python3
"""
Cron Healthcheck
================
Verifica esecuzione cron job e invia alert se non eseguiti entro finestra attesa.

Esempio:
  python cron_healthcheck.py --job "backup_daily" --expected-interval 86400 --marker /tmp/backup_last_run
"""

import argparse
import os
import time
from datetime import datetime
from pathlib import Path


def check_cron_job(marker_file: str, expected_interval: int) -> dict:
    path = Path(marker_file)
    if not path.exists():
        return {"status": "MISSING", "note": "File marker non trovato"}

    last_run = datetime.fromtimestamp(path.stat().st_mtime)
    now = datetime.now()
    delta = (now - last_run).total_seconds()
    overdue = delta > expected_interval

    return {
        "status": "OK" if not overdue else "OVERDUE",
        "last_run": last_run.isoformat(),
        "delta_seconds": int(delta),
        "expected_interval": expected_interval,
        "overdue": overdue,
    }


def main():
    parser = argparse.ArgumentParser(description="Cron Healthcheck")
    parser.add_argument("--job", required=True, help="Nome identificativo job")
    parser.add_argument("--expected-interval", type=int, required=True, help="Intervallo atteso in secondi")
    parser.add_argument("--marker", required=True, help="File marker aggiornato dal cron job")
    args = parser.parse_args()

    print(f"[*] Healthcheck cron job: {args.job}")
    result = check_cron_job(args.marker, args.expected_interval)

    print(f"    Status: {result['status']}")
    if "last_run" in result:
        print(f"    Ultimo run: {result['last_run']}")
        print(f"    Trascorso: {result['delta_seconds']}s (atteso: {result['expected_interval']}s)")

    if result.get("overdue"):
        print(f"    [!] ALERT: Job {args.job} non eseguito in tempo!")
        # Qui si potrebbe integrare invio email/Slack


if __name__ == "__main__":
    main()