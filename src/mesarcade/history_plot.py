from __future__ import annotations

from typing import TYPE_CHECKING

import arcade
import numpy as np

from mesarcade import styles
from mesarcade.figure import Figure
from mesarcade.utils import parse_color

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    import mesa

# Type alias for color values
Color = str | tuple[int, int, int] | tuple[int, int, int, int]


def rescale(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    if old_range > 0:
        return (value - old_min) / old_range * new_range + new_min
    else:
        return (value - old_min) * new_range + new_min


def rescale_array_column_inplace(
    np_array: np.ndarray,
    col: int,
    old_min: float,
    old_max: float,
    new_min: float,
    new_max: float,
) -> None:
    values = np_array[:, col]

    old_range = old_max - old_min
    new_range = new_max - new_min

    if old_range > 0:
        values[:] = (values - old_min) / old_range * new_range + new_min
    else:
        values[:] = (values - old_min) * new_range + new_min


def format_tick(value: float) -> str:
    """Formats an axis tick value compactly (max. 4 significant digits)."""
    return f"{value:.4g}"


class _ModelHistoryPlot:
    def __init__(
        self,
        model_attributes: list[str | Callable[[mesa.Model], Any]],
        ylim: list[float | None, float | None] | None = None,
        labels: list[str] | None = None,
        colors: list[str] | None = None,
        rendering_step: int = 5,
        title=None,
        legend: bool = True,
        from_datacollector: bool = False,
    ):
        self.model_attrs = model_attributes
        self.lower_y_lim = ylim[0] if ylim is not None else None
        self.upper_y_lim = ylim[1] if ylim is not None else None
        self.labels = labels
        self.rendering_step = rendering_step
        self.legend = legend
        self.title = title
        self.from_datacollector = from_datacollector
        self.colors = None

        self.padding = 10

        self.validate_input()

        if colors is not None:
            self.colors = [parse_color(color) for color in colors]
        else:
            self.colors = list(styles.DATA_COLORS)

    def validate_input(self):
        if len(self.model_attrs) > 6:
            raise ValueError("Only 6 lines allowed!")

        if self.labels is not None:
            if len(self.model_attrs) != len(self.labels):
                raise ValueError(
                    "The arguments model_attributes and labels must have the same length."
                )

        if self.colors is not None:
            if len(self.model_attrs) != len(self.colors):
                raise ValueError(
                    "The arguments model_attributes and colors must have the same length."
                )

    def setup(self, figure, renderer):
        self.figure = figure
        self.renderer = renderer
        self.model = self.renderer.model

        self.x = self.figure.x
        self.y = self.figure.y

        self.width = self.figure.width
        self.height = self.figure.height

        self.font_size = self.height * 0.026

        # leave room on the left for y tick labels like "0.7811"
        self.plot_area_x = self.x + self.width * 0.18
        self.plot_area_y = self.y + self.height * 0.3
        self.plot_area_width = self.width * (0.82 - 0.03)
        self.plot_area_height = self.height * (0.7 - 0.025)

        self.data_dict = {model_attr: [] for model_attr in self.model_attrs}
        self.scaled_data_dict = {model_attr: [] for model_attr in self.model_attrs}
        self.min_y = self.lower_y_lim
        self.max_y = self.upper_y_lim
        self.min_x = 0
        self.max_x = 0

        self.create_plot_area()
        self.create_axis_ticks()

        # add legend
        if self.legend:
            self.create_legend()

    def _text(self, text, x, y, color=None, **kwargs):
        return self.renderer.text_layer.text(
            text=text,
            x=x,
            y=y,
            color=styles.PLOT_TEXT_MUTED if color is None else color,
            font_size=self.font_size,
            batch=self.figure.text_batch,
            **kwargs,
        )

    def _y_tick_positions(self):
        bottom = self.plot_area_y + self.padding
        span = self.plot_area_height - self.padding * 2
        return [bottom + span / 4 * i for i in range(5)]

    def create_plot_area(self):
        left = self.plot_area_x
        right = self.plot_area_x + self.plot_area_width
        bottom = self.plot_area_y
        top = self.plot_area_y + self.plot_area_height

        # horizontal grid lines
        for y in self._y_tick_positions():
            self.figure.shape_list.append(
                arcade.shape_list.create_line(left, y, right, y, styles.PLOT_GRID, 1)
            )

        # left and bottom axis
        self.figure.shape_list.append(
            arcade.shape_list.create_line(left, bottom, left, top, styles.PLOT_AXIS, 1)
        )
        self.figure.shape_list.append(
            arcade.shape_list.create_line(left, bottom, right, bottom, styles.PLOT_AXIS, 1)
        )

    def create_axis_ticks(self):
        tick_length = 4
        label_x = self.plot_area_x - tick_length - 4

        # y ticks: lines at all 5 positions, labels at min, mid and max
        y_positions = self._y_tick_positions()
        for y in y_positions:
            self.figure.shape_list.append(
                arcade.shape_list.create_line(
                    self.plot_area_x - tick_length, y, self.plot_area_x, y, styles.PLOT_AXIS, 1
                )
            )

        self.min_y_label = self._text(
            "", label_x, y_positions[0], anchor_x="right", anchor_y="cap_center", mono=True
        )
        self.mid_y_label = self._text(
            "", label_x, y_positions[2], anchor_x="right", anchor_y="cap_center", mono=True
        )
        self.max_y_label = self._text(
            "", label_x, y_positions[4], anchor_x="right", anchor_y="cap_center", mono=True
        )

        # x ticks: first and current tick
        x_left = self.plot_area_x + self.padding
        x_right = self.plot_area_x + self.plot_area_width - self.padding
        for x in (x_left, x_right):
            self.figure.shape_list.append(
                arcade.shape_list.create_line(
                    x, self.plot_area_y - tick_length, x, self.plot_area_y, styles.PLOT_AXIS, 1
                )
            )

        x_label_y = self.plot_area_y - tick_length - 4
        self.min_x_label = self._text(
            "0", x_left, x_label_y, anchor_x="center", anchor_y="top", mono=True
        )
        self.max_x_label = self._text(
            "0", x_right, x_label_y, anchor_x="center", anchor_y="top", mono=True
        )
        self.x_axis_title = self._text(
            "tick",
            self.plot_area_x + self.plot_area_width / 2,
            x_label_y,
            anchor_x="center",
            anchor_y="top",
            italic=True,
        )

    def create_legend(self):
        label_x = self.figure.x + self.width * 0.1
        label_y = self.plot_area_y - self.height * 0.12

        if self.labels is not None:
            labels = self.labels
        elif self.labels is None and isinstance(self.model_attrs[0], str):
            labels = self.model_attrs
        else:
            labels = ["no label"] * len(self.model_attrs)

        for i, label in enumerate(labels):
            if i % 2 == 0:
                label_y -= self.font_size * 2
            if i % 2 != 0:
                label_x_ = label_x + self.figure.width / 2
            else:
                label_x_ = label_x

            label_element = self._text(
                label, label_x_, label_y, color=styles.PLOT_TEXT, anchor_y="cap_center"
            )
            self.figure.text_list.append(label_element)

            line_sample = arcade.shape_list.create_line(
                label_x_ - self.font_size * 2.2,
                label_y,
                label_x_ - self.font_size * 0.6,
                label_y,
                self.colors[i],
                3,
            )
            self.figure.shape_list.append(line_sample)

    def update(self):
        # get the current time step
        tick = self.renderer.tick

        # check if it is time to update
        if tick % self.rendering_step == 0 or tick <= 1:
            # for each model attribute that has to be collected
            for model_attr in self.model_attrs:
                # model attribute was given as string?
                if isinstance(model_attr, str):
                    # get the value from a model attribute
                    if not self.from_datacollector:
                        y = getattr(self.model, model_attr)

                    # or get the value from the datacollector
                    else:
                        y_data = self.model.datacollector.model_vars[model_attr]
                        y = y_data[-1] if len(y_data) > 0 else None

                # or as lambda?
                else:
                    y = model_attr(self.model)

                # if there valid new data
                if y is not None and np.isfinite(y):
                    # set min and max values initially (only from valid data,
                    # otherwise None/NaN would break the axis permanently)
                    if self.max_y is None:
                        self.max_y = y
                    if self.min_y is None:
                        self.min_y = y

                    # add new data point
                    self.data_dict[model_attr].append((tick, y))

                    # update min and max values
                    if self.lower_y_lim is None:
                        self.min_y = min(self.min_y, y)

                    if self.upper_y_lim is None:
                        self.max_y = max(self.max_y, y)

                # Rescale the data
                # TODO: Optimize this with numpy
                self.scaled_data_dict[model_attr] = [
                    (
                        rescale(
                            value=x,
                            old_min=0,
                            old_max=tick,
                            new_min=self.plot_area_x + self.padding,
                            new_max=self.plot_area_x + self.plot_area_width - self.padding,
                        ),
                        rescale(
                            value=y,
                            old_min=self.min_y,
                            old_max=self.max_y,
                            new_min=self.plot_area_y + self.padding,
                            new_max=self.plot_area_y + self.plot_area_height - self.padding,
                        ),
                    )
                    for x, y in self.data_dict[model_attr]
                ]

            # update axis labels (y range is unknown until the first valid value)
            if self.min_y is not None and self.max_y is not None:
                self.min_y_label.text = format_tick(self.min_y)
                self.mid_y_label.text = format_tick((self.min_y + self.max_y) / 2)
                self.max_y_label.text = format_tick(self.max_y)
            self.max_x_label.text = str(tick)

    def draw(self):
        for i, model_attr in enumerate(self.model_attrs):
            arcade.draw_line_strip(
                self.scaled_data_dict[model_attr],
                color=self.colors[i],
                line_width=2,
            )


class ModelHistoryPlot(Figure):
    """A line plot that displays the history of model attributes over time.

    Tracks one or more model attributes and visualizes their values as lines
    over the course of the simulation. Supports up to 6 lines.

    Args:
        model_attributes: List of model attributes to track. Each element can be
            a string (attribute name) or a callable that takes a mesa.Model and
            returns a numeric value.
        ylim: Optional y-axis limits as [min, max]. If None, limits are
            determined automatically from the data. Individual elements can be
            None to auto-scale only that bound.
        labels: Optional labels for the legend. If None, attribute names are
            used for string attributes, or "no label" for callables.
        colors: Optional colors for the lines. Accepts color names, RGB tuples,
            or RGBA tuples. Defaults to a predefined color palette.
        legend: Whether to display a legend. Defaults to True.
        title: Optional title for the plot.
        from_datacollector: If True, reads values from the model's datacollector
            instead of directly from model attributes. Only works with string
            attributes. Defaults to False.
        rendering_step: Simulation steps between plot updates. Defaults to 3.
    """

    def __init__(
        self,
        model_attributes: list[str],
        ylim: list[float, float] | None = None,
        labels: list[str] | None = None,
        colors: list[Color] | None = None,
        legend: bool = True,
        title: str | None = None,
        from_datacollector: bool = False,
        rendering_step: int = 3,
    ) -> None:
        plot = _ModelHistoryPlot(
            model_attributes=model_attributes,
            ylim=ylim,
            labels=labels,
            colors=colors,
            legend=legend,
            title=title,
            rendering_step=rendering_step,
            from_datacollector=from_datacollector,
        )
        super().__init__(components=[plot], title=title, get_space=None)
