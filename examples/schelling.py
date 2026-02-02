import mesarcade as mesar
from mesa.examples.basic.schelling.model import Schelling

# artists
agents = mesar.CellAgentArtists(
    get_color_attr = lambda agent: agent.type,
    color_map={0: "blue", 1: "red"},
    shape="circle",
)

# space plot
space = mesar.GridSpacePlot(artists=agents)

# line plot
happy_plot = mesar.ModelHistoryPlot(model_attributes=["happy"], labels=["Happy agents"])

# value display
happy_value = mesar.ValueDisplay(model_attribute="happy", label="Happy agents")

# controllers
density = mesar.NumController("density", 0.8, 0.1, 0.9, 0.1)
minority_pc = mesar.NumController("minority_pc", 0.2, 0.0, 1.0, 0.05)
homophily = mesar.NumController("homophily", 0.4, 0.0, 1.0, 0.125)
width = mesar.NumController("width", 100, 10, 200, 10)
height = mesar.NumController("height", 100, 10, 200, 10)

# gui window
canvas = mesar.Canvas(
    model_class=Schelling,
    plots=[space, happy_plot],
    value_displays=[happy_value],
    controllers=[density, minority_pc, homophily, width, height],
)

# show gui window
canvas.show()
