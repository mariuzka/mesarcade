from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from mesarcade.figure import Figure

if TYPE_CHECKING:
    import mesa
    from mesarcade.artist import Artist


class GridSpacePlot(Figure):
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
