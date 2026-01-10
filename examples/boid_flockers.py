from mesa.examples.basic.boid_flockers.model import BoidFlockers
import mesa_arcade as mesarc

# agents
birds = mesarc.ContinuousSpaceAgentArtists()

# space
space = mesarc.ContinuousSpacePlot(artists=[birds])

# controllers
population_size = mesarc.NumController("population_size", 100, 10, 1000, 50)
speed = mesarc.NumController("speed", 5, 1, 20, 1)
vision = mesarc.NumController("vision", 10, 1, 50, 1)
separation = mesarc.NumController("separation", 2, 1, 20, 1)

# gui window
canvas = mesarc.Canvas(
    model_class=BoidFlockers,
    plots=[space],
    controllers=[population_size, speed, vision, separation],
    )

# show window
canvas.show()