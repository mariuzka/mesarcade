"""Central visual theme of mesarcade.

Modelled after Visual Studio Code: neutral surfaces, thin borders, a blue
accent and a monospaced font for numbers. Two themes are available, "dark"
(VS Code "Dark Modern") and "light" (VS Code "Light Modern"). The active theme
is selected with `apply_theme`, which `mesarcade.Canvas` calls on creation.

All colors are module attributes (e.g. `styles.TEXT`) and must be looked up
at call time, not bound at import time, so that switching themes works.
"""

import arcade
from arcade.gui import UISlider

# fonts: the system UI font for labels (like VS Code's workbench) and a
# monospaced font for numbers (like VS Code's editor)
FONT_NAME = (".AppleSystemUIFont", "Segoe UI", "Ubuntu", "Helvetica Neue", "Arial")
MONO_FONT_NAME = ("Menlo", "Consolas", "DejaVu Sans Mono", "Courier New")

# gui widgets draw their own text blurry on HiDPI displays, so it is hidden and
# drawn crisply by mesarcade.text instead
TRANSPARENT = (0, 0, 0, 0)

# text on accent colored surfaces (primary button, status bar while running)
TEXT_ON_ACCENT = (255, 255, 255, 255)

# colorblind-safe categorical palette (Okabe & Ito, 2008), ordered for
# good contrast on the light plot background
DATA_COLORS = [
    (0, 114, 178, 255),  # blue
    (230, 159, 0, 255),  # orange
    (0, 158, 115, 255),  # bluish green
    (213, 94, 0, 255),  # vermillion
    (204, 121, 167, 255),  # reddish purple
    (86, 180, 233, 255),  # sky blue
]

# plots are always light "paper" surfaces, in both themes
_PLOT = dict(
    PANEL=(255, 255, 255, 255),
    PLOT_GRID=(229, 229, 229, 255),
    PLOT_AXIS=(130, 130, 130, 255),
    PLOT_TEXT=(51, 51, 51, 255),
    PLOT_TEXT_MUTED=(110, 110, 110, 255),
    EDGE=(150, 150, 150, 255),  # network edges
)

THEMES = {
    # VS Code "Dark Modern"
    "dark": dict(
        _PLOT,
        PANEL=(250, 250, 250, 255),
        PLOT_BORDER=(60, 60, 60, 255),
        BACKGROUND=(31, 31, 31, 255),  # editor
        SIDEBAR=(24, 24, 24, 255),  # side bar, status bar
        BORDER=(43, 43, 43, 255),
        TEXT=(204, 204, 204, 255),
        TEXT_MUTED=(157, 157, 157, 255),
        NUMBER=(181, 206, 168, 255),  # numeric literals
        ACCENT=(0, 120, 212, 255),
        ACCENT_HOVER=(2, 110, 193, 255),
        ACCENT_PRESS=(0, 92, 164, 255),
        ACCENT_DISABLED=(43, 43, 43, 255),
        SURFACE=(49, 49, 49, 255),
        SURFACE_HOVER=(60, 60, 60, 255),
        SURFACE_PRESS=(69, 69, 69, 255),
        SURFACE_BORDER=(60, 60, 60, 255),
        SLIDER_TRACK=(60, 60, 60, 255),
        SLIDER_THUMB=(204, 204, 204, 255),
        SLIDER_THUMB_ACTIVE=(255, 255, 255, 255),
    ),
    # VS Code "Light Modern"
    "light": dict(
        _PLOT,
        PLOT_BORDER=(206, 206, 206, 255),
        BACKGROUND=(255, 255, 255, 255),  # editor
        SIDEBAR=(248, 248, 248, 255),  # side bar, status bar
        BORDER=(229, 229, 229, 255),
        TEXT=(59, 59, 59, 255),
        TEXT_MUTED=(110, 110, 110, 255),
        NUMBER=(9, 134, 88, 255),  # numeric literals
        ACCENT=(0, 95, 184, 255),
        ACCENT_HOVER=(2, 88, 168, 255),
        ACCENT_PRESS=(0, 76, 148, 255),
        ACCENT_DISABLED=(229, 229, 229, 255),
        SURFACE=(229, 229, 229, 255),
        SURFACE_HOVER=(204, 204, 204, 255),
        SURFACE_PRESS=(189, 189, 189, 255),
        SURFACE_BORDER=(206, 206, 206, 255),
        SLIDER_TRACK=(229, 229, 229, 255),
        SLIDER_THUMB=(110, 110, 110, 255),
        SLIDER_THUMB_ACTIVE=(59, 59, 59, 255),
    ),
}

