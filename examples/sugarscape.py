import mesa_arcade as mesar
from mesa.examples.advanced.sugarscape_g1mt.model import SugarscapeG1mt

# agents
agents = mesar.CellAgentArtists(
    shape="circle",
    color="black",
)

# sugar cells
sugar = mesar.CellArtists(
    color_attribute="sugar",
    color_map="Greens",
    color_vmin=0,
    color_vmax=4,
    jitter=True,
    size=0.5,
    entity_selector=lambda cell: cell.sugar > 0,
)

# spice cells
spice = mesar.CellArtists(
    color_attribute="spice",
    color_map="Reds",
    color_vmin=0,
    color_vmax=4,
    jitter=True,
    size=0.5,
    entity_selector=lambda cell: cell.spice > 0,
)

# space plot
space_plot = mesar.GridSpacePlot(artists=[sugar, spice, agents])

# line plots
price_plot = mesar.ModelHistoryPlot(y_attributes=["Price"])
traders_plot = mesar.ModelHistoryPlot(y_attributes=["#Traders", "Trade Volume"])

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
        space_plot, 
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
