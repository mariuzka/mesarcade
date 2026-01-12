import arcade
from pyglet.graphics import Batch

from mesa_arcade.utils import parse_color


class Figure:
    def __init__(
        self, space_attr_name: str, components=[], background_color="lightgray", title=None
    ):
        self.components = components
        self.background_color = parse_color(background_color)
        self.title = title
        self.space_attr_name = space_attr_name

    def setup(self, x, y, width, height, renderer):
        self.renderer = renderer
        self.width = width
        self.height = height

        self.font_size = self.height * 0.04

        if self.space_attr_name is not None:
            self.space_width = getattr(self.renderer.model, self.space_attr_name).width
            self.space_height = getattr(self.renderer.model, self.space_attr_name).height
            self.cell_width = self.width / self.space_width
            self.cell_height = self.height / self.space_height

        self.x = x
        self.y = y

        self.shape_list = self.shape_list = arcade.shape_list.ShapeElementList()
        self.text_batch = Batch()
        self.text_list = []

        self.create_empty_figure()
        self.setup_components()

    def update(self):
        for component in self.components:
            component.update()

    def draw(self):
        self.shape_list.draw()
        self.text_batch.draw()
        for component in self.components:
            component.draw()

    def setup_components(self) -> None:
        """Initializes/resets all components including all their sprites."""
        for component in self.components:
            component.setup(figure=self, renderer=self.renderer)

    def create_empty_figure(self):
        if self.title is not None:
            title_text = arcade.Text(
                text=self.title,
                x=self.x,
                y=self.y + self.height + 5,
                batch=self.text_batch,
                color=self.renderer.font_color,
                font_size=self.font_size,
            )
            self.text_list.append(title_text)

        background = arcade.shape_list.create_rectangle_filled(
            center_x=self.x + self.width / 2,
            center_y=self.y + self.height / 2,
            width=self.width,
            height=self.height,
            color=self.background_color,
        )
        self.shape_list.append(background)

        outline = arcade.shape_list.create_rectangle_outline(
            center_x=self.x + self.width / 2,
            center_y=self.y + self.height / 2,
            width=self.width,
            height=self.height,
            color=arcade.color.BLACK,
        )
        self.shape_list.append(outline)
