# Graphic Card Scroll Experience — Handoff

## Project boundary

This project is independent from `berrysite`.

Work only inside:

```text
D:\ChatGPT_Workspace\graphiccardsite
```

Do not copy the berry site's UI into this project. Only the frame-sequence engine architecture is shared.

## Current experience

Three source videos form one continuous scroll-controlled film:

```text
1.mp4 → graphics card reveal
2.mp4 → graphics card enters the PC
3.mp4 → camera reaches the monitor and rendered landscape
```

Each video is extracted at 24 fps into 120 JPEG frames:

```text
frames/1/0000.jpg ... 0119.jpg
frames/2/0000.jpg ... 0119.jpg
frames/3/0000.jpg ... 0119.jpg
```

Total timeline: 360 frames.

## Core engine rules

The site does not use normal document scrolling and does not seek through MP4 files.

```text
wheel / touch / keyboard input
        ↓
bounded target frame
        ↓
current frame moves one frame at a time
        ↓
Canvas render
```

Preserve these invariants:

1. `html` and `body` remain fixed with `overflow: hidden`.
2. Wheel input directly modifies frame intent.
3. The first frame advances immediately inside the input path.
4. Intermediate frames are displayed in order.
5. `MAX_FRAME_BACKLOG` remains bounded so the visual stops quickly.
6. Only scene 1 blocks startup.
7. The next scene preloads while the current scene is running.
8. Do not replace this with `video.currentTime`, GSAP scrub, native smooth scroll, or ScrollTrigger frame selection.

## Current UI direction — important

The old heavy HUD design was intentionally removed.

The production direction is now:

```text
industrial editorial
+ experimental portfolio typography
+ dark product film
+ restrained acid-green accent
```

The video must remain the hero. The interface should feel like an experimental hardware fashion film, not a cockpit dashboard.

Preserve these visual rules:

- One dominant editorial statement per scene.
- Huge condensed typography, often cropped or outlined.
- Asymmetric composition that changes between scenes.
- Thin lines and edge labels instead of boxed panels.
- Acid green only for sequence tags, active states, progress, and one action.
- Large ghost scene numbers in the background.
- Almost no fake telemetry or decorative specifications.
- Scene 3 becomes the cleanest scene so the landscape dominates.
- No rounded SaaS cards, soft gradient dashboards, glassmorphism, or generic gamer HUDs.

Current scene compositions:

```text
Scene 1 — left editorial stack
FORGED / TO BREAK / LIMITS.

Scene 2 — right editorial stack
LOCKED / IN.

Scene 3 — lower-left editorial stack
UNFRAME / REALITY.
```

See:

```text
docs/UI_DIRECTION.md
```

## Main files

- `index.html` — editorial scene structure and minimal navigation.
- `styles.css` — complete industrial editorial visual system.
- `script.js` — direct input-to-frame Canvas engine.
- `extract_scroll_frames.py` — regenerates frame sequences.
- `frames-manifest.json` — runtime frame counts.
- `START_GRAPHICCARD_SITE.cmd` — persistent local launcher.
- `STOP_GRAPHICCARD_SITE.cmd` — stops the detached server.

## Current tuning

```text
FRAMES_PER_PIXEL        0.03
MAX_FRAME_BACKLOG       10
KEYBOARD_FRAMES          5
TOUCH_FRAMES_PER_PIXEL  0.08
NEXT PRELOAD POINT       32%
CANVAS DPR CAP           1.35
CANVAS WIDTH CAP         1600 px
LOCAL PORT               4181
```

## Canvas framing

The renderer uses a near-cover cinematic fit rather than aggressive cover cropping:

```js
const scale = Math.max(containScale, coverScale * 0.96);
```

Do not re-add CSS zoom on the canvas unless the user explicitly asks for it. The previous zoom made the footage feel overly cropped.

## Regenerating frames

From this project folder:

```powershell
.venv\Scripts\python.exe extract_scroll_frames.py
```

If the virtual environment is missing:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install imageio-ffmpeg
.venv\Scripts\python.exe extract_scroll_frames.py
```

## Running locally

Double-click:

```text
START_GRAPHICCARD_SITE.cmd
```

Open:

```text
http://localhost:4181
```

Stop with:

```text
STOP_GRAPHICCARD_SITE.cmd
```

Opening `index.html` through `file://` will not work because the site fetches the manifest and frame files.

## Acceptance checks

Before claiming success:

- Scene 1 loads before the boot overlay disappears.
- Wheel down advances visible frames immediately.
- Wheel up reverses frames immediately.
- A multi-frame input passes through every intermediate frame.
- The sequence indicator changes at scene boundaries.
- Scene 2 and scene 3 load before they are reached during normal use.
- Navigation nodes jump to all three scenes.
- Replay returns to the first frame.
- No page errors or failed frame requests appear.
- `window.scrollY` remains zero.
- The UI remains sparse and does not cover the product unnecessarily.
