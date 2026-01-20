import arcade

class Section:
    def __init__(self, renderer, components, xy_position=None, anchor=None):
        self.renderer = renderer
        self.components = components
        self.xy_position = xy_position
        self.anchor=None
    
    def setup(self):
        pass