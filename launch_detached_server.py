from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path

HOST = "127.0.0.1"
PORT = 4181
ROOT = Path(__file__).resolve().parent
PYTHONW = ROOT / ".venv" / "Scripts" / "pythonw.exe"
SERVER_SCRIPT = ROOT / "persistent_server.py"


def port_is_open() -> bool:
    try:
        with socket.create_connection((HOST, PORT), timeout=0.3):
            return True
    except OSError:
        return False


def start_detached() -> None:
    if not PYTHONW.exists():
        raise FileNotFoundError(f"Missing Python runtime: {PYTHONW}")
    if not SERVER_SCRIPT.exists():
        raise FileNotFoundError(f"Missing server script: {SERVER_SCRIPT}")

    flags = (
        subprocess.DETACHED_PROCESS
        | subprocess.CREATE_NEW_PROCESS_GROUP
        | subprocess.CREATE_NO_WINDOW
    )

    # CREATE_BREAKAWAY_FROM_JOB lets the child survive when an MCP-managed
    # parent process is cleaned up. Some Windows job configurations reject it,
    # so retry without that flag if needed.
    breakaway_flag = getattr(subprocess, "CREATE_BREAKAWAY_FROM_JOB", 0x01000000)

    kwargs = {
        "cwd": str(ROOT),
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "close_fds": True,
    }

    try:
        subprocess.Popen(
            [str(PYTHONW), str(SERVER_SCRIPT)],
            creationflags=flags | breakaway_flag,
            **kwargs,
        )
    except OSError:
        subprocess.Popen(
            [str(PYTHONW), str(SERVER_SCRIPT)],
            creationflags=flags,
            **kwargs,
        )


def main() -> int:
    if not port_is_open():
        start_detached()

    for _ in range(40):
        if port_is_open():
            print(f"http://localhost:{PORT}/")
            return 0
        time.sleep(0.15)

    print("Detached server did not become reachable.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
