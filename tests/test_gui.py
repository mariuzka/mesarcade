import mesarcade as mesar
from mesa.examples.advanced.sugarscape_g1mt.model import SugarscapeG1mt
from mesa.examples.basic.schelling.model import Schelling
from mesa.examples.basic.virus_on_network.model import VirusOnNetwork

import networkx as nx


def run_gui_test(canvas, n_steps=10):
    """Setup canvas, run n model steps with rendering, then close."""
    canvas._setup()
    canvas.renderer.play = True
    
    for _ in range(n_steps):
        canvas.renderer.on_update(1 / 40)
        canvas.renderer.on_draw()

    canvas.window.close()


def test_schelling():
    agents = mesar.CellAgentArtists(
        get_color_attr=lambda agent: agent.type,
        color_map={0: "blue", 1: "red"},
        shape="circle",
    )
    space = mesar.GridSpacePlot(artists=[agents])
    happy_plot = mesar.ModelHistoryPlot(model_attributes=["happy"], labels=["Happy agents"])
    happy_value = mesar.ValueDisplay(model_attribute="happy", label="Happy agents")

    density = mesar.NumController("density", 0.8, 0.1, 0.9, 0.1)
    homophily = mesar.NumController("homophily", 0.4, 0.0, 1.0, 0.125)

    canvas = mesar.Canvas(
        model_class=Schelling,
        plots=[space, happy_plot],
        value_displays=[happy_value],
        controllers=[density, homophily],
        _visible=False,
    )
    run_gui_test(canvas)


def test_sugarscape():
    agents = mesar.CellAgentArtists(shape="circle")
    sugar = mesar.CellArtists(
        get_color_attr=lambda cell: cell.sugar,
        color_map="Greens",
        color_vmin=0,
        color_vmax=5,
        jitter=True,
        size=0.3,
        filter_entities=lambda cell: cell.sugar > 0,
    )
    spice = mesar.CellArtists(
        get_color_attr=lambda cell: cell.spice,
        color_map="Reds",
        color_vmin=0,
        color_vmax=5,
        jitter=True,
        size=0.3,
        filter_entities=lambda cell: cell.spice > 0,
    )

    space_plot = mesar.GridSpacePlot(artists=[sugar, spice, agents])
    price_plot = mesar.ModelHistoryPlot(model_attributes=["Price"])
    traders_plot = mesar.ModelHistoryPlot(model_attributes=["#Traders"])

    canvas = mesar.Canvas(
        model_class=SugarscapeG1mt,
        plots=[space_plot, price_plot, traders_plot],
        _visible=False,
    )
    run_gui_test(canvas)

def test_virus_on_network():
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
        ],
        _visible=False,
    )
    run_gui_test(canvas)