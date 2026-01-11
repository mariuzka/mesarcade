from mesa.examples.basic.boid_flockers.model import BoidFlockers
import mesa_arcade as mesar

# artists
birds = mesar.ContinuousSpaceAgentArtists()

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
    )

# show gui window
canvas.show()