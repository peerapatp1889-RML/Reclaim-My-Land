"""Reusable pixel-friendly UI and Thai text rendering helpers."""

from __future__ import annotations

from pathlib import Path

import pygame


class FontManager:
    """Caches Pygame fonts and renders Thai-capable TTF text."""

    def __init__(self, font_path: str | Path | None = None) -> None:
        pygame.font.init()
        self.font_path = Path(font_path) if font_path else None
        self._cache: dict[int, pygame.font.Font] = {}

    def get(self, size: int) -> pygame.font.Font:
        size = max(8, int(size))
        if size not in self._cache:
            path = self.font_path if self.font_path and self.font_path.is_file() else None
            if path is None:
                candidates = (
                    Path("C:/Windows/Fonts/tahoma.ttf"),
                    Path("C:/Windows/Fonts/angsana.ttc"),
                )
                path = next((candidate for candidate in candidates if candidate.is_file()), None)
            self._cache[size] = pygame.font.Font(str(path) if path else None, size)
        return self._cache[size]

    def render(
        self,
        text: str,
        size: int,
        color: pygame.Color | tuple[int, int, int] = (255, 255, 255),
        *,
        antialias: bool = False,
    ) -> pygame.Surface:
        return self.get(size).render(text, antialias, color)

    def draw(
        self,
        surface: pygame.Surface,
        text: str,
        position: tuple[int, int],
        size: int,
        color: pygame.Color | tuple[int, int, int] = (255, 255, 255),
        *,
        anchor: str = "topleft",
        antialias: bool = False,
    ) -> pygame.Rect:
        rendered = self.render(text, size, color, antialias=antialias)
        rect = rendered.get_rect(**{anchor: position})
        surface.blit(rendered, rect)
        return rect


class PixelButton:
    """Rectangle button with a chunky pixel border and hover state."""

    def __init__(
        self,
        rect: pygame.Rect,
        label: str,
        fonts: FontManager,
        *,
        font_size: int = 30,
        fill: tuple[int, int, int] = (80, 112, 63),
        hover_fill: tuple[int, int, int] = (111, 151, 78),
        border: tuple[int, int, int] = (232, 210, 145),
    ) -> None:
        self.rect = pygame.Rect(rect)
        self.label = label
        self.fonts = fonts
        self.font_size = font_size
        self.fill = fill
        self.hover_fill = hover_fill
        self.border = border
        self.hovered = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.border, self.rect)
        inner = self.rect.inflate(-6, -6)
        pygame.draw.rect(surface, self.hover_fill if self.hovered else self.fill, inner)
        self.fonts.draw(
            surface,
            self.label,
            self.rect.center,
            self.font_size,
            (255, 246, 210),
            anchor="center",
        )


class DialogueBox:
    """Dark translucent textbox with a crisp pixel-art border."""

    def __init__(self, rect: pygame.Rect, fonts: FontManager) -> None:
        self.rect = pygame.Rect(rect)
        self.fonts = fonts
        self.padding = 24

    def draw(self, surface: pygame.Surface, lines: list[str]) -> None:
        panel = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        panel.fill((13, 20, 17, 225))
        surface.blit(panel, self.rect.topleft)
        pygame.draw.rect(surface, (232, 210, 145), self.rect, width=4)
        pygame.draw.rect(surface, (99, 75, 45), self.rect.inflate(-12, -12), width=2)
        line_height = 38
        for index, line in enumerate(lines):
            self.fonts.draw(
                surface,
                line,
                (self.rect.left + self.padding, self.rect.top + self.padding + index * line_height),
                28,
                (255, 248, 220),
            )
