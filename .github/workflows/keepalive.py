"""
keepalive.py
Wakes the deployed Streamlit app by hitting the URL.
Designed to run as a GitHub Actions scheduled job once per day.

This doesn't simulate a full browser session — it sends an HTTP GET
to the app URL which is enough to prevent Streamlit Community Cloud
from marking the app as inactive.

Usage (local test):
    python keepalive.py

GitHub Actions runs this automatically via .github/workflows/keepalive.yml
"""

import urllib.request
import urllib.error
import sys
from datetime import datetime

APP_URL = "https://personal-rag-assistant-6zivofchzgcvpvsddenfxn.streamlit.app"

def ping_app(url: str) -> bool:
    """Send HTTP GET to the app URL. Returns True if app responds."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (keepalive-bot/1.0)",
                "Accept": "text/html",
            }
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            status = response.getcode()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                  f"App responded with status {status} — keepalive OK")
            return True
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    print(f"Pinging {APP_URL} ...")
    success = ping_app(APP_URL)
    sys.exit(0 if success else 1)
