#!/usr/bin/env python3
"""
Password Strength Checker
=========================
Analizza robustezza di una password: lunghezza, complessità, presenza in liste comuni,
stima entropia e calcola hash SHA-256.

Esempio:
  python password_strength_checker.py --password "MiaPassword123!"
"""

import argparse
import hashlib
import re

COMMON_WEAK_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "abc123", "password1",
    "admin", "letmein", "welcome", "111111", "iloveyou", "monkey",
}


def check_password_strength(password: str) -> dict:
    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[^\w\s]", password))
    is_common = password.lower() in COMMON_WEAK_PASSWORDS

    score = sum([
        length >= 8,
        length >= 12,
        has_lower,
        has_upper,
        has_digit,
        has_symbol,
    ])
    if is_common:
        score = 0

    levels = [
        "Molto Debole", "Debole", "Discreta", "Buona",
        "Forte", "Molto Forte", "Eccellente"
    ]
    level = levels[min(score, len(levels) - 1)]

    # Entropia stimata (approssimativa)
    charset_size = (
        (has_lower * 26) + (has_upper * 26) +
        (has_digit * 10) + (has_symbol * 32)
    )
    entropy_bits = length * max(1, charset_size).bit_length() if password else 0

    sha256_hash = hashlib.sha256(password.encode()).hexdigest()

    return {
        "lunghezza": length,
        "minuscole": has_lower,
        "maiuscole": has_upper,
        "cifre": has_digit,
        "simboli": has_symbol,
        "password_comune": is_common,
        "punteggio": score,
        "livello": level,
        "entropia_stimata_bit": entropy_bits,
        "sha256": sha256_hash,
    }


def main():
    parser = argparse.ArgumentParser(description="Password Strength Checker")
    parser.add_argument("--password", required=True, help="Password da analizzare")
    args = parser.parse_args()

    report = check_password_strength(args.password)
    print("[*] Analisi robustezza password:")
    for k, v in report.items():
        print(f"    {k:<24}: {v}")
    if report["password_comune"]:
        print("[!] ATTENZIONE: password presente in liste di password comuni/compromesse.")


if __name__ == "__main__":
    main()