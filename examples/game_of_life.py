import mesarcade as mesar
from mesa.examples.basic.conways_game_of_life.model import ConwaysGameOfLife

# artists
agents = mesar.CellAgentArtists(
    get_color_attr = lambda agent: agent.state,
    color_map={0: "white", 1: "black"},
    shape="rect",
    dynamic_position=False,
    dynamic_population=False,
)

# space plot
space = mesar.GridSpacePlot(artists=[agents])

# controllers
initial_fraction_alive = mesar.NumController("initial_fraction_alive", 0.5, 0.0, 1.0, 0.1)
width = mesar.NumController("width", 50, 10, 200, 10)
height = mesar.NumController("height", 50, 10, 200, 10)

# gui window
canvas = mesar.Canvas(
    model_class=ConwaysGameOfLife,
    plots=[space],
    controllers=[initial_fraction_alive, width, height],
)

# show gui window
canvas.show()
