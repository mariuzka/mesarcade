from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("mesarcade")
except PackageNotFoundError:
    __version__ = "unknown"

from .canvas import Canvas
from .controller import NumController, CatController
from .artist import (
    CellAgentArtists,
    CellArtists,
    ContinuousSpaceAgentArtists,
    NetworkCellArtists,
    NetworkAgentArtists,
)
from .history_plot import ModelHistoryPlot
from .space_plot import GridSpacePlot, ContinuousSpacePlot, NetworkPlot
from .value_display import ValueDisplay

__all__ = [
    "Canvas",
    "CatController",
    "CellArtists",
    "CellAgentArtists",
    "ContinuousSpaceAgentArtists",
    "ModelHistoryPlot",
    "NumController",
    "GridSpacePlot",
    "ContinuousSpacePlot",
    "ValueDisplay",
    "NetworkCellArtists",
    "NetworkAgentArtists",
    "NetworkPlot",
]
