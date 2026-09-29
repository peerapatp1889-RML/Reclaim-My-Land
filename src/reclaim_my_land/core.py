"""Core scene, asset, and audio infrastructure."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .ui import FontManager


class Scene:
    """Base class for a game scene."""

    def __init__(self, manager: "SceneManager") -> None:
        self.manager = manager

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass


class SceneManager:
    """Owns the active scene and performs safe, explicit scene changes."""

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.current: Scene | None = None

    def change_scene(self, next_scene: Scene) -> None:
        if self.current is not None:
            self.current.on_exit()
        self.current = next_scene
        self.current.on_enter()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.current is not None:
            self.current.handle_event(event)

    def update(self, dt: float) -> None:
        if self.current is not None:
            self.current.update(dt)

    def draw(self) -> None:
        if self.current is not None:
            self.current.draw(self.surface)


class AssetManager:
    """Loads and caches images; scaled pixel art uses nearest-neighbor sampling."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self._images: dict[Path, pygame.Surface] = {}

    def image(self, relative_path: str | Path, *, alpha: bool = True) -> pygame.Surface:
        path = (self.root / relative_path).resolve()
        if path not in self._images:
            loaded = pygame.image.load(str(path))
            self._images[path] = loaded.convert_alpha() if alpha else loaded.convert()
        return self._images[path]

    def scaled_image(
        self, relative_path: str | Path, size: tuple[int, int], *, alpha: bool = True
    ) -> pygame.Surface:
        return pygame.transform.scale(self.image(relative_path, alpha=alpha), size)


class AudioManager:
    """Small mixer wrapper that remains safe when audio hardware is unavailable."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.music_volume = 0.65
        self.sfx_volume = 0.8
        self.enabled = pygame.mixer.get_init() is not None

    def play_music(self, relative_path: str | Path, *, loops: int = -1) -> None:
        if not self.enabled:
            return
        path = self.root / relative_path
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loops)

    def play_sfx(self, relative_path: str | Path) -> None:
        if not self.enabled:
            return
        sound = pygame.mixer.Sound(str(self.root / relative_path))
        sound.set_volume(self.sfx_volume)
        sound.play()

    def set_music_volume(self, value: float) -> None:
        self.music_volume = max(0.0, min(1.0, value))
        if self.enabled:
            pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, value: float) -> None:
        self.sfx_volume = max(0.0, min(1.0, value))


class GameApp:
    """Owns the SDL window, logical canvas, and main game loop."""

    SIZE = (1280, 720)
    TITLE = "Reclaim My Land | เปี๊ยกทวงคืนที่ดิน"

    def __init__(self, font_manager: "FontManager") -> None:
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.window = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption(self.TITLE)
        self.canvas = pygame.Surface(self.SIZE).convert()
        self.clock = pygame.time.Clock()
        self.running = True

        self.project_root = Path(__file__).resolve().parents[2]
        self.assets = AssetManager(self.project_root / "assets")
        self.audio = AudioManager(self.project_root / "assets" / "audio")
        self.fonts = font_manager
        self.scenes = SceneManager(self.canvas)

    def run(self, initial_scene: Scene) -> None:
        self.scenes.change_scene(initial_scene)
        while self.running:
            dt = min(self.clock.tick(60) / 1000.0, 0.05)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    self.scenes.handle_event(event)

            self.scenes.update(dt)
            self.scenes.draw()
            # pygame.transform.scale provides nearest-neighbor pixel scaling if resized.
            pygame.display.flip()

        pygame.quit()
