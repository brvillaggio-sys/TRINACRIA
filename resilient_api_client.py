import requests
from requests.exceptions import HTTPError, Timeout, RequestException

def ottieni_dati_api(url: str, timeout_sec: int = 5) -> dict | None:
    """Scarica dati JSON da un'API gestendo in modo robusto gli errori di rete."""
    # Usare una sessione migliora le performance se si fanno più chiamate
    with requests.Session() as sessione:
        try:
            # Imposta un header per non sembrare un bot base e un timeout di sicurezza
            headers = {'User-Agent': 'ScriptPython_Studente/1.0'}
            risposta = sessione.get(url, headers=headers, timeout=timeout_sec)
            
            # Solleva un'eccezione se il server risponde con errore (es. 404 o 500)
            risposta.raise_for_status()
            
            return risposta.json()
            
        except Timeout:
            print("Errore: Il server ha impiegato troppo tempo a rispondere.")
        except HTTPError as e:
            print(f"Errore HTTP: {e}")
        except RequestException as e:
            print(f"Errore di connessione generico: {e}")
            
    return None

# Esempio d'uso (API pubblica per avere una barzelletta sui programmatori):
# dati = ottieni_dati_api("https://v2.jokeapi.dev/joke/Programming?type=single")
# se dati:
#     print(dati.get('joke'))
