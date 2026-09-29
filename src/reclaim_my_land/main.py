"""Runnable Phase 1 entry point for Reclaim My Land."""

from __future__ import annotations

from pathlib import Path

import pygame

from .core import GameApp, Scene
from .ui import FontManager


class FoundationScene(Scene):
    """Temporary scene proving the renderer and scene manager are connected."""

    def __init__(self, manager, fonts: FontManager) -> None:
        super().__init__(manager)
        self.fonts = fonts
        self.elapsed = 0.0

    def update(self, dt: float) -> None:
        self.elapsed += dt

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((36, 57, 43))
        # Placeholder landscape and protagonist; replace with pixel-art sprites later.
        pygame.draw.rect(surface, (67, 93, 56), (0, 450, 1280, 270))
        pygame.draw.rect(surface, (86, 60, 42), (0, 535, 1280, 185))
        pygame.draw.rect(surface, (232, 184, 103), (604, 366, 72, 118))
        pygame.draw.rect(surface, (55, 47, 43), (614, 330, 52, 44))

        self.fonts.draw(
            surface,
            "เปี๊ยกทวงคืนที่ดิน",
            (640, 90),
            54,
            (255, 231, 164),
            anchor="midtop",
        )
        self.fonts.draw(
            surface,
            "Phase 1 — Scene Manager + UI Foundation",
            (640, 165),
            26,
            (235, 239, 216),
            anchor="midtop",
        )
        hint = "Escape: ออกจากเกม"
        self.fonts.draw(surface, hint, (640, 620), 26, (255, 255, 255), anchor="center")


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    font_path = project_root / "assets" / "fonts" / "PixelThai.ttf"
    fonts = FontManager(font_path)
    app = GameApp(fonts)
    app.run(FoundationScene(app.scenes, fonts))


if __name__ == "__main__":
    main()
