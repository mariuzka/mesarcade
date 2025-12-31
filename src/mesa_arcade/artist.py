import arcade
import matplotlib
import matplotlib.colors
import mesa

from mesa_arcade.utils import parse_color

class Artist:
    def __init__(
        self,
        color: str | tuple | list | None = "blue",
        color_attribute: str | None = None,
        color_map: str = "bwr",
        color_vmin: float | None = None,
        color_vmax=None,
        shape="rect",
        dynamic_color = True,
        dynamic_position = True,
        dynamic_agent_set = True,
        agent_selector = lambda agent: True,
        #agent_x_position = lambda agent: agent.cell.coordinate[0],
        #agent_y_position = lambda agent: agent.cell.coordinate[1],
    ):
        self.color = parse_color(color=color)
        self.color_attribute = color_attribute
        self.color_map: str | dict | None = color_map
        self.color_vmin = color_vmin
        self.color_vmax = color_vmax
        self.shape = shape
        self.dynamic_color = dynamic_color
        self.dynamic_position = dynamic_position
        self.dynamic_agent_set = dynamic_agent_set
        self.agent_selector = agent_selector
        #self.agent_x_position = agent_x_position
        #self.agent_y_position = agent_y_position

        self.agents: list[mesa.Agent] | None = None

        self.assert_correct_color_input()
        if self.color_attribute is not None:
            self.color_dict = {}
            self.fill_color_dict()
    
    def setup(self, figure, renderer):
        self.figure = figure
        self.renderer = renderer
        self.setup_sprites()
    
    def draw(self):
        self.sprite_list.draw()
    
    def fill_color_dict(self):
        if isinstance(self.color_map, str):
            norm = matplotlib.colors.Normalize(vmin=self.color_vmin, vmax=self.color_vmax)
            cmap = matplotlib.colormaps[self.color_map]
            for color_value in range(self.color_vmin-100, self.color_vmax+101):
                rgb = tuple(int(255*c) for c in cmap(norm(color_value))[0:3])
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
    
    def set_sprite_position(self, x, y, sprite):
        sprite.center_x = (
            x * self.figure.cell_agent_width 
            + self.figure.x 
            + self.figure.cell_agent_width / 2
        )
        sprite.center_y = (
            y * self.figure.cell_agent_height 
            + self.figure.y 
            + self.figure.cell_agent_height / 2
        )

    def set_sprite_color(self, agent, sprite):
        pass

    def create_sprite(self, agent):
        pass

    def add_sprite(self, agent):
        pass

    def setup_sprites(self):
        pass
       
    
class CellArtist(Artist):
    def __init__(
            self, 
            color = "blue", 
            color_attribute = None, 
            color_map = "bwr", 
            color_vmin = None, 
            color_vmax=None, 
            shape="rect", 
            dynamic_color=True, 
            dynamic_position=True, 
            dynamic_agent_set=True, 
            agent_selector=lambda agent: True,
            ):
        super().__init__(
            color, 
            color_attribute, 
            color_map, 
            color_vmin, 
            color_vmax, 
            shape, 
            dynamic_color, 
            dynamic_position, 
            dynamic_agent_set, 
            agent_selector,
            )
    
    def set_sprite_color(self, agent, sprite):
        if self.color_attribute is None:
            sprite.color = self.color
        else:
            sprite.color = self.color_dict[int(getattr(agent, self.color_attribute))]
            
    def add_sprite(self, agent):
        sprite = self.create_sprite(agent=agent)
        self.sprite_list.append(sprite)
        self.sprite_dict[agent] = sprite

    def setup_sprites(self):
        self.agents = self.select_agents()
        self.sprite_list = arcade.SpriteList(use_spatial_hash=False)
        self.sprite_dict = {}
        for agent in self.agents:
            self.add_sprite(agent=agent)
    
    def create_sprite(self, agent):
        if self.shape == "rect":
            sprite = arcade.SpriteSolidColor(
                width=max(1, self.figure.cell_agent_width),
                height=max(1, self.figure.cell_agent_height),
            )
        elif self.shape == "circle":
            sprite = arcade.SpriteCircle(
                radius=max(1, min(self.figure.cell_agent_width, self.figure.cell_agent_height) / 2), 
                color=arcade.color.BABY_BLUE, # platzhalter
            )
        else:
            raise ValueError("`shape` must be on of: 'rect', 'circle'.")
        
        self.set_sprite_position(x=agent.cell.coordinate[0], y=agent.cell.coordinate[1], sprite=sprite)
        self.set_sprite_color(agent=agent, sprite=sprite)
        return sprite

    def select_agents(self) -> list[mesa.Agent]:
        return [agent for agent in self.renderer.model.agents if self.agent_selector(agent)]
    
    def update(self):
        # TODO: use dirty_color and dirty_position to update only specific agent sprites
        
        # if the set of agents is not fixed during the simulation
        if self.dynamic_agent_set:
            # get all relevant agents
            self.agents = self.select_agents()
            updated_agents = set(self.agents)

            # get all agents that were added previously
            agents_with_sprite = set(self.sprite_dict)
            
            # get all agents which need a sprite
            add_list = updated_agents - agents_with_sprite

            # add sprites for those agents
            for agent in add_list:
                self.add_sprite(agent=agent)

            # get all agents whose sprites can be removed
            remove_list = agents_with_sprite - updated_agents

            # remove the sprites of those agents
            for agent in remove_list:
                sprite = self.sprite_dict.pop(agent)
                self.sprite_list.remove(sprite)
        
        # if both colors and positions change during the simulation
        if self.dynamic_color and self.dynamic_position:
            for agent, sprite in self.sprite_dict.items():
                self.set_sprite_color(agent=agent, sprite=sprite)
                self.set_sprite_position(x=agent.cell.coordinate[0], y=agent.cell.coordinate[1], sprite=sprite)
        
        # if only the colors can change
        elif self.dynamic_color:
            for agent, sprite in self.sprite_dict.items():
                self.set_sprite_color(agent=agent, sprite=sprite)

        # if only the positions can change
        elif self.dynamic_position:
            for agent, sprite in self.sprite_dict.items():
                self.set_sprite_position(x=agent.cell.coordinate[0], y=agent.cell.coordinate[1], sprite=sprite)




class PropertyLayerArtist(Artist):
    def __init__(
            self,
            layer_name,
            color_map="bwr",
            color_vmin=None,
            color_vmax=None,
            shape="rect",
            dynamic_color=True,
            ):
        
        super().__init__(
            color_map=color_map,
            color_vmin=color_vmin,
            color_vmax=color_vmax,
            shape=shape,
            dynamic_color=dynamic_color,
            dynamic_position=False,
            dynamic_agent_set=False,
            )