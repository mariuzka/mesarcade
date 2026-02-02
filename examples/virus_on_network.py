import mesarcade as mesar
from mesa.examples.basic.virus_on_network.model import VirusOnNetwork
import networkx as nx

# network artists (draws nodes and edges)
network = mesar.NetworkAgentArtists(
    networkx_layout=nx.spring_layout,
    get_color_attr = lambda node: node.state.value,
    color_map={
        0: "green",
        1: "red",
        2: "blue",
    }
    )

# space plot
network_plot = mesar.NetworkPlot(artists=[network])

# line plot
sir_plot = mesar.ModelHistoryPlot(
    model_attributes=["Susceptible", "Infected", "Resistant"],
    colors=["green", "red", "blue"],
    )

# controllers
num_nodes = mesar.NumController("num_nodes", 10, 10, 1000, 10)
avg_node_degree = mesar.NumController("avg_node_degree", 3, 1, 10, 1)
initial_outbreak_size = mesar.NumController("initial_outbreak_size", 1, 1, 10, 1, "initial outbreak")
virus_spread_chance = mesar.NumController("virus_spread_chance", 0.4, 0.0, 1.0, 0.1)
virus_check_frequency = mesar.NumController("virus_check_frequency", 0.4, 0.0, 1.0, 0.1, "virus check freq")
recovery_chance = mesar.NumController("recovery_chance", 0.3, 0.0, 1.0, 0.1)
gain_resistance_chance = mesar.NumController("gain_resistance_chance", 0.5, 0.0, 1.0, 0.1, "resistance prob.")

# gui window
canvas = mesar.Canvas(
    model_class=VirusOnNetwork,
    plots=[
        network_plot, 
        sir_plot,
        ],
    controllers=[
        num_nodes,
        avg_node_degree,
        initial_outbreak_size,
        virus_spread_chance,
        virus_check_frequency,
        recovery_chance,
        gain_resistance_chance,
    ]
)

# show gui window
canvas.show()
