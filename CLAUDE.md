# ziforge.github.io — Portfolio Site

## Project Overview

Personal portfolio site for George Howard Redpath (Ziforge). Dark-themed, single-page site showcasing FPGA audio engineering, DSP research, physical modeling synthesis, and instrument design projects.

**Live URL (when public):** https://ziforge.github.io

## Current State

The site is functional with 31+ project cards, interactive background animation, and physically modeled audio synthesis. It needs visual polish and testing before going public.

## Architecture

Single-page static site — no build tools, no frameworks. Three files:

- **`index.html`** — All content + inline `<script>` for the background animation and audio system (~350 lines of inline JS at the top)
- **`style.css`** — Full styling, dark theme with CSS custom properties
- **`main.js`** — UI effects (scroll reveal, nav, card hover effects, terminal decode animation, etc.). The background animation is NOT in this file — it's inline in index.html.
- **`diagrams/`** — SVG + PNG technical diagrams for each project card
- **`images/`** — Photos
- **`test-canvas.html`** — Debug file, can be deleted

## Design System

- **Colors:** Amber `#e8a835` (primary/accent), Cyan `#5bc0be` (secondary), near-black `#0a0a0a` background
- **Font:** JetBrains Mono (headings/code), Inter (body)
- **Aesthetic:** Terminal/hacker feel with monospace text, subtle animations

## Background Animation System (inline script in index.html)

### Boid Flocking
- 350 glowing particle boids with separation, alignment, cohesion
- Mouse attraction (boids follow cursor)
- Edge avoidance keeps boids on screen
- Smooth quadratic Bezier trail rendering
- Particles glow brighter when "singing"

### Audio Synthesis (Web Audio API)
Ported from the Verdant Drift Godot project (`/Volumes/MAC_M3_Store/Dev/verdant-drift/`):

**Bird calls — Mindlin-Laje syrinx physical model:**
- RK4 integration of coupled nonlinear ODE: `dx/dt = y`, `dy/dt = -ax - bx|x| - x^3 + bg*sign(x)*y^2`
- 5 species: blackbird (2200Hz), great tit (4500Hz), wren (5500Hz), robin (3800Hz), wood pigeon (500Hz)
- Each species has alpha/beta motor gesture functions that trace through parameter space
- Single labium, velocity (y) output, gamma=0.15
- Pre-generated AudioBuffers with peak normalization to 0.5
- FM chirp fallback if model produces silence

**Cricket calls — Insect stridulation model:**
- Tooth-strike impulse train (4 pulses per chirp, bell-curve amplitude)
- Wing membrane bandpass resonator (biquad filter, ~4500Hz, Q=25)
- Chirp envelope via sin(t/dur * PI)

**Audio triggers:**
- Bird calls every 3-8 seconds from random boids
- Cricket chirps every 2-4 seconds
- Mouse proximity triggers (boid near cursor may call)
- Stereo panning based on boid X position
- Mute toggle button (bottom-right speaker icon)

### Visual Sound Indicators
- When a bird calls: boid pulses with expanding aura for ~90 frames
- 3 concentric expanding ring "sound waves" emanate from calling boid
- Cricket chirps show smaller cyan rings near bottom of screen

## Critical CSS Z-Index Notes

Canvas visibility was extensively debugged. The ONLY working configuration:

```
#bg-canvas     { z-index: 2; pointer-events: none; opacity: 0.7; }
.container     { z-index: 5; }
section > .container { background: rgba(10,10,10,0.85); }
```

z-index 0, -1, and 1 on the canvas are ALL invisible on this page. Suspected cause: `body { overflow-x: hidden; }` creates stacking context issues. **Do not change these z-index values.**

## AudioContext Autoplay Policy

Chrome requires a "user activation" (click, keydown) to resume an AudioContext. `mousemove` does NOT count. The current code:
- Registers click listener (no `{once:true}`) that always tries `audioCtx.resume()`
- The mute toggle does NOT call `stopPropagation()` so clicks bubble up to resume
- AudioContext is created on first click, buffers are pre-generated immediately

## What Needs Work

1. **Visual upgrade** — User wants "something better than boids" with sound indicators. Current iteration has glowing particles + sound wave rings but hasn't been fully tested/reviewed yet
2. **Test and iterate on visuals** — Hard refresh (Ctrl+Shift+R), click page to init audio, verify particles + rings + audio all work
3. **Clean up** — Delete `test-canvas.html`, remove commented-out `initBackground` in `main.js`
4. **Content review** — Check all 31 project card descriptions for accuracy
5. **Responsive testing** — Mobile layout, touch events for audio init
6. **Performance** — 350 boids with O(n^2) flocking may need spatial hashing on slower devices
7. **Deploy** — When ready, switch repo back to public for GitHub Pages

## Source Models (for reference)

The bird and cricket synthesis was ported from Verdant Drift (Godot game):
- Bird syrinx: `verdant-drift/scripts/audio/physical_models/mindlin_syrinx_model.gd`
- Cricket: `verdant-drift/scripts/audio/physical_models/insect_stridulation_model.gd`
- Alternative bird model with trachea waveguide: `verdant-drift/scripts/audio/physical_models/bird_syrinx_model.gd`
