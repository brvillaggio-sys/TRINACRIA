# TRINACRIA

Una collezione di script Python focalizzati sulla cybersecurity, l'analisi dei dati e l'ottimizzazione delle risorse di sistema. 
Questi strumenti sono stati progettati per essere leggeri, memory-safe ed efficienti, risultando ideali anche per ambienti con risorse hardware limitate (es. sistemi con 4GB di RAM).

## Struttura del Progetto

Il repository è diviso in due aree principali: moduli per la **Cybersecurity** e **Utility** di uso generale.

### 🛡️ Cybersecurity
*   `cybersecurity/async_honeypot.py`: Un Honeypot asincrono multi-protocollo che traccia e logga le connessioni anomale e i payload degli attaccanti in tempo reale.
*   `cybersecurity/ransomware_detector.py`: Sensore euristico per la protezione degli endpoint. Calcola continuamente l'entropia di Shannon sui file per rilevare crittografie anomale tipiche dei ransomware.
*   `cybersecurity/secure_vault.py`: Un vault crittografico che utilizza l'algoritmo AES-256-GCM (Authenticated Encryption with Associated Data) per garantire confidenzialità e integrità dei file.
*   `cybersecurity/password_generator.py`: Generatore di password crittograficamente sicure, perfetto per l'Identity and Access Management.

### 🛠️ Utilities & Ottimizzazione
*   `utils/memory_safe_analyzer.py`: Analizzatore testuale altamente ottimizzato. Utilizza un generatore Python (`yield`) per leggere ed elaborare i file riga per riga, garantendo che la memoria RAM non venga saturata anche con file di enormi dimensioni.
*   `utils/resilient_api_client.py`: Client Web progettato per la resilienza. Include la gestione robusta delle eccezioni (HTTP Error, Timeout, Request Exception) per chiamate API sicure e affidabili.
*   `utils/profiling_decorator.py`: Decoratore personalizzato (`@calcola_tempo`) per misurare e profilare in modo pulito i tempi di esecuzione delle funzioni critiche.

## Installazione

1. Clona questo repository.
2. Assicurati di avere Python 3.x installato.
3. Installa le dipendenze richieste tramite pip:

```bash
pip install -r requirements.txt
```

## Requisiti di Sistema
Gli script sono progettati per operare con il minimo overhead. Sono perfettamente funzionanti su sistemi Windows e Linux, inclusi ambienti con hardware datato o limitato.
