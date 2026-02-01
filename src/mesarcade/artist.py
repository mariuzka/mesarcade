import arcade
import matplotlib
import matplotlib.colors
import networkx as nx
import random

from mesarcade.utils import parse_color

class Artist:
    def __init__(
        self,
        color: str | tuple | list | None = "black",
        color_attribute: str | None = None,
        color_map: str | None = "bwr",
        color_vmin: float | None = None,
        color_vmax: float | None = None,
        shape: str = "rect",
        size: float = 1,
        entity_selector=lambda entity: True,
        jitter: bool = False,
        dynamic_color: bool = True,
        dynamic_position: bool = True,
        dynamic_population: bool = True,
    ):
        self.color = parse_color(color=color)
        self.color_attribute = color_attribute
        self.color_map: str | dict | None = color_map
        self.color_vmin = color_vmin
        self.color_vmax = color_vmax
        self.shape = shape
        self.dynamic_color = dynamic_color
        self.dynamic_position = dynamic_position
        self.dynamic_population = dynamic_population
        self.entity_selector = entity_selector
        self.jitter = jitter
        self.size = size

        self.assert_correct_color_input()
        if self.color_attribute is not None:
            self.color_dict = {}
            self.fill_color_dict()

    def set_size(self):
        self.width = self.figure.cell_width * self.size
        self.height = self.figure.cell_height * self.size

    def setup(self, figure, renderer):
        self.figure = figure
        self.renderer = renderer
        self.model = self.renderer.model
        self.population = self.get_population()

        self.set_size()
        self.setup_sprites()

    def get_population(self):
        pass

    def get_xy_position(self, entity):
        pass

    def scale_x(self, x):
        pass

    def scale_y(self, y):
        pass

    def draw(self):
        self.sprite_list.draw()

    def fill_color_dict(self):
        if isinstance(self.color_map, str):
            norm = matplotlib.colors.Normalize(vmin=self.color_vmin, vmax=self.color_vmax)
            cmap = matplotlib.colormaps[self.color_map]
            for color_value in range(self.color_vmin - 100, self.color_vmax + 101):
                rgb = tuple(int(255 * c) for c in cmap(norm(color_value))[0:3])
                self.color_dict[color_value] = rgb

        elif isinstance(self.color_map, dict):
            self.color_dict = {
                key: parse_color(color=color) for key, color in self.color_map.items()
            }
        else:
            raise ValueError("`color_map` must be a str or a dict.")

    def assert_correct_color_input(self):
        if self.color_attribute is None:
            assert self.color is not None

        elif self.color_attribute is not None:
            assert self.color_map is not None
            if isinstance(self.color_map, str):
                assert self.color_vmin is not None and self.color_vmax is not None

    def set_sprite_position(self, xy_position, sprite):
        x = self.scale_x(xy_position[0])
        y = self.scale_y(xy_position[1])

        if self.jitter:
            x += sprite.mesar_x_jitter
            y += sprite.mesar_y_jitter

        sprite.center_x = x
        sprite.center_y = y

    def set_sprite_color(self, entity, sprite):
        if self.color_attribute is None:
            sprite.color = self.color
        else:
            sprite.color = self.color_dict[int(getattr(entity, self.color_attribute))]

    def add_sprite(self, entity):
        sprite = self.create_sprite(entity=entity)
        self.sprite_list.append(sprite)
        self.sprite_dict[entity] = sprite

    def setup_sprites(self):
        self.selected_entities = self.select_entities()
        self.sprite_list = arcade.SpriteList(use_spatial_hash=False)
        self.sprite_dict = {}
        for entity in self.selected_entities:
            self.add_sprite(entity=entity)

    def create_sprite(self, entity):
        if self.shape == "rect":
            sprite = arcade.SpriteSolidColor(
                width=max(1, self.width),
                height=max(1, self.height),
            )
        elif self.shape == "circle":
            sprite = arcade.SpriteCircle(
                radius=max(1, min(self.width, self.height) / 2),
                color=arcade.color.BABY_BLUE,  # platzhalter
            )
        elif self.shape == "line":
            sprite = arcade.SpriteSequence()
            
            draw_line_strip(
                self.scaled_data_dict[model_attr],
                color=self.color_list[i],
                line_width=2,
            )
       

        if self.jitter:
            sprite.mesar_x_jitter = (self.model.random.random() - 0.5) * self.figure.cell_width
            sprite.mesar_y_jitter = (self.model.random.random() - 0.5) * self.figure.cell_height

        self.set_sprite_position(
            xy_position=self.get_xy_position(entity=entity),
            sprite=sprite,
        )
        self.set_sprite_color(entity=entity, sprite=sprite)
        return sprite

    def select_entities(self) -> list:
        return [entity for entity in self.population if self.entity_selector(entity)]

    def update(self):
        # TODO: use dirty_color and dirty_position to update only specific entity sprites

        # if the set of entities is not fixed during the simulation
        if self.dynamic_population:
            # get all relevant entities
            self.selected_entities = self.select_entities()
            updated_entities = set(self.selected_entities)

            # get all entities that were added previously
            entities_with_sprite = set(self.sprite_dict)

            # get all entities which need a sprite
            add_list = updated_entities - entities_with_sprite

            # add sprites for those entities
            for entity in add_list:
                self.add_sprite(entity=entity)

            # get all entities whose sprites can be removed
            remove_list = entities_with_sprite - updated_entities

            # remove the sprites of those entities
            for entity in remove_list:
                sprite = self.sprite_dict.pop(entity)
                self.sprite_list.remove(sprite)

        # if both colors and positions change during the simulation
        if self.dynamic_color and self.dynamic_position:
            for entity, sprite in self.sprite_dict.items():
                self.set_sprite_color(entity=entity, sprite=sprite)
                self.set_sprite_position(
                    xy_position=self.get_xy_position(entity),
                    sprite=sprite,
                )

        # if only the colors can change
        elif self.dynamic_color:
            for entity, sprite in self.sprite_dict.items():
                self.set_sprite_color(entity=entity, sprite=sprite)

        # if only the positions can change
        elif self.dynamic_position:
            for entity, sprite in self.sprite_dict.items():
                self.set_sprite_position(
                    xy_position=self.get_xy_position(entity),
                    sprite=sprite,
                )


