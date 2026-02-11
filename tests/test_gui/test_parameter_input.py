from mesa.examples.basic.schelling.model import Schelling
import mesa
import mesarcade as mesar

def test_parameter_input():

    class TestModel(mesa.Model):
        def __init__(self, radius, width, height):
            self.radius = radius
            self.width = width
            self.height = height

    canvas = mesar.Canvas(
        model_class=TestModel,
        params={"radius": 99, "width": 500, "height": 500},
        _visible=False,
    )

    canvas._setup()
    
    model = canvas.renderer.model
    assert model.radius == 99
    assert model.width == 500
    assert model.height == 500

    model.radius = 1
    model.width = 2
    model.height = 3

    canvas.renderer.default_buttons.reset_button.on_click(None)

    model = canvas.renderer.model
    assert model.radius == 99
    assert model.width == 500
    assert model.height == 500


def test_parameter_input_with_controller():

    class TestModel(mesa.Model):
        def __init__(self, radius):
            self.radius = radius

    radius_controller = mesar.NumController(
        parameter_name="radius",
        parameter_value=44,
        min_value=0,
        max_value=100,
        step=99,
    )
    canvas = mesar.Canvas(
        model_class=TestModel,
        params={"radius": 99},
        controllers=[radius_controller],
        _visible=False,
    )
    canvas._setup()
    
    model = canvas.renderer.model
    assert model.radius == 44