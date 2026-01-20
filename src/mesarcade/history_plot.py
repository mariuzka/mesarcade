import arcade
import numpy as np
from mesarcade.figure import Figure


def rescale(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    if old_range > 0:
        return (value - old_min) / old_range * new_range + new_max
    else:
        return (value - old_min) * new_range + new_max


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
        values[:] = (values - old_min) / old_range * new_range + new_max
    else:
        values[:] = (values - old_min) * new_range + new_max


class _ModelHistoryPlot:
    def __init__(self, y_attributes, step=5, legend=True):
        if len(y_attributes) > 6:
            raise ValueError("Only 6 lines allowed!")

        self.y_attrs = y_attributes
        self.step = step
        self.legend = legend

        self.color_list = [
            arcade.color.NAVY_BLUE,
            arcade.color.ORANGE,
            arcade.color.GREEN,
            arcade.color.RED,
            arcade.color.PINK,
            arcade.color.PURPLE,
            ]

    def setup(self, figure, renderer):
        self.figure = figure
        self.renderer = renderer

        self.x = self.figure.x
        self.y = self.figure.y

        self.width = self.figure.width
        self.height = self.figure.height

        self.font_size = int(self.height * 0.03)

        self.plot_area_x = self.x + self.width * 0.15
        self.plot_area_y = self.y + self.height * 0.3
        self.plot_area_width = self.width * (0.85 - 0.025)
        self.plot_area_height = self.height * (0.7 - 0.025)

        self.data_dict = {y_attr: [] for y_attr in self.y_attrs}
        self.scaled_data_dict = {y_attr: [] for y_attr in self.y_attrs}
        self.min_y = 0
        self.max_y = 0
        self.min_x = 0
        self.max_x = 0

        self.create_plot_area()
        self.create_axis_ticks()

        # add legend
        if self.legend:
            self.create_legend()

    def create_plot_area(self):
        background = arcade.shape_list.create_rectangle_filled(
            center_x=self.plot_area_x + self.plot_area_width / 2,
            center_y=self.plot_area_y + self.plot_area_height / 2,
            width=self.plot_area_width,
            height=self.plot_area_height,
            color=arcade.color.WHITE,
        )
        self.figure.shape_list.append(background)

        outline = arcade.shape_list.create_rectangle_outline(
            center_x=self.plot_area_x + self.plot_area_width / 2,
            center_y=self.plot_area_y + self.plot_area_height / 2,
            width=self.plot_area_width,
            height=self.plot_area_height,
            color=arcade.color.BLACK,
            border_width=2,
        )
        self.figure.shape_list.append(outline)

    def create_axis_ticks(self):
        self.min_y_label = arcade.Text(
            text="",
            x=0,
            y=self.plot_area_y,
            color=arcade.color.BLACK,
            font_size=self.font_size,
            batch=self.figure.text_batch,
        )
        self.max_y_label = arcade.Text(
            text="",
            x=0,
            y=self.plot_area_y + self.plot_area_height - self.font_size,
            color=arcade.color.BLACK,
            font_size=self.font_size,
            batch=self.figure.text_batch,
        )

    def create_legend(self):
        label_x = self.figure.x + self.width * 0.1
        label_y = self.plot_area_y - self.height * 0.1

        for i, y_attr in enumerate(self.y_attrs):
            if i % 2 == 0:
                label_y -= self.font_size * 2
            if i % 2 != 0:
                label_x_ = label_x + self.figure.width / 2
            else:
                label_x_ = label_x

            label_text = arcade.Text(
                text=y_attr,
                x=label_x_,
                y=label_y,
                batch=self.figure.text_batch,
                color=self.renderer.font_color,
                font_size=self.font_size,
            )
            self.figure.text_list.append(label_text)

            color_dot = arcade.shape_list.create_ellipse(
                center_x=label_x_ - self.font_size,
                center_y=label_y + self.font_size / 3,
                width=self.font_size,
                height=self.font_size,
                color=self.color_list[i],
            )
            self.figure.shape_list.append(color_dot)

    def update(self):
        # get the current time step
        tick = self.renderer.tick

        # check if it is time to update
        if tick % self.step == 0 or tick <= 1:
            
            # for each model attribute that has to be collected
            for y_attr in self.y_attrs:
                
                # check if the model has the attribute
                # TODO: Improve this. Maybe ask whether to use the datacollector or not.
                if hasattr(self.renderer.model, y_attr):
                    y = getattr(self.renderer.model, y_attr)

                # if not
                else:
                    # get the data from the datacollector
                    y_data = self.renderer.model.datacollector.model_vars[y_attr]
                    y = y_data[-1] if len(y_data) > 0 else None

                # update min and max values
                if y is not None and np.isfinite(y):
                    if y > self.max_y:
                        self.max_y = y
                    elif y < self.min_y:
                        self.min_y = y
                    self.data_dict[y_attr].append((tick, y))

                # Rescale the data
                # TODO: Optimize this with numpy
                self.scaled_data_dict[y_attr] = [
                    (
                        rescale(
                            value=x,
                            old_min=0,
                            old_max=tick,
                            new_min=self.plot_area_x,
                            new_max=self.plot_area_x + self.plot_area_width,
                        )
                        - self.plot_area_width,
                        rescale(
                            value=y,
                            old_min=self.min_y,
                            old_max=self.max_y,
                            new_min=self.plot_area_y,
                            new_max=self.plot_area_y + self.plot_area_height,
                        )
                        - self.plot_area_height,
                    )
                    for x, y in self.data_dict[y_attr]
                ]

            # update lower y_label
            str_min_y_label = str(round(self.min_y, 3))
            if self.min_y_label.text != str_min_y_label:
                self.min_y_label.text = str_min_y_label
                self.min_y_label.x = (
                    self.plot_area_x - (len(str_min_y_label) + 1) * self.font_size / 1.5
                )
            # update upper y_label
            str_max_y_label = str(round(self.max_y, 3))
            if self.max_y_label != str_max_y_label:
                self.max_y_label.text = str_max_y_label
                self.max_y_label.x = (
                    self.plot_area_x - (len(str_max_y_label) + 1) * self.font_size / 1.5
                )

    def draw(self):
        for i, y_attr in enumerate(self.y_attrs):
            arcade.draw_line_strip(
                self.scaled_data_dict[y_attr],
                color=self.color_list[i],
                line_width=2,
            )


class ModelHistoryPlot(Figure):
    def __init__(self, y_attributes, legend=True, title=None):
        if not isinstance(y_attributes, (list, tuple)):
            y_attributes = [y_attributes]

        plot = _ModelHistoryPlot(
            y_attributes=y_attributes,
            legend=legend,
        )
        super().__init__(components=[plot], title=title, space_attr_name=None)
