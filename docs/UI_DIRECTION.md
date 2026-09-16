# VANTA X90 UI Direction

## Design target

The website should feel like an experimental industrial design portfolio built around a graphics card film.

Not an official GPU product page.
Not a cockpit HUD.
Not a SaaS landing page.

The target mix is:

```text
industrial editorial layouts
+ brutalist typography
+ dark product cinematography
+ restrained technical microcopy
+ acid-green punctuation
```

## Visual hierarchy

Every scene follows this order:

1. Video frame.
2. One dominant phrase.
3. One small scene label.
4. One short supporting sentence.
5. Minimal progress and navigation.

Nothing else should compete with the footage.

## Typography

Use condensed, oversized, tightly tracked type.

Approved behavior:

- solid and outlined words overlapping,
- text partially cropped by the viewport,
- large ghost sequence numbers,
- asymmetrical alignment,
- short phrases rather than marketing paragraphs.

Avoid:

- centered generic hero layouts,
- multiple cards and badges,
- long feature lists,
- small dashboard metrics everywhere.

## Color

Primary:

```text
#050505 — black
#f2f2ed — warm white
```

Accent:

```text
#c7ff2f — acid green
```

The accent is punctuation, not a background theme. Use it for:

- active sequence tag,
- progress line,
- active navigation node,
- replay button,
- one or two status words.

## Scene personalities

### Scene 1 — Hardware form

Composition: left-heavy.

Statement:

```text
FORGED
TO BREAK
LIMITS.
```

The card stays visible on the right and center. Supporting specifications are tiny and unboxed.

### Scene 2 — System integration

Composition: right-heavy.

Statement:

```text
LOCKED
IN.
```

Use one fine crosshair and a thin system-status line. No large panels.

### Scene 3 — Visual output

Composition: lower-left.

Statement:

```text
UNFRAME
REALITY.
```

This is the cleanest scene. The landscape must dominate. Keep only the title, one sentence, replay action, and small 8K output mark.

## Motion

The footage is controlled by the direct frame engine.

UI motion should remain secondary:

- scene copy fades and translates into place,
- ghost sequence numbers drift only a few viewport units with scene progress,
- progress lines move directly with frames,
- no delayed parallax system,
- no smooth-scroll layer between input and frame output.

## Protected engine selectors

These selectors and IDs are used by `script.js` and must remain available:

```text
.story-section
.story-canvas
.section-progress i
.rail-node
#activeChapter
#journeyFill
#scrollCue
#replayButton
#sequenceLoader
#loaderPercent
#loaderBar
```

The HTML can be redesigned, but these hooks must be preserved or the runtime must be updated at the same time.

## Rejection checklist

Reject a redesign if it introduces any of the following:

- heavy fake telemetry,
- multiple bordered HUD panels,
- glowing neon on every element,
- rounded cards,
- official-store product-page styling,
- large specification tables inside the film,
- UI that covers the main GPU or landscape,
- native document scrolling,
- MP4 seeking.
