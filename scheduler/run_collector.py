"""
Crypto Dashboard - Automatischer Daten-Collector
Wird vom Windows Task Scheduler alle 6 Stunden aufgerufen.
Ruft den /coin Endpoint auf und loggt das Ergebnis.
"""

import requests
import logging
import os
from datetime import datetime

# Log-Datei liegt im selben Ordner wie dieses Script
LOG_FILE = os.path.join(os.path.dirname(__file__), "collector.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

FLASK_URL = "http://127.0.0.1:8081/coin"


def collect():
    logging.info("Starte Datenabholung...")
    try:
        response = requests.get(FLASK_URL, timeout=600)  # 10 Min. Timeout (100 Seiten!)
        data = response.json()
        logging.info(
            f"Erfolgreich: {data.get('coins_abgerufen')} Coins abgerufen, "
            f"{data.get('db_fehler')} DB-Fehler."
        )
    except Exception as e:
        logging.error(f"Fehler beim Abruf: {e}")


if __name__ == "__main__":
    collect()
