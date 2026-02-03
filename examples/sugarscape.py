import mesarcade as mesar
from mesa.examples.advanced.sugarscape_g1mt.model import SugarscapeG1mt

# agents
agents_on_sugar = mesar.CellAgentArtists(
    shape="circle",
    color="black",
)

agents_on_spice = mesar.CellAgentArtists(
    shape="circle",
    color="black",
)

# sugar cells
sugar = mesar.CellArtists(
    get_color_attr=lambda cell: cell.sugar,
    color_map="Greens",
    color_vmin=0,
    color_vmax=4,
)

# spice cells
spice = mesar.CellArtists(
    get_color_attr=lambda cell: cell.spice,
    color_map="Reds",
    color_vmin=0,
    color_vmax=4,
)

# space plot
spice_space = mesar.GridSpacePlot(artists=[spice, agents_on_spice], title="Sugar")
sugar_space = mesar.GridSpacePlot(artists=[sugar, agents_on_sugar], title="Spice")

# line plots
price_plot = mesar.ModelHistoryPlot(model_attributes=["Price"], from_datacollector=True)
traders_plot = mesar.ModelHistoryPlot(
    model_attributes=["#Traders", "Trade Volume"], from_datacollector=True
)

# controllers
initial_population = mesar.NumController("initial_population", 200, 50, 500, 10)
endowment_min = mesar.NumController("endowment_min", 50, 30, 100, 1)
endowment_max = mesar.NumController("endowment_max", 50, 30, 100, 1)
metabolism_min = mesar.NumController("metabolism_min", 1, 1, 3, 1)
metabolism_max = mesar.NumController("metabolism_max", 5, 3, 8, 1)
vision_min = mesar.NumController("vision_min", 1, 1, 3, 1)
vision_max = mesar.NumController("vision_max", 5, 3, 8, 1)
enable_trade = mesar.CatController("enable_trade", True, [True, False])

# gui window
canvas = mesar.Canvas(
    model_class=SugarscapeG1mt,
    plots=[
        spice_space,
        sugar_space,
        price_plot,
        traders_plot,
    ],
    controllers=[
        initial_population,
        endowment_min,
        endowment_max,
        metabolism_min,
        metabolism_max,
        enable_trade,
        vision_min,
        vision_max,
    ],
)

# show gui window
canvas.show()
