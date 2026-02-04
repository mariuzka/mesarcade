import mesarcade as mesar
from mesa.examples.basic.conways_game_of_life.model import ConwaysGameOfLife

# artists
agents = mesar.CellAgentArtists(
    color_attribute="state",
    color_map={0: "white", 1: "black"},
    shape="rect",
    dynamic_position=False,
    dynamic_population=False,
)

# space plot
space = mesar.GridSpacePlot(artists=[agents])

# line plot
dead_alive_plot = mesar.ModelHistoryPlot(
    model_attributes=[
        lambda model: len([agent for agent in model.agents if agent.state == 0]),
        lambda model: len([agent for agent in model.agents if agent.state == 1]),
    ],
    labels=["n cells dead", "n cells alive"],
)

# value displays
n_dead = mesar.ValueDisplay(
    model_attribute=lambda model: len([agent for agent in model.agents if agent.state == 0]),
    label="n dead",
)

# controllers
initial_fraction_alive = mesar.NumController("initial_fraction_alive", 0.5, 0.0, 1.0, 0.1)
width = mesar.NumController("width", 50, 10, 200, 10)
height = mesar.NumController("height", 50, 10, 200, 10)

# gui window
canvas = mesar.Canvas(
    model_class=ConwaysGameOfLife,
    plots=[space, dead_alive_plot],
    controllers=[initial_fraction_alive, width, height],
    value_displays=[n_dead],
)

# show gui window
canvas.show()
