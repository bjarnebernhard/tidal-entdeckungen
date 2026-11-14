# Tidal-Entdeckungen

Claude schreibt jede Nacht neue Song-Empfehlungen nach `songs/latest.txt`.
Ein Push auf diese Datei startet die GitHub Action, die die Songs bei Tidal sucht
und in die Playlist **Tägliche Entdeckungen** schreibt (jeden Tag neu gefüllt).

## Einmalige Einrichtung (geht komplett am Handy)

1. Repo → Actions → „Tidal-Login“ → Run workflow.
2. Den laufenden Job öffnen, im Schritt `python -u login.py` erscheint ein Link
   `link.tidal.com/…` – öffnen und bei Tidal bestätigen (innerhalb von 5 Minuten).
3. Fertig: Der Login liegt im Actions-Cache und wird bei jedem Lauf erneuert.
   Läuft 7 Tage lang nichts, verfällt er – dann Schritt 1–2 wiederholen.

## Einstellungen (in `.github/workflows/tidal-sync.yml`)

- `PLAYLIST_NAME`: Name der Playlist
- `MODE`: `replace` (eine Playlist, täglich neu gefüllt) oder `new` (jeden Tag eine neue Playlist mit Datum)

## Alternativ auf Android (Termux)

```
pkg install python git
pip install tidalapi
git clone https://github.com/bjarnebernhard/tidal-entdeckungen
cd tidal-entdeckungen && python login.py
# täglich: git pull && TIDAL_REFRESH_TOKEN=... python tidal_sync.py
```
Akku-Optimierung für Termux abschalten und `termux-wake-lock` nutzen.
