import arcade


def create_button_style(font_size):
    return {
        "normal": {
            "font_name": "Arial",
            "font_size": font_size,
            "font_color": arcade.color.WHITE,
            "bg": arcade.color.DARK_GRAY,
            "border_width": 1,
            "border": arcade.color.BLACK,
        },
        "hover": {
            "font_name": "Arial",
            "font_size": font_size,
            "font_color": arcade.color.WHITE,
            "bg": arcade.color.DARK_GRAY,
            "border_width": 2,
            "border": arcade.color.BLACK,
        },
        "press": {
            "font_name": "Arial",
            "font_size": font_size,
            "font_color": arcade.color.WHITE,
            "bg": arcade.color.DARK_GRAY,
            "border_width": 2,
            "border": arcade.color.WHITE,
        },
    }
