# Windows Task Scheduler – Einrichtung (alle 6 Stunden)

## Voraussetzung
Flask muss laufen (Docker + app.py aktiv).

## Schritt-für-Schritt

1. **Windows-Taste** drücken → "Aufgabenplanung" suchen → öffnen

2. Rechts: **"Einfache Aufgabe erstellen..."** klicken

3. **Name:** `Crypto Dashboard Collector`
   **Beschreibung:** `Ruft alle 6h Coin-Daten ab und speichert in MariaDB`

4. **Trigger:** Täglich → Startzeit z.B. `08:00 Uhr`
   → Dann unter "Erweiterte Einstellungen":
   ✅ "Aufgabe alle ... wiederholen" → **6 Stunden**, Dauer: **Unbegrenzt**

5. **Aktion:** Programm starten
   - Programm: `C:\Users\BousainaGhadhab\AppData\Local\Programs\Python\Python3xx\python.exe`
     (deinen echten Python-Pfad prüfen mit: `where python` im Terminal)
   - Argumente: `run_collector.py`
   - Starten in: `C:\Users\BousainaGhadhab\crypto-dashboard-powerbi\scheduler`

6. **Fertigstellen** → ✅ "Eigenschaften öffnen" anklicken
   → Reiter "Bedingungen": 
   ❌ "Nur starten wenn Netzteil" → **deaktivieren**

7. **Testen:** Rechtsklick auf die Aufgabe → **"Ausführen"**
   → Prüfe die Datei: `scheduler/collector.log`

## Log prüfen
```
# Erwartete Ausgabe in collector.log:
2025-07-10 08:00:01 - INFO - Starte Datenabholung...
2025-07-10 08:12:45 - INFO - Erfolgreich: 10000 Coins abgerufen, 0 DB-Fehler.
```
