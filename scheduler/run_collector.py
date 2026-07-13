"""
Crypto Dashboard - Automatischer Daten-Collector
Wird vom Windows Task Scheduler alle 6 Stunden aufgerufen.
Startet Flask, wartet bis er bereit ist, ruft /coin auf, stoppt Flask.
"""

import subprocess
import requests
import logging
import os
import time

LOG_FILE = os.path.join(os.path.dirname(__file__), "collector.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

PYTHON_EXE = r"C:\Users\BousainaGhadhab\crypto_venv\Scripts\python.exe"
APP_PY = r"C:\Users\BousainaGhadhab\crypto-dashboard-powerbi\app.py"
FLASK_URL = "http://127.0.0.1:8081/coin"


def warte_auf_flask(max_sekunden=30):
    for _ in range(max_sekunden):
        try:
            requests.get("http://127.0.0.1:8081/status", timeout=2)
            return True
        except Exception:
            time.sleep(1)
    return False


def collect():
    logging.info("=== Starte Collector-Lauf ===")
    logging.info("Starte Flask...")
    flask_prozess = subprocess.Popen(
        [PYTHON_EXE, APP_PY],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if not warte_auf_flask():
        logging.error("Flask hat nicht geantwortet - Abbruch.")
        flask_prozess.terminate()
        return
    logging.info("Flask bereit. Starte Datenabholung...")
    try:
        response = requests.get(FLASK_URL, timeout=1800)
        data = response.json()
        logging.info(
            f"Erfolgreich: {data.get('coins_abgerufen')} Coins abgerufen, "
            f"{data.get('db_fehler')} DB-Fehler."
        )
    except Exception as e:
        logging.error(f"Fehler beim Abruf: {e}")
    finally:
        logging.info("Stoppe Flask...")
        flask_prozess.terminate()
        flask_prozess.wait()
        logging.info("=== Collector-Lauf beendet ===")


if __name__ == "__main__":
    collect()
