from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mesarcade")
except PackageNotFoundError:
    __version__ = "unknown"

from .artist import (
    CellAgentArtists,
    CellArtists,
    ContinuousSpaceAgentArtists,
    NetworkAgentArtists,
    NetworkCellArtists,
)
from .canvas import Canvas
from .controller import CatController, NumController
from .history_plot import ModelHistoryPlot
from .space_plot import ContinuousSpacePlot, GridSpacePlot, NetworkPlot
from .value_display import ValueDisplay

__all__ = [
    "Canvas",
    "CatController",
    "CellAgentArtists",
    "CellArtists",
    "ContinuousSpaceAgentArtists",
    "ContinuousSpacePlot",
    "GridSpacePlot",
    "ModelHistoryPlot",
    "NetworkAgentArtists",
    "NetworkCellArtists",
    "NetworkPlot",
    "NumController",
    "ValueDisplay",
]
