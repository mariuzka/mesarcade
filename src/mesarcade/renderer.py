import arcade
import arcade.gui
import arcade.gui.widgets.text
import mesa

from mesarcade.button import DefaultButtons
from mesarcade.controller import NumController
from mesarcade.utils import parse_color
from mesarcade.value_display import ValueDisplay


class Renderer(arcade.View):
    def __init__(
        self,
        model_class: type[mesa.model],
        figures: list,
        controllers: list,
        value_displays: list,
        window_width: int,
        window_height: int,
        target_fps: int,
        rendering_step: int,
    ):
        super().__init__()

        self.model_class = model_class
        self.figures = figures
        self.controllers = controllers
        self.value_displays = value_displays
        self.parameter_dict = {}
        self.window_width = window_width
        self.window_height = window_height
        self.target_fps = target_fps
        self.rendering_step = rendering_step

    def setup(self):
        # play / pause state
        self.play = False

        # tick counter
        self.tick = 0

        # ui stuff
        self.buttons = []
        self.ui_groups = []
        self.anchor = arcade.gui.UIAnchorLayout()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager.add(self.anchor)
        self.background_color = parse_color("whitesmoke")
        self.font_color = (45, 45, 50)

        # calculate window properties
        self.atomic_width = round(self.window_width / 36)
        self.atomic_height = round(self.window_height / 36)

        self.small_button_width = self.atomic_width * 0.6
        self.small_button_height = self.atomic_height * 0.8
        self.big_button_width = round(self.atomic_width * 2)
        self.big_button_height = round(self.atomic_height * 2)

        self.font_size = round(self.atomic_height * 0.5)

        # setup core components
        self.setup_model()
        self.setup_controllers()

        # add default buttons
        self.add_fps_buttons()
        self.add_rendering_step_buttons()
        self.add_default_buttons()

        # set initial target fps
        self.set_fps(new_value=self.target_fps)

    def update_parameter_dict(self) -> None:
        for controller in self.controllers:
            self.parameter_dict[controller.parameter_name] = controller.parameter_value

    def setup_model(self) -> None:
        """Setups a fresh model instance with the current parameter setting."""

        # reset the tick counter
        self.tick = 0

        # get the latest parameter values from the controllers
        self.update_parameter_dict()

        # remove the fps parameter
        self.parameter_dict.pop("target_fps", None)
        self.parameter_dict.pop("rendering_step", None)

        # create a new model instance with the current parameter setting
        self.model = self.model_class(**self.parameter_dict)

        self.setup_figures()
        self.setup_value_displays()

    def setup_figures(self):
        if len(self.figures) == 1:
            fig_width = self.atomic_height * 33
            fig_height = self.atomic_height * 33

            fig = self.figures[0]
            fig_x = self.window_width / 2 - fig_width / 2 + self.atomic_width * 2
            fig_y = self.window_height / 2 - fig_width / 2
            fig.setup(x=fig_x, y=fig_y, width=fig_width, height=fig_height, renderer=self)

        elif len(self.figures) == 2:
            fig_width = self.atomic_height * 19
            fig_height = self.atomic_height * 19

            fig_1 = self.figures[0]
            fig_1_x = (
                self.window_width / 2 - fig_width / 2 - fig_width / 4 - self.atomic_height * 1.5
            )
            fig_1_y = self.window_height / 2 - fig_width / 2
            fig_1.setup(x=fig_1_x, y=fig_1_y, width=fig_width, height=fig_height, renderer=self)

            fig_2 = self.figures[1]
            fig_2_x = self.window_width / 2 + fig_width / 4 - self.atomic_height * 0.5
            fig_2_y = self.window_height / 2 - fig_width / 2
            fig_2.setup(x=fig_2_x, y=fig_2_y, width=fig_width, height=fig_height, renderer=self)

        elif len(self.figures) in [3, 4]:
            fig_width = self.atomic_height * 15
            fig_height = self.atomic_height * 15

            fig_1 = self.figures[0]
            fig_1_x = self.window_width / 2 - fig_width / 2 - fig_width / 4 - self.atomic_height
            fig_1_y = self.window_height / 2 + self.atomic_height
            fig_1.setup(x=fig_1_x, y=fig_1_y, width=fig_width, height=fig_height, renderer=self)

            fig_2 = self.figures[1]
            fig_2_x = self.window_width / 2 + fig_width / 4 + self.atomic_height
            fig_2_y = self.window_height / 2 + self.atomic_height
            fig_2.setup(x=fig_2_x, y=fig_2_y, width=fig_width, height=fig_height, renderer=self)

            fig_3 = self.figures[2]
            fig_3_x = self.window_width / 2 - fig_width / 2 - fig_width / 4 - self.atomic_height
            fig_3_y = self.window_height / 2 - fig_width - self.atomic_height
            fig_3.setup(x=fig_3_x, y=fig_3_y, width=fig_width, height=fig_height, renderer=self)

            if len(self.figures) == 4:
                fig_4 = self.figures[3]
                fig_4_x = self.window_width / 2 + fig_width / 4 + self.atomic_height
                fig_4_y = self.window_height / 2 - fig_width - self.atomic_height
                fig_4.setup(
                    x=fig_4_x,
                    y=fig_4_y,
                    width=fig_width,
                    height=fig_height,
                    renderer=self,
                )

    def set_target_objects_of_controllers(self):
        for i, controller in enumerate(self.controllers):
            if controller.parameter_name not in ["target_fps", "rendering_step"]:
                controller.buttons.target_object = self.model

    def setup_controllers(self) -> None:
        for i, controller in enumerate(self.controllers):
            controller.renderer = self
            controller.setup(i=i + 3)
        self.set_target_objects_of_controllers()

    def draw_value_displays(self) -> None:
        self.tick_display.draw()
        self.fps_display.draw()
        for value_display in self.value_displays:
            value_display.draw()

    def update_value_displays(self, force_update=False) -> None:
        self.tick_display.update(new_value=self.tick, force_update=force_update)
        self.fps_display.update(new_value=int(arcade.get_fps(60)), force_update=force_update)
        for value_display in self.value_displays:
            value_display.update(force_update=force_update)

    def setup_value_displays(self) -> None:
        self.tick_display = ValueDisplay(label="Tick", update_step=10)
        self.tick_display.setup(i=1, renderer=self, initial_value=self.tick)

        self.fps_display = ValueDisplay(label="FPS", update_step=10)
        self.fps_display.setup(i=2, renderer=self, initial_value=int(arcade.get_fps(60)))

        for i, value_display in enumerate(self.value_displays):
            value_display.setup(i=i + 3, renderer=self)

    def add_default_buttons(self):
        DefaultButtons(renderer=self).add_to_anchor()

    def add_rendering_step_buttons(self):
        self.rendering_step_buttons = NumController(
            parameter_name="rendering_step",
            parameter_value=self.rendering_step,
            min_value=1,
            max_value=10,
            step=1,
            label="Rendering step",
            _target_object=self,
        )
        self.rendering_step_buttons.renderer = self
        self.rendering_step_buttons.setup(i=2)
        self.controllers.append(self.rendering_step_buttons)
        self.rendering_step_buttons.buttons.slider.on_change = self.on_rendering_step_change

    def add_fps_buttons(self):
        self.fps_buttons = NumController(
            parameter_name="target_fps",
            parameter_value=self.target_fps,
            min_value=5,
            max_value=60,
            step=5,
            label="Target FPS",
            _target_object=self,
        )
        self.fps_buttons.renderer = self
        self.fps_buttons.setup(i=1)
        self.controllers.append(self.fps_buttons)
        self.fps_buttons.buttons.slider.on_change = self.on_fps_change

    def set_fps(self, new_value):
        self.target_fps = int(new_value)
        self.window.set_update_rate(1 / self.target_fps)
        self.fps_buttons.buttons.update()

    def on_fps_change(self, slider_event):
        self.set_fps(slider_event.new_value)

    def set_rendering_step(self, new_value):
        self.rendering_step = new_value

    def on_rendering_step_change(self, slider_event):
        self.rendering_step_buttons.buttons.update()
        self.set_rendering_step(slider_event.new_value)

    def draw_figures(self):
        for figure in self.figures:
            figure.draw()

    def update_figures(self):
        for figure in self.figures:
            figure.update()

    def on_draw(self):
        """Render the screen."""

        self.clear()
        self.draw_figures()
        self.draw_value_displays()

        self.manager.draw()

    def on_update(self, delta_time):
        if self.play:
            self.model.step()
            self.tick += 1

            if self.tick % self.rendering_step == 0:
                self.update_figures()
                self.update_value_displays()
