import mesa_arcade as mesar
from mesa.examples.advanced.sugarscape_g1mt.model import SugarscapeG1mt

# artists
agents = mesar.CellAgentArtists(
    shape="circle",
    )
sugar = mesar.CellArtists(
    color_attribute="sugar",
    color_map="Greens",
    color_vmin=0,
    color_vmax=5,
    jitter=True,
    size=0.3,
    entity_selector=lambda cell: cell.sugar > 0,
    )
spice = mesar.CellArtists(
    color_attribute="spice",
    color_map="Reds",
    color_vmin=0,
    color_vmax=5,
    jitter=True,
    size=0.3,
    entity_selector=lambda cell: cell.spice > 0,
    )

# space plot
space_plot = mesar.GridSpacePlot(artists=[sugar, spice, agents])

# line plots
price_plot = mesar.ModelHistoryPlot(y_attributes=["Price"])
traders_plot = mesar.ModelHistoryPlot(y_attributes=["#Traders"])

# controllers
density = mesar.NumController("density", 0.8, 0.1, 0.9, 0.1)

# gui window
canvas = mesar.Canvas(
    model_class=SugarscapeG1mt,
    plots=[
        space_plot,
        price_plot,
        traders_plot,
        ],
    controllers=[
    ]
)

# show gui window
canvas.show()