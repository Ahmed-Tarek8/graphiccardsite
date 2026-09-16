from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PID_FILE = ROOT / ".graphiccardsite-server.pid"


def main() -> int:
    if not PID_FILE.exists():
        print("Graphics-card site server is not running.")
        return 0

    pid_text = PID_FILE.read_text(encoding="utf-8").strip()
    if not pid_text.isdigit():
        PID_FILE.unlink(missing_ok=True)
        print("Removed invalid server PID file.")
        return 0

    result = subprocess.run(
        ["taskkill.exe", "/PID", pid_text, "/T", "/F"],
        capture_output=True,
        text=True,
        check=False,
    )
    PID_FILE.unlink(missing_ok=True)

    if result.returncode == 0:
        print("Graphics-card site server stopped.")
        return 0

    print(result.stderr.strip() or "Server process was already stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
