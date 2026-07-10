"""
Crypto Dashboard - Flask API

REST API endpoint that fetches live cryptocurrency market data
from the CoinGecko API and stores it in a MariaDB database.
Historisierung: jeder Abruf wird als neuer Datensatz gespeichert.
"""

import flask
import requests
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = flask.Flask(__name__)


def get_db_connection():
    """Erstellt eine neue DB-Verbindung."""
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )


@app.route("/coin")
def get_coin():
    """
    Fetches live cryptocurrency market data and stores it in the database.
    Jeder Aufruf schreibt einen neuen Historisierungs-Eintrag (collected_at = NOW()).
    """
    db = get_db_connection()
    cursor = db.cursor()
    alle_coins = []
    fehler_count = 0

    for seite in range(1, 101):
        url = (
            f"https://api.coingecko.com/api/v3/coins/markets"
            f"?vs_currency=eur&page={seite}"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            daten = response.json()
        except Exception as e:
            print(f"API Fehler auf Seite {seite}: {e}")
            continue

        if not isinstance(daten, list) or len(daten) == 0:
            print(f"Seite {seite}: Keine Daten mehr – Schleife beendet.")
            break

        print(f"Seite {seite}: {len(daten)} Coins abgerufen.")
        alle_coins.extend(daten)

        for coin in daten:
            coin_sql = """
                INSERT INTO coins (id, symbol, name)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    symbol = VALUES(symbol),
                    name = VALUES(name)
            """

            history_sql = """
                INSERT INTO market_history
                (coin_id, current_price, market_cap_rank, high_24h, low_24h,
                 price_change_24h, total_volume, last_updated, collected_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """

            coin_werte = (
                coin.get("id"),
                coin.get("symbol"),
                coin.get("name"),
            )

            last_updated = coin.get("last_updated")
            if last_updated:
                last_updated = last_updated.replace("T", " ").replace("Z", "")[:19]

            history_werte = (
                coin.get("id"),
                coin.get("current_price"),
                coin.get("market_cap_rank"),
                coin.get("high_24h"),
                coin.get("low_24h"),
                coin.get("price_change_24h"),
                coin.get("total_volume"),
                last_updated,
            )

            try:
                cursor.execute(coin_sql, coin_werte)
                cursor.execute(history_sql, history_werte)
                db.commit()
            except Exception as e:
                db.rollback()
                fehler_count += 1
                print(f"DB Fehler bei {coin.get('id')}: {e}")

    cursor.close()
    db.close()

    return flask.jsonify({
        "status": "ok",
        "coins_abgerufen": len(alle_coins),
        "db_fehler": fehler_count,
    })


@app.route("/status")
def status():
    """Einfacher Health-Check Endpoint."""
    return flask.jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
