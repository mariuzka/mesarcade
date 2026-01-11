import arcade
import mesa

from mesa_arcade.renderer import Renderer


class Canvas:
    def __init__(
        self, 
        model_class: mesa.Model,
        plots = [],
        controllers = [],
        window_width: int = 1200,
        window_title: str = "Mesa simulation",
        target_tps: int = 40,
        rendering_step: int = 1,
    ):
        window_height = int(window_width * 0.6)

        arcade.enable_timings()
        
        # the arcade window object
        self.window = arcade.Window(
            width=window_width, 
            height=window_height, 
            title=window_title, 
            resizable=False,
            antialiasing=False,
            )
        
        # the arcade view object
        self.renderer = Renderer(
            model_class=model_class,
            figures=plots,
            controllers=controllers,
            window_width=window_width,
            window_height=window_height,
            target_tps=target_tps,
            rendering_step=rendering_step,
            )
        

    def show(self) -> None:
        """Renders the canvas."""

        arcade.set_background_color(arcade.color.BLACK)
        
        # setup the renderer 
        self.renderer.setup()
        
        # initialize the mesa model
        self.renderer.setup_model()

        # initialize arcade window
        self.window.show_view(new_view=self.renderer)

        # show the window & run the simulation
        arcade.run()