from mesarcade.figure import Figure


class GridSpacePlot(Figure):
    def __init__(self, artists=[], background_color="white", title=None, space_attr_name="grid"):
        if not isinstance(artists, (list, tuple)):
            artists = [artists]

        super().__init__(
            components=artists,
            background_color=background_color,
            title=title,
            space_attr_name=space_attr_name,
            figure_type="grid",
        )


class ContinuousSpacePlot(Figure):
    def __init__(self, artists=[], background_color="white", title=None, space_attr_name="space"):
        if not isinstance(artists, (list, tuple)):
            artists = [artists]

        super().__init__(
            components=artists,
            background_color=background_color,
            title=title,
            space_attr_name=space_attr_name,
            figure_type="continuous",
        )

class NetworkPlot(Figure):
    def __init__(self, artists=[], background_color="white", title=None, space_attr_name="grid"):
        if not isinstance(artists, (list, tuple)):
            artists = [artists]

        super().__init__(
            components=artists,
            background_color=background_color,
            title=title,
            space_attr_name=space_attr_name,
            figure_type="network",
        )