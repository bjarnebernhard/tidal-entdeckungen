"""Exportiert Tidal-Playlists als Textdatei ("Artist – Titel"), damit Claude
sie als Geschmacksvorlage für die täglichen Entdeckungen lesen kann.

Umgebungsvariablen:
  EXPORT_PLAYLISTS  Komma-getrennt: "datei.txt=playlist-uuid,..."
                    (Standard: songs/rotation.txt = Playlist „Rotation“)
  TIDAL_REFRESH_TOKEN / TOKEN_FILE  wie bei tidal_sync.py
"""

import datetime
import os

from tidal_sync import login

DEFAULT = "songs/rotation.txt=f4fee4c3-9585-4238-b4c4-44963b67859e"


def export(session, uuid: str, path: str) -> None:
    playlist = session.playlist(uuid)
    lines, offset = [], 0
    while True:
        batch = playlist.tracks(limit=100, offset=offset)
        if not batch:
            break
        for track in batch:
            artists = " & ".join(a.name for a in (track.artists or [track.artist]))
            lines.append(f"{artists} – {track.name}")
        offset += len(batch)
        if len(batch) < 100:
            break
    today = datetime.date.today().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Tidal-Playlist „{playlist.name}“ (Stand {today}, {len(lines)} Songs)\n")
        f.write("\n".join(lines) + "\n")
    print(f"{len(lines)} Songs aus '{playlist.name}' nach {path} geschrieben.")


def main() -> None:
    session = login()
    for entry in os.environ.get("EXPORT_PLAYLISTS", DEFAULT).split(","):
        path, uuid = (p.strip() for p in entry.split("=", 1))
        try:
            export(session, uuid, path)
        except Exception as e:  # eine kaputte Playlist soll den Rest nicht stoppen
            print(f"Export von {uuid} fehlgeschlagen: {e}")


if __name__ == "__main__":
    main()
