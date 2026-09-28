# Cyber Toolkit - Python Security Scripts

Raccolta di script Python per cybersecurity, automazione, OSINT e red-teaming etico.  
**Uso esclusivo su sistemi di cui si possiede autorizzazione esplicita** (laboratori propri, CTF, ambienti di test).

---

## ⚠️ Disclaimer Etico

Questi tool sono forniti **solo per scopi educativi e di testing autorizzato**.  
L'uso non autorizzato su reti o sistemi di terzi è illegale e viola normative come il GDPR e le leggi sulla cybersecurity.

---

## 📦 Struttura del Repository

### Core Security (5 script)
| File | Descrizione |
|------|-------------|
| `port_scanner.py` | Scanner TCP multithread con rilevamento servizi |
| `password_strength_checker.py` | Analisi robustezza password (entropia, blacklist, hash) |
| `log_watcher_bruteforce.py` | Rilevamento brute-force da log (es. auth.log) |
| `file_integrity_checker.py` | Baseline SHA-256 e rilevamento modifiche file |
| `file_encryptor_aes256.py` | Cifratura/decifratura AES-256-GCM con PBKDF2 |

### Automazioni (10 script)
| File | Descrizione |
|------|-------------|
| `auto_backup.py` | Backup automatizzato con compressione e hash |
| `service_monitor.py` | Monitoraggio stato servizi di rete (HTTP, SSH, DB) |
| `log_rotator.py` | Rotazione e archiviazione log con compressione |
| `disk_watcher.py` | Alert utilizzo disco oltre soglia configurabile |
| `process_watcher.py` | Monitoraggio processi critici e riavvio automatico |
| `ssl_expiry_checker.py` | Controllo scadenza certificati SSL/TLS |
| `config_auditor.py` | Verifica configurazioni di sicurezza (es. SSH, firewall) |
| `user_audit.py` | Audit utenti di sistema (ultimi login, shell, sudo) |
| `network_traffic_logger.py` | Logging traffico di rete con filter per IP/porta |
| `cron_healthcheck.py` | Verifica esecuzione cron job e invio alert |

### OSINT (5 script)
| File | Descrizione |
|------|-------------|
| `domain_info.py` | Raccolta info dominio (WHOIS, DNS, MX, TXT) |
| `subdomain_enum.py` | Enumerazione subdomain da wordlist |
| `email_harvester.py` | Estrazione email da pagine web (regex) |
| `ip_reputation.py` | Controllo reputazione IP (blacklist, ASN, geo) |
| `social_scraper.py` | Estrazione metadati pubblici da profili social (API-safe) |

### Red-Teaming Etico (5 script)
| File | Descrizione |
|------|-------------|
| `payload_generator.py` | Generazione payload base64/obfuscati per test |
| `credential_phishing_sim.py` | Simulatore di landing page phishing (solo test interni) |
| `wifi_probe_sniffer.py` | Rilevamento probe request Wi-Fi (monitor mode) |
| `usb_autorun_test.py` | Test autorun USB in ambiente controllato |
| `internal_recon.py` | Ricognizione interna (host, share, utenti) |

---

## 🚀 Installazione

```bash
# Clona il repository
git clone https://github.com/tuo-username/cyber-toolkit.git
cd cyber-toolkit

# Crea virtual environment (opzionale ma consigliato)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# o: venv\Scripts\activate  # Windows

# Installa dipendenze
pip install -r requirements.txt
```

---

## 📋 Requisiti

Vedi `requirements.txt` per tutte le dipendenze esterne.  
Alcuni script richiedono privilegi elevati (`sudo`) o modalità monitor per Wi-Fi.

---

## 💡 Esempi d'Uso

### Port Scanner
```bash
python port_scanner.py --target 127.0.0.1 --start 1 --end 1024
```

### Password Checker
```bash
python password_strength_checker.py --password "MiaPassword123!"
```

### Log Watcher
```bash
python log_watcher_bruteforce.py --file /var/log/auth.log --threshold 5
```

### File Integrity
```bash
# Crea baseline
python file_integrity_checker.py --path /etc --baseline etc_baseline.json --mode init

# Verifica integrità
python file_integrity_checker.py --path /etc --baseline etc_baseline.json --mode check
```

### Encrypt/Decrypt
```bash
# Cifra
python file_encryptor_aes256.py --mode encrypt --file dati.txt --password "chiave-segreta"

# Decifra
python file_encryptor_aes256.py --mode decrypt --file dati.txt.enc --password "chiave-segreta"
```

---

## 🛡️ Best Practices

- **Testare in ambienti isolati** prima di usare in produzione
- **Documentare ogni esecuzione** (log, output, timestamp)
- **Non condividere output sensibili** (hash, log, credential)
- **Aggiornare regolarmente** wordlist e blacklist

---

## 📄 Licenza

MIT License — vedi file `LICENSE`.

---

## 🤝 Contributi

Contributi benvenuti! Apri una issue o una PR per:
- Nuovi script
- Bug fix
- Miglioramenti documentazione

---

## 📬 Contatti

Per domande o collaborazioni: [tua-email@example.com](mailto:tua-email@example.com)

---

*Creato con ❤️ per la community cybersecurity italiana*