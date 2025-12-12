#!/usr/bin/env python3
import http.server
import socketserver
import threading
import webbrowser
import os
import sys
from pathlib import Path

PORT = 8000
SITE_DIR_NAME = "html"

def get_site_root() -> Path:
    """
    Return the directory that contains the website (USB_ROOT/html).
    Works for both .py and PyInstaller .exe.
    """
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).resolve().parent
    else:
        base = Path(__file__).resolve().parent

    site_root = base / SITE_DIR_NAME
    if not site_root.exists():
        raise FileNotFoundError(f"Site directory not found: {site_root}")

    return site_root

def run_server(site_root: Path):
    os.chdir(site_root)
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"Serving {site_root}")
        print(f"http://127.0.0.1:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

def main():
    try:
        site_root = get_site_root()
    except Exception as e:
        print(f"ERROR: {e}")
        input("Press Enter to exit...")
        return

    thread = threading.Thread(
        target=run_server,
        args=(site_root,),
        daemon=True
    )
    thread.start()

    url = f"http://127.0.0.1:{PORT}/index.html"
    webbrowser.open(url)

    input("Press Enter to stop the server and exit...")

if __name__ == "__main__":
    main()
