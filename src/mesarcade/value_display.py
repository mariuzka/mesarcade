import arcade
from pyglet.graphics import Batch

class ValueDisplay:
    def  __init__(
            self, 
            model_attribute: str | None = None, 
            label: str | None = None, 
            update_step: int = 10,
            from_datacollector = False,
            get_model_attribute = None,
            ):
        """Displays the value of a given model attribute.

        Args:
            model_attribute (str | None, optional): The model attribute. Defaults to None.
            label (str | None, optional): An optional label for the model attribute. Defaults to None.
            update_step (int, optional): The number of steps after which the displayed value gets updated. Defaults to 10.
        """
        self.model_attribute = model_attribute
        self.label = label
        self.update_step = update_step
        self.from_datacollector = from_datacollector
        self.get_model_attribute = get_model_attribute
        

    def setup(self, i, renderer, initial_value = None):
        self.renderer = renderer
        self.model = self.renderer.model

        self.text_batch = Batch()
        self.text_list = []

        self.x_of_origin = self.renderer.atomic_width * 33
        self.y_of_origin = self.renderer.atomic_height * 36

        self.x_of_self = self.x_of_origin
        self.y_of_self = self.y_of_origin - i * self.renderer.atomic_height * 3

        self.x_of_label = self.x_of_self
        self.y_of_label = self.y_of_self

        self.x_of_value = self.x_of_self
        self.y_of_value = self.y_of_self - self.renderer.atomic_height

        if initial_value is not None:
            self.current_value = str(initial_value)
        elif self.model_attribute is not None:
            self.current_value = self.get_value_from_model()
        else:
            initial_value = "NA"
        
        
        self.label_element = arcade.Text(
            text=self.model_attribute if self.label is None else self.label,
            x=self.x_of_label,
            y=self.y_of_label,
            batch=self.text_batch,
            color=self.renderer.font_color,
            font_size=self.renderer.font_size,
            )
        self.text_list.append(self.label_element)

        self.value_element = arcade.Text(
            text=self.current_value,
            x=self.x_of_value,
            y=self.y_of_value,
            batch=self.text_batch,
            color=self.renderer.font_color,
            font_size=self.renderer.font_size,
            )
        self.text_list.append(self.value_element)
    
    def get_value_from_model(self):
        # get the value from a model attribute
        if not self.from_datacollector and self.get_model_attribute is None:
            return str(getattr(self.model, self.model_attribute))
        
        # get the value from the datacollector
        elif self.from_datacollector:
            return str(self.model.datacollector.model_vars[self.model_attribute][-1])

        # get the value by hand using the lambda function
        else:
            return str(self.get_model_attribute(self.model))

    def update(self, new_value = None, force_update = False):
        if self.renderer.tick % self.update_step == 0 or force_update:
            new_value = self.get_value_from_model() if new_value is None else new_value
            if new_value != self.current_value:
                self.current_value = new_value
                self.value_element.text = new_value
            
    def draw(self):
        self.text_batch.draw()