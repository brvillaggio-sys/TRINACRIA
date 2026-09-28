#!/usr/bin/env python3
"""
Zero-Day Behavioral Analyzer
============================
Analisi comportamentale per rilevare attività anomale (possibili zero-day).

Esempio:
  python zero_day_behavioral_analyzer.py --process-log proc.log --baseline baseline.json --mode learn|detect
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

PROCESS_PATTERN = re.compile(
    r"(?P<timestamp>\S+)\s+(?P<user>\w+)\s+(?P<command>\S+)\s+(?P<args>.+)"
)


def extract_process_events(log_file: str) -> list:
    events = []
    with open(log_file) as f:
        for line in f:
            match = PROCESS_PATTERN.match(line.strip())
            if match:
                events.append({
                    "timestamp": match.group("timestamp"),
                    "user": match.group("user"),
                    "command": match.group("command"),
                    "args": match.group("args"),
                })
    return events


def build_baseline(events: list) -> dict:
    user_commands = defaultdict(Counter)
    command_args = defaultdict(Counter)

    for e in events:
        user_commands[e["user"]][e["command"]] += 1
        command_args[e["command"]][e["args"]] += 1

    baseline = {
        "user_commands": {
            user: cmd.most_common(10) for user, cmd in user_commands.items()
        },
        "command_args": {
            cmd: args.most_common(5) for cmd, args in command_args.items()
        },
    }
    return baseline


def detect_anomalies(events: list, baseline: dict) -> list:
    alerts = []
    for e in events:
        user = e["user"]
        cmd = e["command"]
        args = e["args"]

        # Comando mai visto per utente
        if user in baseline["user_commands"]:
            known_cmds = [c for c, _ in baseline["user_commands"][user]]
            if cmd not in known_cmds:
                alerts.append(f"[NEW_CMD] {user} ha eseguito {cmd} {args}")

        # Argomenti anomali per comando
        if cmd in baseline["command_args"]:
            known_args = [a for a, _ in baseline["command_args"][cmd]]
            if args not in known_args and len(known_args) >= 3:
                alerts.append(f"[NEW_ARGS] {user} ha eseguito {cmd} con args insoliti: {args}")

    return alerts


def main():
    parser = argparse.ArgumentParser(description="Zero-Day Behavioral Analyzer")
    parser.add_argument("--process-log", required=True, help="Log processi da analizzare")
    parser.add_argument("--baseline", required=True, help="File baseline JSON")
    parser.add_argument("--mode", choices=["learn", "detect"], required=True)
    args = parser.parse_args()

    events = extract_process_events(args.process_log)
    print(f"[*] Eventi processo estratti: {len(events)}")

    if args.mode == "learn":
        baseline = build_baseline(events)
        with open(args.baseline, "w") as f:
            json.dump(baseline, f, indent=2)
        print(f"[*] Baseline creata: {args.baseline}")
    else:
        if not Path(args.baseline).exists():
            print(f"[!] Baseline non trovata: {args.baseline}")
            return
        with open(args.baseline) as f:
            baseline = json.load(f)
        alerts = detect_anomalies(events, baseline)
        print(f"[*] Anomalie comportamentali: {len(alerts)}")
        for a in alerts:
            print(f"    [!] {a}")


if __name__ == "__main__":
    main()