# Tidal-Entdeckungen

Claude schreibt jede Nacht neue Song-Empfehlungen nach `songs/latest.txt`.
Ein Push auf diese Datei startet die GitHub Action, die die Songs bei Tidal sucht
und in die Playlist **Tägliche Entdeckungen** schreibt (jeden Tag neu gefüllt).

## Einmalige Einrichtung

1. Lokal (PC oder Termux): `pip install tidalapi` und `python login.py`.
   Den angezeigten Link öffnen, bei Tidal bestätigen, den ausgegebenen Token kopieren.
2. Auf GitHub: Repo → Settings → Secrets and variables → Actions → New repository secret
   - Name: `TIDAL_REFRESH_TOKEN`, Wert: der kopierte Token.
3. Testen: Actions → „Tidal-Playlist aktualisieren“ → Run workflow.

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
