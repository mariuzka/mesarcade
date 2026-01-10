import mesa_arcade as mesarc
from mesa.examples.basic.schelling.model import Schelling

agents = mesarc.CellAgents(
    color_attribute="type",
    color_map={0: "blue", 1: "red"},
    shape="rect",
)
space_plot = mesarc.GridSpacePlot(artists=agents)

density = mesarc.NumController("density", 0.8, 0.1, 0.9, 0.1)
minority_pc = mesarc.NumController("minority_pc", 0.2, 0.0, 1.0, 0.05)
homophily = mesarc.NumController("homophily", 0.4, 0.0, 1.0, 0.125)
width = mesarc.NumController("width", 100, 10, 200, 10)
height = mesarc.NumController("height", 100, 10, 200, 10)

happy_plot = mesarc.ModelHistoryPlot("happy")

canvas = mesarc.Canvas(
    model_class=Schelling,
    plots=[space_plot, happy_plot],
    controllers=[
        density,
        minority_pc,
        homophily,
        width,
        height,
    ]
)
canvas.show()