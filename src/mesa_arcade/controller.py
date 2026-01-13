import arcade
import arcade.gui
import arcade.gui.widgets.text

from mesa_arcade.styles import create_button_style
from mesa_arcade.button import SmallButton


def round_parameter_value(value, step):
    if isinstance(step, int):
        return int(value)
    else:
        return round(value, len(str(step)) + 1)


def get_current_parameter_value(parameter_name, target_object, renderer):
    if hasattr(target_object, parameter_name):
        return getattr(target_object, parameter_name)
    else:
        return renderer.parameter_dict[parameter_name]


def set_new_parameter_value(parameter_name, new_value, target_object, renderer, controller):
    if hasattr(target_object, parameter_name):
        setattr(
            target_object,
            parameter_name,
            new_value,
        )
    controller.parameter_value = new_value
    renderer.parameter_dict[parameter_name] = new_value


class _Controller:
    def __init__(
        self,
        parameter_name: str,
        parameter_value: float,
        label: str | None = None,
        _target_object=None,
    ):
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value
        self.label = label
        self._target_object = _target_object
        self.renderer = None

    def calculate_align_y(self, i):
        return round(-(i * (self.renderer.atomic_height * 3.1)) - self.renderer.atomic_height * 2)


class CatController(_Controller):
    def __init__(
        self,
        parameter_name,
        parameter_value,
        parameter_options=[],
        label=None,
        _target_object=None,
    ):
        super().__init__(
            parameter_name,
            parameter_value,
            label,
            _target_object,
        )
        self.parameter_options = parameter_options

    def setup(self, i):
        self.align_y = self.calculate_align_y(i=i)
        self.buttons = CatControllerButtons(
            controller=self,
            align_y=self.align_y,
            renderer=self.renderer,
            parameter_name=self.parameter_name,
            value=self.parameter_value,
            options=self.parameter_options,
            label=self.label,
            target_object=self._target_object,
        )
        self.buttons.add_to_anchor()


class NumController(_Controller):
    def __init__(
        self,
        parameter_name,
        parameter_value,
        min_value,
        max_value,
        step,
        label=None,
        _target_object=None,
    ):
        super().__init__(
            parameter_name=parameter_name,
            parameter_value=parameter_value,
            label=label,
            _target_object=_target_object,
        )
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.buttons = None

    def setup(self, i):
        self.align_y = self.calculate_align_y(i=i)
        self.buttons = NumControllerButtons(
            controller=self,
            align_y=self.align_y,
            renderer=self.renderer,
            parameter_name=self.parameter_name,
            value=self.parameter_value,
            min_value=self.min_value,
            max_value=self.max_value,
            step=self.step,
            label=self.label,
            target_object=self._target_object,
        )
        self.buttons.add_to_anchor()


class ControllerButton(SmallButton):
    def __init__(
        self,
        controller: _Controller,
        controller_buttons: "NumControllerButtons",
        renderer,
        parameter_name: str,
        increase=True,
        step=0.1,
    ):
        self.controller = controller
        self.controller_buttons = controller_buttons
        self.parameter_name = parameter_name
        self.increase = increase
        self.step = step if self.increase else -step
        self.step_digits = len(str(step))
        super().__init__(renderer=renderer)
        self.renderer.ui_groups.append(self)
        self.text = "+" if self.increase else "-"

    def on_click(self, event):
        if self.parameter_name not in ["target_fps", "rendering_step"]:
            self.controller_buttons.target_object = self.renderer.model

        current_value = get_current_parameter_value(
            parameter_name=self.parameter_name,
            target_object=self.controller_buttons.target_object,
            renderer=self.renderer,
        )
        new_parameter_value = current_value + self.step
        new_parameter_value = round_parameter_value(new_parameter_value, self.step)

        if new_parameter_value > self.controller_buttons.max_value:
            new_parameter_value = self.controller_buttons.max_value

        if new_parameter_value < self.controller_buttons.min_value:
            new_parameter_value = self.controller_buttons.min_value

        set_new_parameter_value(
            parameter_name=self.parameter_name,
            new_value=new_parameter_value,
            target_object=self.controller_buttons.target_object,
            renderer=self.renderer,
            controller=self.controller,
        )
        self.controller_buttons.update()

        # TODO: make this better
        if self.parameter_name == "target_fps":
            self.renderer.set_fps(new_value=new_parameter_value)
        elif self.parameter_name == "rendering_step":
            self.renderer.set_rendering_step(new_value=new_parameter_value)


