import mesa_arcade as mesarc

from mesa.examples.advanced.sugarscape_g1mt.model import SugarscapeG1mt

agents = mesarc.CellAgentArtists(shape="circle")
sugar = mesarc.CellArtists(
    color_attribute="sugar",
    color_map="Greens",
    color_vmin=0,
    color_vmax=5,
    jitter=True,
    size=0.5,
    dynamic_population=True,
    entity_selector=lambda cell: cell.sugar > 0,
    )
spice = mesarc.CellArtists(
    color_attribute="spice",
    color_map="Reds",
    color_vmin=0,
    color_vmax=5,
    jitter=True,
    size=0.5,
    dynamic_population=True,
    entity_selector=lambda cell: cell.spice > 0,
    )

space_plot = mesarc.GridSpacePlot(artists=[sugar, spice, agents])

density = mesarc.NumController("density", 0.8, 0.1, 0.9, 0.1)

price_plot = mesarc.ModelHistoryPlot("Price")
traders_plot = mesarc.ModelHistoryPlot("#Traders")

canvas = mesarc.Canvas(
    model_class=SugarscapeG1mt,
    plots=[
        space_plot,
        price_plot,
        traders_plot,
        ],
    controllers=[
    ]
)
canvas.show()