class CellAgentArtists(Artist):
    """
    A visual representation of CellAgents.
    """

    def __init__(
        self,
        color: str | tuple | list | None = "black",
        color_attribute: str | None = None,
        color_map: str | None = "bwr",
        color_vmin: float | None = None,
        color_vmax: float | None = None,
        shape: str = "circle",
        size: float = 1,
        entity_selector=lambda entity: True,
        jitter: bool = False,
        dynamic_color: bool = True,
        dynamic_position: bool = True,
        dynamic_population: bool = True,
    ):
        super().__init__(
            color=color,
            color_attribute=color_attribute,
            color_map=color_map,
            color_vmin=color_vmin,
            color_vmax=color_vmax,
            shape=shape,
            size=size,
            entity_selector=entity_selector,
            jitter=jitter,
            dynamic_color=dynamic_color,
            dynamic_position=dynamic_position,
            dynamic_population=dynamic_population,
        )

    def get_population(self):
        return self.model.agents

    def get_xy_position(self, entity):
        return entity.cell.coordinate

    def scale_x(self, x):
        return x * self.figure.cell_width + self.figure.x + self.figure.cell_width / 2

    def scale_y(self, y):
        return y * self.figure.cell_height + self.figure.y + self.figure.cell_height / 2


class CellArtists(Artist):
    """
    A visual representation of Cells.
    """

    def __init__(
        self,
        color: str | tuple | list | None = "grey",
        color_attribute: str | None = None,
        color_map: str | None = "bwr",
        color_vmin: float | None = None,
        color_vmax: float | None = None,
        shape: str = "rect",
        size: float = 1,
        entity_selector=lambda entity: True,
        jitter: bool = False,
        dynamic_color: bool = True,
        dynamic_position: bool = False,
        dynamic_population: bool = True,
    ):
        super().__init__(
            color=color,
            color_attribute=color_attribute,
            color_map=color_map,
            color_vmin=color_vmin,
            color_vmax=color_vmax,
            shape=shape,
            size=size,
            entity_selector=entity_selector,
            jitter=jitter,
            dynamic_color=dynamic_color,
            dynamic_position=dynamic_position,
            dynamic_population=dynamic_population,
        )

    def get_population(self):
        return self.model.grid

    def get_xy_position(self, entity):
        return entity.coordinate

    def scale_x(self, x):
        return x * self.figure.cell_width + self.figure.x + self.figure.cell_width / 2

    def scale_y(self, y):
        return y * self.figure.cell_height + self.figure.y + self.figure.cell_height / 2


