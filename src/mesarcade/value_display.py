from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

import arcade
from pyglet.graphics import Batch

if TYPE_CHECKING:
    import mesa


class ValueDisplay:
    """Displays the current value of a model attribute in the GUI.

    Shows a labeled value that updates during the simulation. Useful for
    displaying key metrics like population counts, resource levels, or
    any other scalar value derived from the model.

    Args:
        model_attribute: The attribute to display. Can be a string (attribute
            name) or a callable that takes a mesa.Model and returns a value.
        label: Optional label text. If None, the attribute name is used for
            string attributes, or "no label" for callables.
        update_step: Simulation steps between value updates. Defaults to 10.
        from_datacollector: If True, reads values from the model's datacollector
            instead of directly from the model. Only works with string
            attributes. Defaults to False.
    """

    def __init__(
        self,
        model_attribute: str | Callable[[mesa.Model], Any] | None,
        label: str | None = None,
        update_step: int = 10,
        from_datacollector: bool = False,
    ) -> None:
        self.model_attribute = model_attribute
        self.label = label
        self.update_step = update_step
        self.from_datacollector = from_datacollector

    def setup(self, i, renderer, initial_value=None):
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

        # get the label text
        if self.label is not None:
            label_text = self.label
        elif self.label is None and isinstance(self.model_attribute, str):
            label_text = self.model_attribute
        else:
            label_text = "no label"

        # create the label element
        self.label_element = arcade.Text(
            text=label_text,
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
        if isinstance(self.model_attribute, str):
            if not self.from_datacollector:
                return str(getattr(self.model, self.model_attribute))

            # get the value from the datacollector
            else:
                return str(self.model.datacollector.model_vars[self.model_attribute][-1])

        # get the value using a lambda function
        else:
            return str(self.model_attribute(self.model))

    def update(self, new_value=None, force_update=False):
        if self.renderer.tick % self.update_step == 0 or force_update:
            new_value = self.get_value_from_model() if new_value is None else new_value
            if new_value != self.current_value:
                self.current_value = new_value
                self.value_element.text = new_value

    def draw(self):
        self.text_batch.draw()
