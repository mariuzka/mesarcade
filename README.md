# Mesa-arcade

Mesa-arcade is a Python package which uses Arcade to visualize simulations built with Mesa.

## Components

To visualize Mesa models, Mesa-arcade offers several components which can/must be combined by you:

### Artists

Artists are the visual representations of the entities in a mesa model.

- `CellArtists`: A visual representation for `mesa.Cell` and `mesa.Property_Layer`.
- `CellAgentArtists`: A visual representation for a set of `mesa.CellAgent`s.
- `ContinuousSpaceAgentArtists`: A visual representation for a set of `mesa.ContinuousSpaceAgent`s.

**Example:**

```python
agents = mesar.CellAgentArtists(
    color_attribute="type",
    color_map={0: "blue", 1: "red"},
)
```

<br>

# SpacePlots

SpacePlots are visual representations of certain space types in Mesa and plot the corresponding `Artist`s at their position.
You can add/layer as many artists as you want to.

- `GridSpacePlot`: Visualizes a grid.
- `ContinuousSpacePlot`: Visualizes a continuous space.

**Example:**

Let's create a visual representation of a grid and add our a agent artists.
We could add other artists, too.

```python
grid_space = mesar.GridSpacePlot(artists=[agents])
```

<br>

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

Interactive controllers of model attributes / parameters.

- `NumController`: A controller for metric parameters.
- `CatController`: A controlelr for categorial paremeters.

**Example

### Canvas

The `Canvas` is the main window in which all components are placed.

## Full example

```{python}
import mesa_arcade as mesar
from mesa.examples.basic.schelling.model import Schelling

# artists
agents = mesar.CellAgentArtists(
    color_attribute="type",
    color_map={0: "blue", 1: "red"},
    shape="circle",
)

# space plot
space = mesar.GridSpacePlot(artists=agents)

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