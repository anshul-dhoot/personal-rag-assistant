"""
keepalive.py
Wakes the deployed Streamlit app by hitting the URL.
Runs daily via GitHub Actions to prevent Streamlit Community Cloud sleep.

Any HTTP response (including redirects and wake-up pages) counts as success.
Only fails if the URL is completely unreachable.
"""

import urllib.request
import urllib.error
import sys
from datetime import datetime

APP_URL = "https://personal-rag-assistant-6zivofchzgcvpvsddenfxn.streamlit.app"


def ping_app(url: str) -> bool:
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,*/*",
            }
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            status = response.getcode()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Response: {status} — OK")
            return True
    except urllib.error.HTTPError as e:
        # Any HTTP response means server is alive — count as success
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] HTTP {e.code} — app reachable, keepalive OK")
        return True
    except urllib.error.URLError as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] URL error: {e.reason} — app unreachable")
        return False
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error: {e}")
        return False


if __name__ == "__main__":
    print(f"Pinging {APP_URL} ...")
    success = ping_app(APP_URL)
    if success:
        print("Keepalive complete.")
        sys.exit(0)
    else:
        print("App unreachable — keepalive failed.")
        sys.exit(1)
