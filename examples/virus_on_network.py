import mesarcade as mesar
from mesa.examples.basic.virus_on_network.model import VirusOnNetwork
import networkx as nx

nodes = mesar.NetworkCellAgentArtists()

# space plot
space_plot = mesar.NetworkPlot(artists=[nodes])

# gui window
canvas = mesar.Canvas(
    model_class=VirusOnNetwork,
    plots=[space_plot],
)

# show gui window
canvas.show()