class _ControllerButtons:
    def __init__(
        self,
        controller,
        align_y,
        renderer,
        parameter_name: str,
        value,
        label=None,
        target_object=None,
    ):
        self.controller = controller
        self.align_y = align_y
        self.renderer = renderer
        self.parameter_name = parameter_name
        self.parameter_value = value
        self.label = label
        self.target_object = self.renderer.model if target_object is None else target_object
        self.current_value = get_current_parameter_value(
            parameter_name=self.parameter_name,
            target_object=self.target_object,
            renderer=self.renderer,
        )

    def update(self):
        self.current_value = get_current_parameter_value(
            parameter_name=self.parameter_name,
            target_object=self.target_object,
            renderer=self.renderer,
        )
        self.label_current_value.text = self.current_value
        self.slider.value = self.current_value

    def add_to_anchor(self):
        pass


class CatControllerButtons(_ControllerButtons):
    def __init__(
        self,
        controller,
        align_y,
        renderer,
        parameter_name: str,
        value,
        options,
        label=None,
        target_object=None,
    ):
        self.controller = controller
        self.align_y = align_y
        self.renderer = renderer
        self.parameter_name = parameter_name
        self.parameter_value = value
        self.options = options
        self.label = label
        self.target_object = self.renderer.model if target_object is None else target_object

        self.current_value = get_current_parameter_value(
            parameter_name=self.parameter_name,
            target_object=self.target_object,
            renderer=self.renderer,
        )

        self.label = arcade.gui.widgets.text.UILabel(
            text=self.parameter_name if self.label is None else self.label,
            text_color=arcade.color.BLACK,
            font_size=int(self.renderer.atomic_height / 2),
            font_name="arial",
        )
        FONT_SIZE = int(self.renderer.atomic_height / 2)
        primary_style = create_button_style(font_size=FONT_SIZE)
        active_style = create_button_style(font_size=FONT_SIZE)
        dropdown_style = create_button_style(font_size=FONT_SIZE)

        self.dropdown = arcade.gui.UIDropdown(
            default=str(value),
            options=[str(option) for option in self.options],
            width=self.renderer.atomic_width * 7,
            height=self.renderer.atomic_height,
            primary_style=primary_style,
            active_style=active_style,
            dropdown_style=dropdown_style,
        )
        self.dropdown.on_change = self.on_dropdown_change

    def update(self):
        self.current_value = get_current_parameter_value(
            parameter_name=self.parameter_name,
            target_object=self.target_object,
            renderer=self.renderer,
        )

    def on_dropdown_change(self, dropdown_event):
        if self.parameter_name != "target_fps":
            self.target_object = self.renderer.model

        new_parameter_value = dropdown_event.new_value

        setattr(
            self.target_object,
            self.parameter_name,
            new_parameter_value,
        )
        self.controller.parameter_value = new_parameter_value
        self.renderer.parameter_dict[self.parameter_name] = new_parameter_value
        self.update()

    def add_to_anchor(self):
        self.renderer.anchor.add(
            self.label,
            anchor_x="left",
            anchor_y="top",
            align_x=int(self.renderer.atomic_width),
            align_y=int(self.align_y + self.renderer.atomic_height),
        )
        self.renderer.anchor.add(
            self.dropdown,
            anchor_x="left",
            anchor_y="top",
            align_x=int(self.renderer.atomic_width),
            align_y=int(self.align_y),
        )


