import mesa_arcade as mesarc
from mesa.examples.basic.conways_game_of_life.model import ConwaysGameOfLife

# agents
agents = mesarc.CellAgents(
    color_attribute="state",
    color_map={0: "white", 1: "black"},
    dynamic_population=False,
    dynamic_color=True,
)

# space
space_plot = mesarc.GridSpacePlot(artists=[agents])

# controllers
initial_fraction_alive = mesarc.NumController("initial_fraction_alive", 0.5, 0.0, 1.0, 0.1)
width = mesarc.NumController("width", 50, 10, 200, 10)
height = mesarc.NumController("height", 50, 10, 200, 10)

# gui window
canvas = mesarc.Canvas(
    model_class=ConwaysGameOfLife,
    plots=[space_plot],
    controllers=[
        initial_fraction_alive,
        width,
        height,
    ]
)

# show window
canvas.show()