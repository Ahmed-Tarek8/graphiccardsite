from __future__ import annotations

import os
import sys
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "127.0.0.1"
PORT = 4181
ROOT = Path(__file__).resolve().parent
PID_FILE = ROOT / ".graphiccardsite-server.pid"
LOG_FILE = ROOT / ".graphiccardsite-server.log"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        # Keep the detached process quiet. Fatal startup errors are written below.
        return


class ReusableThreadingHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def write_log(message: str) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


def main() -> int:
    os.chdir(ROOT)
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")

    try:
        server = ReusableThreadingHTTPServer((HOST, PORT), QuietHandler)
    except OSError as exc:
        write_log(f"Failed to bind {HOST}:{PORT}: {exc}")
        PID_FILE.unlink(missing_ok=True)
        return 1

    write_log(f"Server started on http://{HOST}:{PORT} with PID {os.getpid()}")

    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    except Exception as exc:  # noqa: BLE001
        write_log(f"Server crashed: {exc!r}")
        return 1
    finally:
        server.server_close()
        PID_FILE.unlink(missing_ok=True)
        write_log("Server stopped")

    return 0


if __name__ == "__main__":
    sys.exit(main())
