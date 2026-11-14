"""Einmaliger Tidal-Login.

Läuft normalerweise über die GitHub Action „Tidal-Login“: Im Log erscheint ein
Link, den du öffnest und bei Tidal bestätigst. Der Token wird dann im
GitHub-Actions-Cache gespeichert (TOKEN_FILE) und nie im Log angezeigt.

Lokal ohne TOKEN_FILE wird der Refresh-Token stattdessen ausgegeben.
"""

import json
import os

import tidalapi

session = tidalapi.Session()
session.login_oauth_simple(fn_print=lambda s: print(s, flush=True))

token_file = os.environ.get("TOKEN_FILE")
if token_file:
    os.makedirs(os.path.dirname(token_file) or ".", exist_ok=True)
    with open(token_file, "w") as f:
        json.dump({"refresh_token": session.refresh_token}, f)
    print("Login erfolgreich – Token gespeichert.", flush=True)
else:
    print("\nLogin erfolgreich. Dein Refresh-Token (geheim halten!):\n")
    print(session.refresh_token)
