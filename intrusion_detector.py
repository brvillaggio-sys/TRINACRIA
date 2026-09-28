#!/usr/bin/env python3
"""
Intrusion Detection System (IDS) - Behavioral
==============================================
Rileva anomalie comportamentali: login orari insoliti, comandi sospetti, picchi di attività.

Esempio:
  python intrusion_detector.py --log auth.log --baseline baseline.json --mode learn|detect
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


LOGIN_PATTERN = re.compile(r"(?i)accepted\s+\w+\s+for\s+(?P<user>\w+)\s+from\s+(?P<ip>[\d.]+)")


def extract_login_events(log_file: str) -> list:
    events = []
    with open(log_file) as f:
        for line in f:
            match = LOGIN_PATTERN.search(line)
            if match:
                events.append({
                    "user": match.group("user"),
                    "ip": match.group("ip"),
                    "hour": datetime.strptime(line.split()[0][:19], "%Y-%m-%dT%H:%M:%S").hour,
                })
    return events


def build_baseline(events: list) -> dict:
    user_hours = defaultdict(list)
    user_ips = defaultdict(set)
    for e in events:
        user_hours[e["user"]].append(e["hour"])
        user_ips[e["user"]].add(e["ip"])

    baseline = {}
    for user, hours in user_hours.items():
        counter = Counter(hours)
        normal_hours = [h for h, c in counter.items() if c >= 2]
        baseline[user] = {
            "normal_hours": sorted(normal_hours),
            "known_ips": list(user_ips[user]),
        }
    return baseline


def detect_anomalies(events: list, baseline: dict) -> list:
    alerts = []
    for e in events:
        user = e["user"]
        if user not in baseline:
            alerts.append(f"[NEW_USER] {user} da {e['ip']} alle {e['hour']}:00")
            continue

        b = baseline[user]
        if e["hour"] not in b["normal_hours"]:
            alerts.append(f"[ORA_INSOLITA] {user} da {e['ip']} alle {e['hour']}:00 (ore normali: {b['normal_hours']})")
        if e["ip"] not in b["known_ips"]:
            alerts.append(f"[NUOVO_IP] {user} da {e['ip']} alle {e['hour']}:00 (IP noti: {b['known_ips']})")
    return alerts


def main():
    parser = argparse.ArgumentParser(description="Intrusion Detection System (Behavioral)")
    parser.add_argument("--log", required=True, help="File log da analizzare")
    parser.add_argument("--baseline", required=True, help="File baseline JSON")
    parser.add_argument("--mode", choices=["learn", "detect"], required=True)
    args = parser.parse_args()

    events = extract_login_events(args.log)
    print(f"[*] Eventi login estratti: {len(events)}")

    if args.mode == "learn":
        baseline = build_baseline(events)
        with open(args.baseline, "w") as f:
            json.dump(baseline, f, indent=2)
        print(f"[*] Baseline creata: {args.baseline}")
        for user, b in baseline.items():
            print(f"    {user}: ore normali={b['normal_hours']}, IP noti={b['known_ips']}")
    else:
        if not Path(args.baseline).exists():
            print(f"[!] Baseline non trovata: {args.baseline}. Esegui prima --mode learn")
            return
        with open(args.baseline) as f:
            baseline = json.load(f)
        alerts = detect_anomalies(events, baseline)
        print(f"[*] Anomalie rilevate: {len(alerts)}")
        for a in alerts:
            print(f"    [!] {a}")


if __name__ == "__main__":
    main()