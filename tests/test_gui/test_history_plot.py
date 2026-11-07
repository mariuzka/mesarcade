import math

import mesa
import pytest

import mesarcade as mesar


class DummyModel(mesa.Model):
    def __init__(self):
        super().__init__()
        self.values = []
        self.value = None

    def step(self):
        self.value = self.values.pop(0) if self.values else 1.0


@pytest.mark.parametrize("invalid", [None, math.nan, math.inf])
def test_history_plot_ignores_invalid_first_values(invalid):
    """Invalid first values must neither crash the plot nor break its y axis."""
    plot = mesar.ModelHistoryPlot(model_attributes=["value"], labels=["value"], rendering_step=1)
    canvas = mesar.Canvas(model_class=DummyModel, plots=[plot], _visible=False)
    canvas._setup()

    renderer = canvas.renderer
    renderer.model.value = invalid
    renderer.model.values = [invalid, 0.2, 0.5, 0.3]

    renderer.play = True
    for _ in range(10):
        renderer.on_update(0.02)

    history_plot = plot.components[0]
    assert history_plot.min_y == 0.2
    assert history_plot.max_y == 1.0
    assert history_plot.min_y_label.text == "0.2"
    assert history_plot.max_y_label.text == "1"
    assert all(
        math.isfinite(x) and math.isfinite(y) for x, y in history_plot.scaled_data_dict["value"]
    )

    canvas.window.close()
