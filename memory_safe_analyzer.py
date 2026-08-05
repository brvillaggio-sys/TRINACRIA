import re
from collections import Counter
from typing import Generator

def estrai_parole(percorso_file: str) -> Generator[str, None, None]:
    """Generatore che legge un file riga per riga per non saturare la RAM."""
    pattern = re.compile(r'\b[a-zA-Zà-ùÀ-Ù]+\b')
    
    with open(percorso_file, 'r', encoding='utf-8') as file:
        for riga in file:
            # yield restituisce una parola alla volta, mettendo in pausa la funzione
            for parola in pattern.findall(riga):
                yield parola.lower()

def analizza_frequenze(percorso_file: str, top_n: int = 5) -> None:
    """Conta le parole più frequenti in un file di testo."""
    try:
        # Passiamo il generatore direttamente al Counter
        contatore = Counter(estrai_parole(percorso_file))
        
        print(f"Le {top_n} parole più frequenti:")
        for parola, frequenza in contatore.most_common(top_n):
            print(f"- '{parola}': {frequenza} volte")
            
    except FileNotFoundError:
        print("Errore: Il file specificato non è stato trovato.")

# Esempio d'uso:
# analizza_frequenze("Divina_Commedia.txt", 10)
