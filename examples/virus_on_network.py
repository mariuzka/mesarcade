import mesarcade as mesar
from mesa.examples.basic.virus_on_network.model import VirusOnNetwork
import networkx as nx

nodes = mesar.NetworkCellAgentArtists(networkx_layout=nx.kamada_kawai_layout)

# space plot
space_plot = mesar.NetworkPlot(artists=[nodes])

# line plot
sir_plot = mesar.ModelHistoryPlot(
    model_attributes=["Infected", "Susceptible", "Resistant"],
    )

# controllers
num_nodes = mesar.NumController(
    parameter_name="num_nodes",
    parameter_value=10,
    min_value=10,
    max_value=1000,
    step=50,
    )

# gui window
canvas = mesar.Canvas(
    model_class=VirusOnNetwork,
    plots=[space_plot, sir_plot],
    controllers=[num_nodes]
)

# show gui window
canvas.show()