class NumControllerButtons(_ControllerButtons):
    def __init__(
        self,
        controller,
        align_y,
        renderer,
        parameter_name: str,
        value,
        min_value,
        max_value,
        step,
        label=None,
        target_object=None,
    ):
        self.controller = controller
        self.align_y = align_y
        self.renderer = renderer
        self.parameter_name = parameter_name
        self.parameter_value = value
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.label = label
        self.target_object = self.renderer.model if target_object is None else target_object

        self.current_value = get_current_parameter_value(
            parameter_name=self.parameter_name,
            target_object=self.target_object,
            renderer=self.renderer,
        )

        self.label = arcade.gui.widgets.text.UILabel(
            text=self.parameter_name if self.label is None else self.label,
            text_color=arcade.color.BLACK,
            font_size=int(self.renderer.atomic_height / 2),
            font_name="arial",
        )

        self.increase_button = ControllerButton(
            controller=self.controller,
            controller_buttons=self,
            renderer=renderer,
            parameter_name=parameter_name,
            increase=True,
            step=step,
        )
        self.decrease_button = ControllerButton(
            controller=self.controller,
            controller_buttons=self,
            renderer=renderer,
            parameter_name=parameter_name,
            increase=False,
            step=step,
        )
        self.label_current_value = arcade.gui.widgets.text.UILabel(
            text=str(self.current_value),
            text_color=arcade.color.BLACK,
            font_size=int(self.renderer.atomic_height / 2),
            font_name="arial",
        )
        self.slider = arcade.gui.UISlider(
            value=self.parameter_value,
            min_value=self.min_value,
            max_value=self.max_value,
            step=self.step,
            width=self.renderer.atomic_width * 7,
        )
        self.slider.on_change = self.on_slider_change

        self.slider.style["normal"].bg = arcade.color.LIGHT_GRAY
        self.slider.style["hover"].bg = arcade.color.LIGHT_GRAY
        self.slider.style["press"].bg = arcade.color.LIGHT_GRAY

        self.slider.style["normal"].filled_track = arcade.color.BATTLESHIP_GREY
        self.slider.style["hover"].filled_track = arcade.color.BATTLESHIP_GREY
        self.slider.style["press"].filled_track = arcade.color.BATTLESHIP_GREY

        self.slider.style["normal"].filled_step = arcade.color.BLACK
        self.slider.style["hover"].filled_step = arcade.color.BLACK
        self.slider.style["press"].filled_step = arcade.color.BLACK

        self.slider.style["normal"].unfilled_step = arcade.color.BLACK
        self.slider.style["hover"].unfilled_step = arcade.color.BLACK
        self.slider.style["press"].unfilled_step = arcade.color.BLACK

        self.slider.style["normal"].border = arcade.color.BLACK
        self.slider.style["hover"].border = arcade.color.BLACK
        self.slider.style["press"].border = arcade.color.BLACK

        self.slider.style["normal"].border_width = 2
        self.slider.style["hover"].border_width = 3
        self.slider.style["press"].border_width = 4
        self.update()

    def update(self):
        self.current_value = get_current_parameter_value(
            parameter_name=self.parameter_name,
            target_object=self.target_object,
            renderer=self.renderer,
        )
        self.label_current_value.text = self.current_value
        self.slider.value = self.current_value

    def on_slider_change(self, slider_event):
        if self.parameter_name != "target_fps":
            self.target_object = self.renderer.model

        new_parameter_value = slider_event.new_value
        new_parameter_value = round_parameter_value(new_parameter_value, self.controller.step)

        set_new_parameter_value(
            parameter_name=self.parameter_name,
            new_value=new_parameter_value,
            target_object=self.target_object,
            renderer=self.renderer,
            controller=self.controller,
        )
        self.update()

    def add_to_anchor(self):
        ALIGN_X = self.renderer.atomic_width

        self.renderer.anchor.add(
            self.label,
            anchor_x="left",
            anchor_y="top",
            align_x=ALIGN_X,
            align_y=int(self.align_y + self.renderer.atomic_height),
        )
        self.renderer.anchor.add(
            self.decrease_button,
            anchor_x="left",
            anchor_y="top",
            align_x=ALIGN_X + self.renderer.atomic_width * 4,
            align_y=self.align_y + self.renderer.atomic_height,
        )
        self.renderer.anchor.add(
            self.increase_button,
            anchor_x="left",
            anchor_y="top",
            align_x=ALIGN_X + self.renderer.atomic_width * 4 + self.renderer.small_button_width,
            align_y=self.align_y + self.renderer.atomic_height,
        )
        self.renderer.anchor.add(
            self.label_current_value,
            anchor_x="left",
            anchor_y="top",
            align_x=ALIGN_X + self.renderer.atomic_width * 6,
            align_y=self.align_y + self.renderer.atomic_height,
        )
        self.renderer.anchor.add(
            self.slider,
            anchor_x="left",
            anchor_y="top",
            align_x=ALIGN_X,
            align_y=self.align_y + self.renderer.atomic_height * 0.19,
        )
