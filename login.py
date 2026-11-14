"""Einmaliger Tidal-Login. Gibt den Refresh-Token aus, den du als GitHub-Secret
TIDAL_REFRESH_TOKEN speicherst.

    pip install tidalapi
    python login.py
"""

import tidalapi

session = tidalapi.Session()
session.login_oauth_simple()  # zeigt einen Link – öffnen und mit Tidal bestätigen
print("\nLogin erfolgreich. Dein Refresh-Token (geheim halten!):\n")
print(session.refresh_token)
