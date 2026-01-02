import arcade
from pyglet.graphics import Batch

from mesa_arcade.utils import parse_color
from mesa_arcade.plot import _ModelHistoryPlot

class Figure:
    def __init__(self, components=[], background_color = "lightgray", title = None):
        self.components = components
        self.background_color = parse_color(background_color)
        self.title = title

    def setup(self, x, y, width, height, renderer):
        self.renderer = renderer
        self.width = width
        self.height = height

        self.font_size = self.height * 0.04
        
        self.n_grid_cols = self.renderer.model.grid.width
        self.n_grid_rows = self.renderer.model.grid.height
        self.cell_width = self.width / self.n_grid_cols
        self.cell_height = self.height / self.n_grid_rows

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


class ModelHistoryPlot(Figure):
    def __init__(self, y_attributes, legend=True, title=None):
        if not isinstance(y_attributes, (list, tuple)):
            y_attributes = [y_attributes]

        plot = _ModelHistoryPlot(
            y_attributes=y_attributes,
            legend=legend,
        )
        super().__init__(components=[plot], title=title)

class SpacePlot(Figure):
    def __init__(self, artists=[], background_color="white", title=None):
        if not isinstance(artists, (list, tuple)):
            artists = [artists]

        super().__init__(
            components=artists,
            background_color=background_color,
            title=title,
            )