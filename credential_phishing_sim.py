#!/usr/bin/env python3
"""
Credential Phishing Simulator (Red-Teaming Etico)
=================================================
Genera landing page HTML per simulazioni phishing interne (SOLO test autorizzati).
Non raccoglie credential reali — solo mock per awareness training.

Esempio:
  python credential_phishing_sim.py --output login_page.html --company "MyCorp"
"""

import argparse
from pathlib import Path


def generate_phishing_page(company: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Accesso {company} - Simulazione Phishing</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f0f0f0; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
        .login-box {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 320px; }}
        h2 {{ text-align: center; color: #333; }}
        input {{ width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }}
        button {{ width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }}
        button:hover {{ background: #0056b3; }}
        .disclaimer {{ font-size: 12px; color: #666; text-align: center; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Accesso {company}</h2>
        <form onsubmit="event.preventDefault(); alert('SIMULAZIONE PHISHING: Nessuna credenziale è stata inviata. Questo è un test di sicurezza.');">
            <label>Email aziendale</label>
            <input type="email" name="email" placeholder="nome.cognome@{company.lower()}.com" required>
            <label>Password</label>
            <input type="password" name="password" placeholder="••••••••" required>
            <button type="submit">Accedi</button>
        </form>
        <p class="disclaimer">
            ⚠️ Questa è una pagina di SIMULAZIONE PHISHING per formazione sicurezza.<br>
            Nessuna credenziale viene raccolta o trasmessa.
        </p>
    </div>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Credential Phishing Simulator (Red-Teaming Etico)")
    parser.add_argument("--output", default="login_page.html", help="File HTML output")
    parser.add_argument("--company", default="Azienda", help="Nome azienda per personalizzazione")
    args = parser.parse_args()

    print("[!] USO ESCLUSIVO PER SIMULAZIONI INTERNE AUTORIZZATE (awareness training)")

    html = generate_phishing_page(args.company)
    with open(args.output, "w") as f:
        f.write(html)

    print(f"[*] Landing page generata: {args.output}")
    print(f"    Azienda: {args.company}")
    print("[*] Apri il file nel browser per testare la simulazione.")


if __name__ == "__main__":
    main()