import mesarcade as mesar
from mesa.examples.advanced.sugarscape_g1mt.model import SugarscapeG1mt
from mesa.examples.basic.schelling.model import Schelling
from mesa.examples.basic.virus_on_network.model import VirusOnNetwork
from mesa.examples.basic.conways_game_of_life.model import ConwaysGameOfLife
from mesa.examples.basic.boid_flockers.model import BoidFlockers

import networkx as nx


def run_gui_test(canvas, n_steps=10):
    """Setup canvas, run n model steps with rendering, then close."""
    canvas._setup()
    canvas.renderer.play = True

    for _ in range(n_steps):
        canvas.renderer.on_update(1 / 40)
        canvas.renderer.on_draw()

    canvas.window.close()


def test_boid_flockers():
    # artists
    birds = mesar.ContinuousSpaceAgentArtists(
        dynamic_color=False,
        dynamic_population=False,
    )

    # space plot
    space = mesar.ContinuousSpacePlot(artists=[birds])

    # controllers
    population_size = mesar.NumController("population_size", 100, 10, 1000, 50)
    speed = mesar.NumController("speed", 5, 1, 20, 1)
    vision = mesar.NumController("vision", 10, 1, 50, 1)
    separation = mesar.NumController("separation", 2, 1, 20, 1)

    # gui window
    canvas = mesar.Canvas(
        model_class=BoidFlockers,
        plots=[space],
        controllers=[population_size, speed, vision, separation],
        _visible=False,
    )

    run_gui_test(canvas)


def test_game_of_life():
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
        ylim=[0,1],
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
        _visible=False,
    )

    # show gui window
    run_gui_test(canvas)


def test_schelling():
    # artists
    agents = mesar.CellAgentArtists(
        color_attribute="type",
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
        _visible=False,
        
    )
    run_gui_test(canvas)


def test_sugarscape():
    agents = mesar.CellAgentArtists(shape="circle")
    sugar = mesar.CellArtists(
        color_attribute="sugar",
        color_map="Greens",
        color_vmin=0,
        color_vmax=5,
        jitter=True,
        size=0.3,
        filter_entities=lambda cell: cell.sugar > 0,
    )
    spice = mesar.CellArtists(
        color_attribute="spice",
        color_map="Reds",
        color_vmin=0,
        color_vmax=5,
        jitter=True,
        size=0.3,
        filter_entities=lambda cell: cell.spice > 0,
    )

    space_plot = mesar.GridSpacePlot(artists=[sugar, spice, agents])
    price_plot = mesar.ModelHistoryPlot(model_attributes=["Price"], from_datacollector=True)
    traders_plot = mesar.ModelHistoryPlot(model_attributes=["#Traders"], from_datacollector=True)

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
        color_attribute=lambda node: node.state.value,
        color_map={
            0: "green",
            1: "red",
            2: "blue",
        },
    )

    # space plot
    network_plot = mesar.NetworkPlot(artists=[network])

    # line plot
    sir_plot = mesar.ModelHistoryPlot(
        model_attributes=["Susceptible", "Infected", "Resistant"],
        colors=["green", "red", "blue"],
        from_datacollector=True,
    )

    # controllers
    num_nodes = mesar.NumController("num_nodes", 10, 10, 1000, 10)
    avg_node_degree = mesar.NumController("avg_node_degree", 3, 1, 10, 1)
    initial_outbreak_size = mesar.NumController(
        "initial_outbreak_size", 1, 1, 10, 1, "initial outbreak"
    )
    virus_spread_chance = mesar.NumController("virus_spread_chance", 0.4, 0.0, 1.0, 0.1)
    virus_check_frequency = mesar.NumController(
        "virus_check_frequency", 0.4, 0.0, 1.0, 0.1, "virus check freq"
    )
    recovery_chance = mesar.NumController("recovery_chance", 0.3, 0.0, 1.0, 0.1)
    gain_resistance_chance = mesar.NumController(
        "gain_resistance_chance", 0.5, 0.0, 1.0, 0.1, "resistance prob."
    )

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
