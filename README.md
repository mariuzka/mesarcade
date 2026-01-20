# Mesarcade

**Mesa + Arcade**

Mesarcade is a Python package that provides fast, interactive visualizations of Mesa agent-based models using Python Arcade.  


⚠️ mesarcade is under active development. APIs may change.

## Components

mesarcade follows a compositional design: you define how agents are drawn (Artists), where they are drawn (SpacePlots), what is tracked over time (HistoryPlots), and how parameters can be changed (Controllers), all embedded in a Canvas.

### Artists

Artists are the visual representations of the entities in a mesa model.

- `CellArtists`: A visual representation for `mesa.Cell` and `mesa.Property_Layer`.
- `CellAgentArtists`: A visual representation for a set of `mesa.CellAgent`s.
- `ContinuousSpaceAgentArtists`: A visual representation for a set of `mesa.ContinuousSpaceAgent`s.

**Example:**

Let's create a visual representation for our CellAgents. We map the agent attribute `type` to the colors blue and red.

```python
agents = mesar.CellAgentArtists(
    color_attribute="type",
    color_map={0: "blue", 1: "red"},
)
```

### SpacePlots

SpacePlots are visual representations of certain space types in Mesa and plot the corresponding `Artist`s at their position.
You can add/layer as many artists as you want to.

- `GridSpacePlot`: Visualizes a grid.
- `ContinuousSpacePlot`: Visualizes a continuous space.

**Example:**

Let's create a visual representation of a grid and add our agent artists.
We could add other artists, too.

```python
grid_space = mesar.GridSpacePlot(artists=[agents])
```

### HistoryPlots

Line plots that plot (multiple) values as a function of the simulated time steps.

- `ModelHistoryPlot`: Plots model attributes and data that is collected using `mesa.DataCollector` as a function of the simulated time steps.

- (`AgentHistoryPlot`: On the ToDo-List.)

**Example**

Let's add a `ModelHistoryPlot` that visualizes the model attribute `happy` over time:

```python
happy_plot = mesar.ModelHistoryPlot(y_attributes=["happy"])
```

### Controllers

Interactive controllers of model attributes and parameters.

- `NumController`: A controller for numeric parameters.
- `CatController`: A controller for categorical paremeters.

**Example**

Let's add a controller that determines the value of the model parameter `homophily`:

```python
homophily = mesar.NumController(
    parameter_name="homophily", 
    parameter_value=0.4, 
    min_value=0,
    max_value=1,
    step=0.125,
    )
```

### Canvas

The `Canvas` is the main window in which all components are placed.

**Example**

```python
canvas = mesar.Canvas(
    model_class=Schelling, # the mesa model
    plots=[space, happy_plot], # all plots
    controllers=[density, minority_pc, homophily, width, height], # all controllers
)

# start the visualization
canvas.show()
```

## Full example

*More examples can be found in [`"/mesarcade/examples"`](https://github.com/mariuzka/mesarcade/tree/main/examples).*

```python
import mesa_arcade as mesar
from mesa.examples.basic.schelling.model import Schelling

# artists
agents = mesar.CellAgentArtists(
    color_attribute="type",
    color_map={0: "blue", 1: "red"},
    shape="circle",
)

# space plot
space = mesar.GridSpacePlot(artists=[agents])

# line plot
happy_plot = mesar.ModelHistoryPlot(y_attributes=["happy"])

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
    controllers=[density, minority_pc, homophily, width, height],
)

# show gui window
canvas.show()
```
