import arcade
import arcade.gui

from mesarcade import styles
from mesarcade.styles import create_button_style, create_primary_button_style


class SmallButton(arcade.gui.UIFlatButton):
    def __init__(self, renderer):
        font_size = renderer.small_button_height / 1.5
        super().__init__(style=create_button_style(font_size=font_size))
        self.renderer = renderer
        self.height = self.renderer.small_button_height
        self.width = self.renderer.small_button_width
        self.setup()
        self.renderer.text_layer.add_caption(self, font_size=font_size, color=styles.TEXT)

    def setup(self):
        pass


class BigButton(arcade.gui.UIFlatButton):
    def __init__(self, renderer):
        self.font_size = renderer.big_button_height / 3.2
        super().__init__(style=create_button_style(font_size=self.font_size))
        self.renderer = renderer
        self.height = self.renderer.big_button_height
        self.width = self.renderer.big_button_width
        self.caption = self.renderer.text_layer.add_caption(
            self, font_size=self.font_size, color=styles.TEXT
        )
        self.setup()

    def setup(self):
        pass

    def set_primary(self, primary: bool) -> None:
        """Switches between the accent colored and the default button style."""
        style_factory = create_primary_button_style if primary else create_button_style
        self.style = style_factory(font_size=self.font_size)
        self.caption.crisp_text.color = styles.TEXT_ON_ACCENT if primary else styles.TEXT
        self.trigger_full_render()


class PlayButton(BigButton):
    def setup(self):
        self.get_text()

    def get_text(self):
        # highlighted while the simulation is running, default style while paused
        self.text = "Play" if not self.renderer.play else "Pause"
        self.set_primary(self.renderer.play)

    def on_click(self, event):
        self.renderer.update_value_displays(force_update=True)
        self.renderer.play = not self.renderer.play
        self.get_text()


class StepButton(BigButton):
    def setup(self):
        self.text = "Step"

    def on_click(self, event):
        self.renderer.model.step()
        self.renderer.tick += 1
        self.renderer.update_figures()
        self.renderer.update_value_displays(force_update=True)


class ResetButton(BigButton):
    def setup(self):
        self.text = "Reset"

    def on_click(self, event):
        self.renderer.setup_model()
        self.renderer.update_value_displays(force_update=True)


class DefaultButtons:
    def __init__(self, renderer):
        self.renderer = renderer
        self.align_y = -self.renderer.atomic_height
        self.play_button = PlayButton(renderer=self.renderer)
        self.step_button = StepButton(renderer=self.renderer)
        self.reset_button = ResetButton(renderer=self.renderer)

    def add_to_anchor(self):
        self.renderer.anchor.add(
            self.play_button,
            anchor_x="left",
            anchor_y="top",
            align_y=self.align_y,
            align_x=self.renderer.atomic_width * 1.5,
        )
        self.renderer.anchor.add(
            self.step_button,
            anchor_x="left",
            anchor_y="top",
            align_y=self.align_y,
            align_x=self.renderer.atomic_width * 3.5,
        )
        self.renderer.anchor.add(
            self.reset_button,
            anchor_x="left",
            anchor_y="top",
            align_y=self.align_y,
            align_x=self.renderer.atomic_width * 5.5,
        )
