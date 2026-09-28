#!/usr/bin/env python3
"""
File Encryptor AES-256-GCM
==========================
Cifra e decifra file usando AES-256 in modalità GCM (autenticata).
Derivazione chiave con PBKDF2 (200.000 iterazioni, SHA-256).

Dipendenza:
  pip install pycryptodome

Esempi:
  python file_encryptor_aes256.py --mode encrypt --file dati.txt --password "chiave-segreta"
  python file_encryptor_aes256.py --mode decrypt --file dati.txt.enc --password "chiave-segreta"
"""

import argparse
import os
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=32, count=200_000, hmac_hash_module=SHA256)


def encrypt_file(filepath: str, password: str):
    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM)

    with open(filepath, "rb") as f:
        plaintext = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    out_path = filepath + ".enc"

    with open(out_path, "wb") as f:
        for part in (salt, cipher.nonce, tag, ciphertext):
            f.write(part)

    print(f"[*] File cifrato con AES-256-GCM -> {out_path}")


def decrypt_file(filepath: str, password: str):
    with open(filepath, "rb") as f:
        salt = f.read(16)
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        print("[!] Decifratura fallita: password errata o file corrotto/manomesso.")
        return

    out_path = filepath.replace(".enc", ".dec")
    with open(out_path, "wb") as f:
        f.write(plaintext)
    print(f"[*] File decifrato correttamente -> {out_path}")


def main():
    parser = argparse.ArgumentParser(description="File Encryptor AES-256-GCM")
    parser.add_argument("--mode", choices=["encrypt", "decrypt"], required=True,
                        help="encrypt=cifra, decrypt=decifra")
    parser.add_argument("--file", required=True, help="File da cifrare/decifrare")
    parser.add_argument("--password", required=True, help="Password per derivare la chiave")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"[!] File non trovato: {args.file}")
        return

    if args.mode == "encrypt":
        encrypt_file(args.file, args.password)
    else:
        decrypt_file(args.file, args.password)


if __name__ == "__main__":
    main()