# colors of the active theme, set by apply_theme()
Color = tuple[int, int, int, int]
PANEL: Color = THEMES["dark"]["PANEL"]
PLOT_BORDER: Color = THEMES["dark"]["PLOT_BORDER"]
PLOT_GRID: Color = THEMES["dark"]["PLOT_GRID"]
PLOT_AXIS: Color = THEMES["dark"]["PLOT_AXIS"]
PLOT_TEXT: Color = THEMES["dark"]["PLOT_TEXT"]
PLOT_TEXT_MUTED: Color = THEMES["dark"]["PLOT_TEXT_MUTED"]
EDGE: Color = THEMES["dark"]["EDGE"]
BACKGROUND: Color = THEMES["dark"]["BACKGROUND"]
SIDEBAR: Color = THEMES["dark"]["SIDEBAR"]
BORDER: Color = THEMES["dark"]["BORDER"]
TEXT: Color = THEMES["dark"]["TEXT"]
TEXT_MUTED: Color = THEMES["dark"]["TEXT_MUTED"]
NUMBER: Color = THEMES["dark"]["NUMBER"]
ACCENT: Color = THEMES["dark"]["ACCENT"]
ACCENT_HOVER: Color = THEMES["dark"]["ACCENT_HOVER"]
ACCENT_PRESS: Color = THEMES["dark"]["ACCENT_PRESS"]
ACCENT_DISABLED: Color = THEMES["dark"]["ACCENT_DISABLED"]
SURFACE: Color = THEMES["dark"]["SURFACE"]
SURFACE_HOVER: Color = THEMES["dark"]["SURFACE_HOVER"]
SURFACE_PRESS: Color = THEMES["dark"]["SURFACE_PRESS"]
SURFACE_BORDER: Color = THEMES["dark"]["SURFACE_BORDER"]
SLIDER_TRACK: Color = THEMES["dark"]["SLIDER_TRACK"]
SLIDER_THUMB: Color = THEMES["dark"]["SLIDER_THUMB"]
SLIDER_THUMB_ACTIVE: Color = THEMES["dark"]["SLIDER_THUMB_ACTIVE"]

THEME = "light"


def apply_theme(theme: str) -> None:
    """Activates a theme ("dark" or "light")."""
    if theme not in THEMES:
        raise ValueError(f"Unknown theme {theme!r}. Choose one of {list(THEMES)}.")
    global THEME
    THEME = theme
    globals().update(THEMES[theme])


apply_theme(THEME)


def _button_state(font_size, font_color, bg, border, border_width=1):
    return arcade.gui.UIFlatButton.UIStyle(
        font_name=FONT_NAME,
        font_size=font_size,
        font_color=font_color,
        bg=bg,
        border=border,
        border_width=border_width,
    )


def create_button_style(font_size, font_color=TRANSPARENT):
    """Secondary button: grey surface with a thin border."""
    return {
        "normal": _button_state(font_size, font_color, SURFACE, SURFACE_BORDER),
        "hover": _button_state(font_size, font_color, SURFACE_HOVER, SURFACE_BORDER),
        "press": _button_state(font_size, font_color, SURFACE_PRESS, SURFACE_BORDER),
        "disabled": _button_state(font_size, font_color, SURFACE, SURFACE_BORDER),
    }


def create_primary_button_style(font_size, font_color=TRANSPARENT):
    """Primary button: filled with the accent color."""
    return {
        "normal": _button_state(font_size, font_color, ACCENT, ACCENT),
        "hover": _button_state(font_size, font_color, ACCENT_HOVER, ACCENT_HOVER),
        "press": _button_state(font_size, font_color, ACCENT_PRESS, ACCENT_PRESS),
        "disabled": _button_state(font_size, font_color, ACCENT_DISABLED, ACCENT_DISABLED),
    }


def create_slider_style():
    """Slim track with accent fill and a solid light thumb, no step dots."""

    def state(thumb):
        return UISlider.UIStyle(
            bg=thumb,
            border=thumb,
            border_width=1,
            filled_track=ACCENT,
            filled_step=None,
            unfilled_track=SLIDER_TRACK,
            unfilled_step=None,
        )

    return {
        "normal": state(SLIDER_THUMB),
        "hover": state(SLIDER_THUMB_ACTIVE),
        "press": state(SLIDER_THUMB_ACTIVE),
        "disabled": state(SLIDER_TRACK),
    }
