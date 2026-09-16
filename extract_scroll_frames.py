from pathlib import Path
import json
import subprocess
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent
FRAMES_ROOT = ROOT / "frames"
FRAMES_ROOT.mkdir(exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 24
WIDTH = 1280
manifest = {}

for index in range(1, 4):
    source = ROOT / f"{index}.mp4"
    target_dir = FRAMES_ROOT / str(index)
    target_dir.mkdir(parents=True, exist_ok=True)

    for old_frame in target_dir.glob("*.jpg"):
        old_frame.unlink()

    output_pattern = target_dir / "%04d.jpg"
    command = [
        FFMPEG,
        "-y",
        "-hide_banner",
        "-loglevel", "warning",
        "-i", str(source),
        "-vf", f"fps={FPS},scale={WIDTH}:-2:flags=lanczos",
        "-q:v", "4",
        "-start_number", "0",
        str(output_pattern),
    ]

    print(f"Extracting {source.name}...", flush=True)
    subprocess.run(command, check=True)

    generated = sorted(target_dir.glob("*.jpg"))
    manifest[str(index)] = {
        "count": len(generated),
        "fps": FPS,
        "width": WIDTH,
        "pattern": f"./frames/{index}/{{frame}}.jpg",
    }
    print(f"Scene {index}: {len(generated)} frames", flush=True)

(ROOT / "frames-manifest.json").write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8",
)
print("GPU frame extraction complete.")
