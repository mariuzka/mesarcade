import mesa
import pytest
from arcade.gui import UIOnChangeEvent

import mesarcade as mesar


class DummyModel(mesa.Model):
    def __init__(self, option):
        super().__init__()
        self.option = option


@pytest.mark.parametrize(
    "options, old, new",
    [
        ([True, False], True, False),
        ([1, 2, 3], 1, 3),
        ([0.5, 1.5], 0.5, 1.5),
        (["a", "b"], "a", "b"),
    ],
)
def test_cat_controller_keeps_option_types(options, old, new):
    """The dropdown works with strings, but the model must get the original values."""
    controller = mesar.CatController("option", old, options)
    canvas = mesar.Canvas(model_class=DummyModel, controllers=[controller], _visible=False)
    canvas._setup()

    buttons = controller.buttons
    buttons.on_dropdown_change(UIOnChangeEvent(buttons.dropdown, str(old), str(new)))

    model = canvas.renderer.model
    assert model.option == new
    assert type(model.option) is type(new)

    # the selected value is used for new model instances as well
    canvas.renderer.default_buttons.reset_button.on_click(None)
    model = canvas.renderer.model
    assert model.option == new
    assert type(model.option) is type(new)

    canvas.window.close()
