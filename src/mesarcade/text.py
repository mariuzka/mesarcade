"""Crisp text rendering on HiDPI (e.g. Retina) displays.

pyglet rasterizes glyphs in logical pixels. On a display with a pixel ratio of
2, the glyph textures are therefore stretched to twice their size, which makes
all text blurry. The TextLayer renders text at physical resolution instead:
font sizes and positions are multiplied by the pixel ratio, and the text is
drawn with a camera that maps one world unit to one physical pixel.

All public coordinates and font sizes are in logical pixels, just like the rest
of mesarcade.
"""

from __future__ import annotations

import arcade
from arcade.types import LRBT
from pyglet.graphics import Batch

from mesarcade import styles

# Cap height of typical sans-serif fonts relative to the em size. Used to center
# text optically (on the capital letters / digits) instead of on the font box.
CAP_HEIGHT = 0.716
# pyglet converts points to pixels with 96 dpi
PT_TO_PX = 96 / 72


class CrispText:
    """Wrapper around arcade.Text that works in logical coordinates.

    Args:
        anchor_y: Besides pyglet's anchors, "cap_center" places the vertical
            center of the capital letters/digits at y.
    """

    def __init__(
        self,
        layer: TextLayer,
        text: str,
        x: float,
        y: float,
        font_size: float,
        color=None,
        batch: Batch | None = None,
        anchor_x: str = "left",
        anchor_y: str = "baseline",
        bold: bool = False,
        italic: bool = False,
        mono: bool = False,
    ) -> None:
        self.layer = layer
        self.font_size = font_size
        self._cap_center = anchor_y == "cap_center"
        self._x = x
        self._y = y
        self._text = arcade.Text(
            text=str(text),
            x=0,
            y=0,
            color=styles.TEXT if color is None else color,
            font_size=round(font_size * layer.ratio),
            font_name=styles.MONO_FONT_NAME if mono else styles.FONT_NAME,
            bold=bold,
            italic=italic,
            anchor_x=anchor_x,
            anchor_y="baseline" if self._cap_center else anchor_y,
            batch=layer.batch if batch is None else batch,
        )
        self._place()

    def _place(self) -> None:
        r = self.layer.ratio
        y = self._y
        if self._cap_center:
            y -= self.font_size * PT_TO_PX * CAP_HEIGHT / 2
        self._text.position = (round(self._x * r), round(y * r))

    @property
    def text(self) -> str:
        return self._text.text

    @text.setter
    def text(self, value) -> None:
        value = str(value)
        if self._text.text != value:
            self._text.text = value

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value
        self._place()

    @property
    def position(self) -> tuple[float, float]:
        return self._x, self._y

    @position.setter
    def position(self, value: tuple[float, float]) -> None:
        if value != (self._x, self._y):
            self._x, self._y = value
            self._place()

    @property
    def color(self):
        return self._text.color

    @color.setter
    def color(self, value) -> None:
        if tuple(self._text.color) != tuple(value):
            self._text.color = value

    @property
    def visible(self) -> bool:
        return self._text.visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._text.visible = value


class _Caption:
    """Crisp label drawn centered on top of a gui widget.

    The widget keeps its own text (invisible via a transparent font color), so
    that its behaviour and its `text` attribute stay unchanged.
    """

    def __init__(self, layer: TextLayer, widget, font_size: float, color, mono=False) -> None:
        self.widget = widget
        self.crisp_text = CrispText(
            layer,
            text=widget.text,
            x=0,
            y=0,
            font_size=font_size,
            color=color,
            anchor_x="center",
            anchor_y="cap_center",
            mono=mono,
        )

    def sync(self) -> None:
        rect = self.widget.rect
        self.crisp_text.text = self.widget.text
        self.crisp_text.position = (rect.center_x, rect.center_y)
        self.crisp_text.visible = self.widget.visible


class TextLayer:
    """Renders all text of the GUI at physical resolution."""

    def __init__(self, window: arcade.Window) -> None:
        self.ratio = window.get_pixel_ratio()
        width, height = window.get_size()
        w, h = width * self.ratio, height * self.ratio

        self.camera = arcade.Camera2D(
            position=(w / 2, h / 2),
            projection=LRBT(-w / 2, w / 2, -h / 2, h / 2),
            window=window,
        )
        self.batch = Batch()
        self.captions: list[_Caption] = []

    def text(self, text, x, y, font_size, **kwargs) -> CrispText:
        """Creates a text element. Pass `batch` to manage its lifetime yourself."""
        return CrispText(self, text, x, y, font_size, **kwargs)

    def add_caption(self, widget, font_size: float, color, mono: bool = False) -> _Caption:
        caption = _Caption(self, widget, font_size, color, mono)
        self.captions.append(caption)
        return caption

    def draw(self, batches: list[Batch] = ()) -> None:
        for caption in self.captions:
            caption.sync()

        with self.camera.activate():
            for batch in batches:
                batch.draw()
            self.batch.draw()
