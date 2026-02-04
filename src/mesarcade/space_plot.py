from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from mesarcade.figure import Figure

if TYPE_CHECKING:
    import mesa
    from mesarcade.artist import Artist


class GridSpacePlot(Figure):
    """A plot for visualizing cell-based grid spaces.

    Displays agents and/or cells on a discrete grid. The grid dimensions
    are automatically determined from the space.

    Args:
        artists: Artist(s) defining how to render entities (e.g., CellAgentArtists).
        background_color: Background color of the plot area.
        title: Optional title displayed above the plot.
        get_space: Callable returning the grid space from the model.
    """

    def __init__(
        self,
        artists: Artist | list[Artist] = [],
        background_color: str | tuple[int, int, int] | tuple[int, int, int, int] = "white",
        title: str | None = None,
        get_space: Callable[[mesa.Model], Any] = lambda model: model.grid,
    ) -> None:
        if not isinstance(artists, (list, tuple)):
            artists = [artists]

        super().__init__(
            components=artists,
            background_color=background_color,
            title=title,
            get_space=get_space,
            figure_type="grid",
        )


class ContinuousSpacePlot(Figure):
    """A plot for visualizing continuous 2D spaces.

    Displays agents that move freely in continuous space. Agent positions
    are scaled to fit the plot area based on the space dimensions.

    Args:
        artists: Artist(s) defining how to render entities (e.g., ContinuousSpaceAgentArtists).
        background_color: Background color of the plot area.
        title: Optional title displayed above the plot.
        get_space: Callable returning the continuous space from the model.
    """

    def __init__(
        self,
        artists: Artist | list[Artist] = [],
        background_color: str | tuple[int, int, int] | tuple[int, int, int, int] = "white",
        title: str | None = None,
        get_space: Callable[[mesa.Model], Any] = lambda model: model.space,
    ) -> None:
        if not isinstance(artists, (list, tuple)):
            artists = [artists]

        super().__init__(
            components=artists,
            background_color=background_color,
            title=title,
            get_space=get_space,
            figure_type="continuous",
        )


class NetworkPlot(Figure):
    """A plot for visualizing network/graph-based spaces.

    Displays agents and/or nodes on a network graph. Node positions are
    computed using a networkx layout algorithm specified in the artist.

    Args:
        artists: Artist(s) defining how to render entities (e.g., NetworkCellArtists).
        background_color: Background color of the plot area.
        title: Optional title displayed above the plot.
        get_space: Callable returning the network grid from the model.
    """

    def __init__(
        self,
        artists: Artist | list[Artist] = [],
        background_color: str | tuple[int, int, int] | tuple[int, int, int, int] = "white",
        title: str | None = None,
        get_space: Callable[[mesa.Model], Any] = lambda model: model.grid,
    ) -> None:
        if not isinstance(artists, (list, tuple)):
            artists = [artists]

        super().__init__(
            components=artists,
            background_color=background_color,
            title=title,
            get_space=get_space,
            figure_type="network",
        )
