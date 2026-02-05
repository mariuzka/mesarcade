import mesarcade as mesar
from mesa.examples.basic.conways_game_of_life.model import ConwaysGameOfLife


def get_share_agents_alive(model):
    return round(len([agent for agent in model.agents if agent.state == 1]) / len(model.agents), 2)


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
    model_attributes=[get_share_agents_alive],
    labels=["share agents alive"],
    ylim=[0, 1],
)

# value displays
p_alive = mesar.ValueDisplay(
    model_attribute=get_share_agents_alive,
    label="share agents alive",
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
    value_displays=[p_alive],
)

# show gui window
canvas.show()
