"""Window chrome in the style of VS Code: a side bar and a status bar."""

from __future__ import annotations

from typing import TYPE_CHECKING

import arcade
from pyglet.graphics import Batch

from mesarcade import styles

if TYPE_CHECKING:
    from mesarcade.renderer import Renderer


class Chrome:
    """Draws the side bar behind the controls and the status bar at the bottom.

    The status bar shows the simulation state, the current tick and the frame
    rate.
    """

    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer
        self.width = renderer.window_width
        self.height = renderer.window_height

        self.sidebar_width = round(renderer.atomic_width * 8.6)
        self.status_height = round(renderer.atomic_height * 1.1)

        self.text_batch = Batch()
        font_size = renderer.font_size * 0.8
        center_y = self.status_height / 2
        padding = renderer.atomic_width * 0.5

        def status_text(x, anchor_x="left"):
            return renderer.text_layer.text(
                text="",
                x=x,
                y=center_y,
                font_size=font_size,
                color=styles.TEXT_MUTED,
                batch=self.text_batch,
                anchor_x=anchor_x,
                anchor_y="cap_center",
            )

        self.state_text = status_text(padding)
        self.tick_text = status_text(padding + renderer.atomic_width * 3.5)
        self.fps_text = status_text(self.width - padding, anchor_x="right")
        self.model_text = status_text(self.width - padding - renderer.atomic_width * 4.5, "right")
        self.model_text.text = renderer.model_class.__name__

    def update_status(self) -> None:
        r = self.renderer
        self.tick_text.text = f"Tick {r.tick}"
        self.fps_text.text = f"FPS {int(arcade.get_fps(60))} / {r.target_fps}"

    def draw(self) -> None:
        running = self.renderer.play

        # side bar
        arcade.draw_lbwh_rectangle_filled(
            0, self.status_height, self.sidebar_width, self.height, styles.SIDEBAR
        )
        arcade.draw_line(
            self.sidebar_width,
            self.status_height,
            self.sidebar_width,
            self.height,
            styles.BORDER,
            1,
        )

        # status bar
        arcade.draw_lbwh_rectangle_filled(0, 0, self.width, self.status_height, styles.SIDEBAR)
        arcade.draw_line(0, self.status_height, self.width, self.status_height, styles.BORDER, 1)

        self.state_text.text = "▶  Running" if running else "■  Paused"
