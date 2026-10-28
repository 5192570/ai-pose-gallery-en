#!/usr/bin/env python3
"""Run the gallery locally and open it in the default browser."""

from __future__ import annotations

import http.server
import socket
import sys
import threading
import webbrowser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HOST = "127.0.0.1"
PORT_START = 8000
PORT_END = 8010


class QuietServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> int:
    handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(
        *args, directory=str(ROOT), **kwargs
    )

    server = None
    for port in range(PORT_START, PORT_END + 1):
        try:
            server = QuietServer((HOST, port), handler)
            break
        except OSError:
            continue

    if server is None:
        print(
            f"Could not find an available port between {PORT_START} and {PORT_END}.",
            file=sys.stderr,
        )
        return 1

    url = f"http://{HOST}:{server.server_address[1]}/"
    print("AI Pose Gallery local server")
    print(f"Serving project files from: {ROOT}")
    print(f"Open in your browser: {url}")
    print("Keep this window open while using the gallery. Press Ctrl+C to stop.\n")

    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping local server...")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
