from __future__ import annotations

from typing import TYPE_CHECKING

import arcade
import mesa

from mesarcade.renderer import Renderer

if TYPE_CHECKING:
    from mesarcade.figure import Figure
    from mesarcade.controller import NumController, CatController
    from mesarcade.value_display import ValueDisplay


class Canvas:
    """The main GUI window."""

    def __init__(
        self,
        model_class: type[mesa.Model],
        plots: list[Figure] = [],
        controllers: list[NumController | CatController] = [],
        value_displays: list[ValueDisplay] = [],
        window_width: int = 1200,
        window_title: str = "mesarcade",
        target_fps: int = 40,
        rendering_step: int = 1,
        _visible: bool = True,
    ) -> None:
        """ "
        Creates a new canvas instance.

        Args:
            model_class (type[mesa.Model]):
                The mesa model class.
            plots (list, optional):
                The list of controllers that should be placed in the canvas.
                Currently, the maximum number of plots is 4.
                Defaults to [].
            controllers (list, optional):
                The list of controllers that should be placed in the canvas.
                Defaults to [].
            window_width (int, optional):
                The width of the canvas window in pixels.
                Determines the height of the canvas.
                Defaults to 1200.
            window_title (str, optional):
                The title of the canvas.
                Defaults to "mesarcade".
            target_fps (int, optional):
                The number of frames per second (FPS) that the animations should show.
                Defaults to 40.
            rendering_step (int, optional):
                The number of simulation steps until the visualizations are rerendered.
                Defaults to 1.
        """
        window_height = int(window_width * 0.6)

        if not arcade.timings_enabled():
            arcade.enable_timings()

        # the arcade window object
        self.window = arcade.Window(
            width=window_width,
            height=window_height,
            title=window_title,
            resizable=False,
            antialiasing=False,
            visible=_visible,
        )

        # the arcade view object
        self.renderer = Renderer(
            model_class=model_class,
            figures=plots,
            controllers=controllers,
            value_displays=value_displays,
            window_width=window_width,
            window_height=window_height,
            target_fps=target_fps,
            rendering_step=rendering_step,
        )

    def _setup(self):
        # setup the renderer
        self.renderer.setup()

        # initialize the mesa model
        self.renderer.setup_model()

        # initialize arcade window
        self.window.show_view(new_view=self.renderer)

    def show(self) -> None:
        """Renders the canvas."""

        # setup everything
        self._setup()

        # show the window & run the simulation
        arcade.run()
