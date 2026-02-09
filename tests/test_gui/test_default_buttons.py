from mesa.examples.basic.schelling.model import Schelling
import mesarcade as mesar

def test_play_button():
    canvas = mesar.Canvas(
        model_class=Schelling,
        _visible=False,
    )
    canvas._setup()
    
    for _ in range(10):
        canvas.renderer.on_update(None)

    assert canvas.renderer.play == False
    assert canvas.renderer.tick == 0

    canvas.renderer.default_buttons.play_button.on_click(None)
    
    for _ in range(10):
        canvas.renderer.on_update(None)
    
    assert canvas.renderer.play == True
    assert canvas.renderer.tick == 10

    canvas.renderer.default_buttons.play_button.on_click(None)
    
    assert canvas.renderer.play == False
    assert canvas.renderer.tick == 10

    canvas.window.close()


def test_reset_button():
    canvas = mesar.Canvas(
        model_class=Schelling,
        _visible=False,
    )
    canvas._setup()
    canvas.renderer.play = True
    
    assert canvas.renderer.tick == 0

    for _ in range(10):
        canvas.renderer.on_update(None)
    
    assert canvas.renderer.tick == 10

    canvas.renderer.default_buttons.reset_button.on_click(None)

    assert canvas.renderer.tick == 0

    canvas.window.close()


def test_step_button():
    canvas = mesar.Canvas(
        model_class=Schelling,
        _visible=False,
    )
    canvas._setup()

    assert canvas.renderer.tick == 0

    for _ in range(15):
        canvas.renderer.default_buttons.step_button.on_click(None)

    assert canvas.renderer.tick == 15

    canvas.window.close()