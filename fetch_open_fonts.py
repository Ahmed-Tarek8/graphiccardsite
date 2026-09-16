from __future__ import annotations

import shutil
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
CACHE = ROOT / ".font-cache"

SOURCES = {
    "outward": "https://codeload.github.com/raoulaudouin/outward/zip/refs/heads/master",
    "karrik": "https://gitlab.com/phantomfoundry/karrik_fonts/-/archive/main/karrik_fonts-main.zip",
}

FONTS.mkdir(exist_ok=True)
CACHE.mkdir(exist_ok=True)

for name, url in SOURCES.items():
    archive = CACHE / f"{name}.zip"
    extracted = CACHE / name
    if extracted.exists():
        shutil.rmtree(extracted)
    print(f"Downloading {name}...")
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=60) as response, archive.open("wb") as output:
        shutil.copyfileobj(response, output)
    with zipfile.ZipFile(archive) as zip_file:
        zip_file.extractall(extracted)

font_files = []
for extension in ("*.woff2", "*.woff", "*.otf", "*.ttf"):
    font_files.extend(CACHE.rglob(extension))

wanted = {
    "Outward-Block.woff2": ["outward-block", "outwardblock"],
    "Outward-Borders.woff2": ["outward-borders", "outwardborders"],
    "Karrik-Regular.woff2": ["karrik-regular", "karrikregular"],
}

for destination_name, needles in wanted.items():
    matches = [
        path for path in font_files
        if any(needle in path.stem.lower().replace("_", "-") for needle in needles)
    ]
    if not matches:
        print(f"Missing {destination_name}")
        continue
    source = sorted(matches, key=lambda path: (path.suffix.lower() != ".woff2", len(str(path))))[0]
    destination = FONTS / destination_name.replace(".woff2", source.suffix.lower())
    shutil.copy2(source, destination)
    print(f"Copied {source.name} -> {destination.name}")

print("Available font files:")
for path in sorted(FONTS.iterdir()):
    print(path.name)
