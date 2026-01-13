import arcade
import arcade.gui
import arcade.gui.widgets.text
import mesa

from mesa_arcade.button import DefaultButtons
from mesa_arcade.controller import NumController


class Renderer(arcade.View):
    def __init__(
        self,
        model_class: mesa.model,
        figures: list,
        controllers: list,
        window_width: int,
        window_height: int,
        target_fps: int,
        rendering_step: int,
    ):
        super().__init__()

        self.model_class = model_class
        self.figures = figures
        self.controllers = controllers
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
        self.background_color = (235, 236, 238)
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

        # add default buttons & displays
        self.add_fps_display()
        self.add_tick_counter_display()
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
                    x=fig_4_x, y=fig_4_y, width=fig_width, height=fig_height, renderer=self
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

    def add_default_buttons(self):
        DefaultButtons(renderer=self).add_to_anchor()

    def add_tick_counter_display(self):
        self.tick_counter_text = arcade.gui.widgets.text.UILabel(
            text=f"tick: {self.tick}",
            text_color=arcade.color.BLACK,
            font_size=self.font_size,
        )
        self.anchor.add(
            self.tick_counter_text,
            anchor_x="left",
            anchor_y="top",
            align_x=int(self.atomic_width * 33),
            align_y=int(-self.atomic_height - self.big_button_height * 0.25),
        )

    def add_fps_display(self):
        self.fps_text = arcade.gui.widgets.text.UILabel(
            text=f"FPS: {int(arcade.get_fps(60))}",
            text_color=arcade.color.BLACK,
            font_size=self.font_size,
        )
        self.anchor.add(
            self.fps_text,
            anchor_x="left",
            anchor_y="top",
            align_x=int(self.atomic_width * 33),
            align_y=int(
                -self.atomic_height * 3 - self.atomic_height * 0.25,
            ),
        )

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

    def on_draw(self):
        """Render the screen."""

        self.clear()

        for figure in self.figures:
            figure.draw()

        self.manager.draw()

        # draw fps & tick counter
        self.fps_text.text = f"FPS: {int(arcade.get_fps(60))}"
        self.tick_counter_text.text = f"tick: {self.tick}"

    def on_update(self, delta_time):
        if self.play:
            self.model.step()
            self.tick += 1

            if self.tick % self.rendering_step == 0:
                for figure in self.figures:
                    figure.update()
