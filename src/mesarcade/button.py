import arcade
import arcade.gui

from mesarcade.styles import create_button_style


class SmallButton(arcade.gui.UIFlatButton):
    def __init__(self, renderer):
        super().__init__(
            style=create_button_style(font_size=renderer.small_button_height / 1.5),
        )
        self.renderer = renderer
        self.height = self.renderer.small_button_height
        self.width = self.renderer.small_button_width
        self.setup()

    def setup(self):
        pass


class BigButton(arcade.gui.UIFlatButton):
    def __init__(self, renderer):
        super().__init__(
            style=create_button_style(font_size=renderer.big_button_height / 3.5),
        )
        self.renderer = renderer
        self.height = self.renderer.big_button_height
        self.width = self.renderer.big_button_width
        self.setup()

    def setup(self):
        pass


class PlayButton(BigButton):
    def setup(self):
        self.get_text()

    def get_text(self):
        self.text = "Play" if not self.renderer.play else "Pause"

    def on_click(self, event):
        self.renderer.play = not self.renderer.play
        self.get_text()


class StepButton(BigButton):
    def setup(self):
        self.text = "Step"

    def on_click(self, event):
        self.renderer.model.step()
        self.renderer.tick += 1
        for figure in self.renderer.figures:
            figure.update()


class ResetButton(BigButton):
    def setup(self):
        self.text = "Reset"

    def on_click(self, event):
        self.renderer.setup_model()


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