class ContinuousSpaceAgentArtists(Artist):
    """
    A visual representation of ContinuousSpaceAgents.
    """

    def __init__(
        self,
        color: str | tuple | list | None = "black",
        color_attribute: str | None = None,
        color_map: str | None = "bwr",
        color_vmin: float | None = None,
        color_vmax: float | None = None,
        shape: str = "circle",
        size: float = 2,
        entity_selector=lambda entity: True,
        jitter: bool = False,
        dynamic_color: bool = True,
        dynamic_position: bool = True,
        dynamic_population: bool = True,
    ):
        super().__init__(
            color=color,
            color_attribute=color_attribute,
            color_map=color_map,
            color_vmin=color_vmin,
            color_vmax=color_vmax,
            shape=shape,
            size=size,
            entity_selector=entity_selector,
            jitter=jitter,
            dynamic_color=dynamic_color,
            dynamic_position=dynamic_position,
            dynamic_population=dynamic_population,
        )

    def get_population(self):
        return self.model.agents

    def get_xy_position(self, entity):
        return entity.position

    def scale_x(self, x):
        return x * self.figure.cell_width + self.figure.x

    def scale_y(self, y):
        return y * self.figure.cell_height + self.figure.y


class NetworkCellArtists(Artist):
    def __init__(
        self,
        color: str | tuple | list | None = "black",
        color_attribute: str | None = None,
        color_map: str | None = "bwr",
        color_vmin: float | None = None,
        color_vmax: float | None = None,
        shape: str = "circle",
        size: float = 2,
        entity_selector=lambda entity: True,
        jitter: bool = False,
        dynamic_color: bool = True,
        dynamic_position: bool = True,
        dynamic_population: bool = True,
        node_size = 1,
        node_gap = 10,
        networkx_layout = nx.spring_layout
    ):
        super().__init__(
            color=color,
            color_attribute=color_attribute,
            color_map=color_map,
            color_vmin=color_vmin,
            color_vmax=color_vmax,
            shape=shape,
            size=size,
            entity_selector=entity_selector,
            jitter=jitter,
            dynamic_color=dynamic_color,
            dynamic_position=dynamic_position,
            dynamic_population=dynamic_population,
        )
        self.node_size = node_size
        self.node_gap = node_gap
        self.networkx_layout = networkx_layout

    def _get_node_positions(self):
        self.layout_positions = self.networkx_layout(self.model.grid.G)
        
        self.max_x_node_position = max([abs(self.layout_positions[i][0]) for i in self.layout_positions])
        self.max_y_node_position = max([abs(self.layout_positions[i][1]) for i in self.layout_positions])
        
        for i, cell in enumerate(self.model.grid):
            cell._MESARCADE_NETWORK_POSITION = self.layout_positions[i]
            cell._MESARCADE_NETWORK_POSITION[0] /= self.max_x_node_position
            cell._MESARCADE_NETWORK_POSITION[1] /= self.max_y_node_position

    def get_population(self):
        self._get_node_positions()
        return self.model.grid

    def get_xy_position(self, entity):
        return entity._MESARCADE_NETWORK_POSITION

    def scale_x(self, x):
        return x * self.figure.width / 2.2 + self.figure.x + self.figure.width / 2

    def scale_y(self, y):
        return y * self.figure.height / 2.2 + self.figure.y + self.figure.height / 2
    
    def draw(self):
        self.sprite_list.draw()

        edges = self.model.grid.G.edges()

        for u, v in edges:
            node_u_pos = self.layout_positions[u]
            node_v_pos = self.layout_positions[v]

            node_u_pos = [self.scale_x(node_u_pos[0]), self.scale_y(node_u_pos[1])]
            node_v_pos = [self.scale_x(node_v_pos[0]), self.scale_y(node_v_pos[1])]

            arcade.draw_line_strip(
                [node_u_pos, node_v_pos],
                color=arcade.color.BLACK,
                line_width=2,
            )
        
class NetworkCellAgentArtists(NetworkCellArtists):
    def get_xy_position(self, entity):
        return entity.cell._MESARCADE_NETWORK_POSITION
    
    def get_population(self):
        self._get_node_positions()
        return self.model.agents