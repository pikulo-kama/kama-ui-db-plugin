from kui.core.app import KamaApplication
from kui.dto.style import KamaColor, KamaComposedColor, KamaFont

from kui_db_plugin.database import db


def load_colors(application: KamaApplication):

    for color_row in db.retrieve_table("setup_color"):
        color = KamaComposedColor(
            color_code=color_row.get("color_id"),
            light_color=KamaColor(color_row.get("light")),
            dark_color=KamaColor(color_row.get("dark"))
        )

        application.add_color(color)


def load_fonts(application: KamaApplication):

    for font_row in db.retrieve_table("setup_font"):
        color = KamaFont(
            font_code=font_row.get("font_id"),
            font_size=font_row.get("font_size"),
            font_family=font_row.get("font_family"),
            font_weight=font_row.get("font_weight")
        )

        application.add_font(color)
