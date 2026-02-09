from mesa.examples.basic.boid_flockers.model import BoidFlockers
import mesarcade as mesar
from dataclasses import dataclass


@dataclass
class Event:
    new_value: float


def create_canvas():
    population_size_controller = mesar.NumController(
        "population_size",
        100,
        25,
        1000,
        25,
        "n birds",
    )
    canvas = mesar.Canvas(
        model_class=BoidFlockers,
        controllers=[population_size_controller],
        _visible=False,
    )
    canvas._setup()
    return canvas


def test_num_controller_buttons():
    canvas = create_canvas()

    controller = canvas.renderer.controllers[0]

    # test basic setup
    assert controller.parameter_name == "population_size"
    assert controller.label == "n birds"
    assert controller.parameter_value == 100

    # test increase
    controller.buttons.increase_button.on_click(None)
    assert controller.parameter_value == 125
    assert canvas.renderer.parameter_dict["population_size"] == 125

    # test decrease
    controller.buttons.decrease_button.on_click(None)
    assert controller.parameter_value == 100
    assert canvas.renderer.parameter_dict["population_size"] == 100

    # test maximum
    for _ in range(500):
        controller.buttons.increase_button.on_click(None)

    assert controller.parameter_value == 1000
    assert canvas.renderer.parameter_dict["population_size"] == 1000

    # test minimum
    for _ in range(500):
        controller.buttons.decrease_button.on_click(None)

    assert controller.parameter_value == 25
    assert canvas.renderer.parameter_dict["population_size"] == 25

    canvas.window.close()


def test_num_controller_slider():
    canvas = create_canvas()

    controller = canvas.renderer.controllers[0]

    assert controller.parameter_value == 100

    controller.buttons.slider.on_change(Event(new_value=200))

    assert controller.parameter_value == 200

    canvas.window.close()


def test_increase_and_reset():
    canvas = create_canvas()

    controller = canvas.renderer.controllers[0]

    assert len(canvas.renderer.model.agents) == 100

    # increase by 25
    controller.buttons.increase_button.on_click(None)

    # restart model
    canvas.renderer.default_buttons.reset_button.on_click(None)

    assert len(canvas.renderer.model.agents) == 125

    canvas.window.close()
