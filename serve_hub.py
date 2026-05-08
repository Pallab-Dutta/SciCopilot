from __future__ import annotations

import http.server
import socketserver
import webbrowser
from pathlib import Path


HOST = "127.0.0.1"
PORT = 8000
ROOT = Path(__file__).resolve().parent


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    handler = http.server.SimpleHTTPRequestHandler

    with ReusableTCPServer((HOST, PORT), handler) as httpd:
        url = f"http://{HOST}:{PORT}/index.html"
        print(f"SciCopilot hub is available at {url}")
        print("Press Ctrl+C to stop the server.")
        webbrowser.open(url)
        httpd.serve_forever()


if __name__ == "__main__":
    import os

    os.chdir(ROOT)
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped.")
