"""Schreibt die tägliche Songliste (songs/latest.txt) in eine Tidal-Playlist.

Benötigt die Umgebungsvariable TIDAL_REFRESH_TOKEN (einmalig mit login.py holen).
Optional:
  PLAYLIST_NAME  Name der Playlist (Standard: "Tägliche Entdeckungen")
  MODE           "replace" = feste Playlist jeden Tag neu füllen (Standard)
                 "new"     = jeden Tag eine neue Playlist mit Datum anlegen
  SONG_FILE      Pfad zur Songliste (Standard: songs/latest.txt)
"""

import datetime
import difflib
import json
import os
import re
import sys

import tidalapi

PLAYLIST_NAME = os.environ.get("PLAYLIST_NAME", "Tägliche Entdeckungen")
MODE = os.environ.get("MODE", "replace")
SONG_FILE = os.environ.get("SONG_FILE", "songs/latest.txt")


def login() -> tidalapi.Session:
    refresh_token = os.environ.get("TIDAL_REFRESH_TOKEN")
    token_file = os.environ.get("TOKEN_FILE")
    if not refresh_token and token_file and os.path.exists(token_file):
        with open(token_file) as f:
            refresh_token = json.load(f).get("refresh_token")
    if not refresh_token:
        sys.exit("Kein Tidal-Login gefunden – erst die Action „Tidal-Login“ ausführen.")
    session = tidalapi.Session()
    if not session.token_refresh(refresh_token):
        sys.exit("Refresh-Token abgelaufen – login.py erneut ausführen.")
    if not session.load_oauth_session(
        session.token_type, session.access_token, refresh_token, session.expiry_time
    ):
        sys.exit("Tidal-Login fehlgeschlagen.")
    return session


def read_songs(path: str) -> list[tuple[str, str]]:
    songs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line = re.sub(r"^\d+[.)]\s*", "", line)  # "1. " entfernen
            parts = re.split(r"\s+[–—-]\s+", line, maxsplit=1)
            if len(parts) == 2:
                songs.append((parts[0].strip(), parts[1].strip()))
            else:
                print(f"Übersprungen (Format 'Artist – Titel' erwartet): {line}")
    return songs


def similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_track(session: tidalapi.Session, artist: str, title: str):
    results = session.search(f"{artist} {title}", models=[tidalapi.Track], limit=10)
    best, best_score = None, 0.0
    for track in results.get("tracks", []):
        artist_names = " ".join(a.name for a in (track.artists or [track.artist]))
        score = similar(artist, artist_names) + similar(title, track.name)
        if score > best_score:
            best, best_score = track, score
    # Mindestens grob passender Artist + Titel, sonst lieber weglassen
    return best if best_score >= 1.1 else None


def get_playlist(session: tidalapi.Session, name: str, description: str):
    for pl in session.user.playlists():
        if isinstance(pl, tidalapi.UserPlaylist) and pl.name == name:
            return pl
    return session.user.create_playlist(name, description)


def main() -> None:
    songs = read_songs(SONG_FILE)
    if not songs:
        sys.exit("Keine Songs in der Liste gefunden.")

    session = login()
    today = datetime.date.today().isoformat()

    track_ids, missing = [], []
    for artist, title in songs:
        track = find_track(session, artist, title)
        if track:
            track_ids.append(str(track.id))
            print(f"✔ {artist} – {title}  →  {track.artist.name} – {track.name}")
        else:
            missing.append(f"{artist} – {title}")
            print(f"✘ Nicht auf Tidal gefunden: {artist} – {title}")

    if not track_ids:
        sys.exit("Kein einziger Song gefunden – Playlist bleibt unverändert.")

    description = f"Neue Entdeckungen vom {today}"
    if MODE == "new":
        playlist = session.user.create_playlist(f"Entdeckungen {today}", description)
    else:
        playlist = get_playlist(session, PLAYLIST_NAME, description)
        if playlist.num_tracks:
            playlist.clear()
        playlist = session.playlist(playlist.id)  # frischer Stand (ETag)
        playlist.edit(description=description)
        playlist = session.playlist(playlist.id)

    playlist.add(track_ids)
    print(f"\n{len(track_ids)} Songs in '{playlist.name}' geschrieben.")
    if missing:
        print(f"{len(missing)} nicht gefunden: " + "; ".join(missing))


if __name__ == "__main__":
    main()
