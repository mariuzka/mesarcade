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
    """The main GUI window for visualizing mesa agent-based models.

    Creates an interactive window that displays plots, controls, and value
    displays for a mesa simulation. Call show() to start the visualization.

    Args:
        model_class: The mesa model class to instantiate and visualize.
        plots: List of plots (e.g., GridSpacePlot, ModelHistoryPlot) to display.
            Maximum 4 plots supported.
        controllers: List of controllers (NumController, CatController) for
            adjusting model parameters interactively.
        value_displays: List of ValueDisplay instances showing model metrics.
        params: Dictionary of fixed model parameters passed to the model
            constructor. Values in this dict are overwritten by controllers
            that target the same parameter. Defaults to None.
        window_width: Window width in pixels. Height is calculated as 60% of
            width. Defaults to 1200.
        window_title: Title shown in the window title bar. Defaults to "mesarcade".
        target_fps: Target frames per second for animation. Defaults to 40.
        rendering_step: Number of simulation steps between visual updates.
            Defaults to 1.
    """

    def __init__(
        self,
        model_class: type[mesa.Model],
        plots: list[Figure] = [],
        controllers: list[NumController | CatController] = [],
        value_displays: list[ValueDisplay] = [],
        params: dict | None = None,
        window_width: int = 1200,
        window_title: str = "mesarcade",
        target_fps: int = 40,
        rendering_step: int = 1,
        _visible: bool = True,
    ) -> None:
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
            parameter_dict=params,
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
