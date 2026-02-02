from mesarcade.figure import Figure


class GridSpacePlot(Figure):
    def __init__(
        self, 
        artists=[], 
        background_color="white", 
        title=None, 
        get_space=lambda model: model.grid,
        ):
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
        artists=[], 
        background_color="white", 
        title=None, 
        get_space=lambda model: model.space,
        ):
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
        artists=[], 
        background_color="white", 
        title=None, 
        get_space=lambda model: model.grid,
        ):
        if not isinstance(artists, (list, tuple)):
            artists = [artists]

        super().__init__(
            components=artists,
            background_color=background_color,
            title=title,
            get_space=get_space,
            figure_type="network",
        )