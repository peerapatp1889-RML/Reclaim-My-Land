# Reclaim My Land — เปี๊ยกทวงคืนที่ดิน

A 2D pixel-art game built with Python and Pygame. This repository is being developed in phases.

## Phase 1

The current foundation includes a 1280×720 game loop, scene manager, Thai text/font helper, pixel-style UI primitives, and image/audio loading helpers. Gameplay scenes will be added in the next phases.

## Run

```bash
python -m pip install -r requirements.txt
python -m src.reclaim_my_land.main
```

Place a Thai-capable pixel font at `assets/fonts/PixelThai.ttf`. Pygame uses the font glyph metrics for Thai mark placement, so the selected font determines how clearly vowels and tone marks render.

Press Escape to close the Phase 1 foundation scene.
