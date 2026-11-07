import arcade
from pyglet.graphics import Batch

from mesarcade import styles
from mesarcade.utils import parse_color


class Figure:
    def __init__(
        self,
        get_space,
        components=[],
        background_color=None,
        title: str | None = None,
        figure_type: str | None = None,
    ):
        self.components = components
        # None: resolved in setup(), when the theme of the canvas is known
        self._background_color = background_color
        self.title = title
        self.get_space = get_space
        self.figure_type = figure_type

    def setup(self, x, y, width, height, renderer):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.renderer = renderer

        self.background_color = (
            styles.PANEL if self._background_color is None else parse_color(self._background_color)
        )

        self.font_size = self.height * 0.03

        if self.figure_type == "network":
            pass

        elif self.figure_type in ["grid", "continuous"]:
            space = self.get_space(self.renderer.model)
            self.space_width = space.width
            self.space_height = space.height
            self.cell_width = self.width / self.space_width
            self.cell_height = self.height / self.space_height

        self.shape_list = self.shape_list = arcade.shape_list.ShapeElementList()
        self.text_batch = Batch()
        self.text_list = []

        self.create_empty_figure()
        self.setup_components()

    def update(self):
        for component in self.components:
            component.update()

    def draw(self):
        # text is drawn by the renderer's text layer
        self.shape_list.draw()
        for component in self.components:
            component.draw()

    def setup_components(self) -> None:
        """Initializes/resets all components including all their sprites."""
        for component in self.components:
            component.setup(figure=self, renderer=self.renderer)

    def create_empty_figure(self):
        if self.title is not None:
            # panel header in the style of VS Code: small, uppercase, muted
            title_text = self.renderer.text_layer.text(
                text=self.title.upper(),
                x=self.x,
                y=self.y + self.height + 8,
                batch=self.text_batch,
                color=styles.TEXT_MUTED,
                font_size=self.renderer.font_size * 0.85,
                bold=True,
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
            color=styles.PLOT_BORDER,
            border_width=1,
        )
        self.shape_list.append(outline)
