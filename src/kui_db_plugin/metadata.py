import json

from kdb.manager import DatabaseManager
from kui.core.metadata import WidgetMetadata, RefreshEventMetadata
from kui.core.provider import MetadataProvider


class DatabaseTableMetadataProvider(MetadataProvider):

    def __init__(self, db_manager: DatabaseManager):
        self.__manager = db_manager

    def provide(self, section_id: str) -> list[WidgetMetadata]:

        metadata = []
        widgets = self.__manager.table("ui_widgets") \
            .where("section_id = ?", section_id) \
            .retrieve()

        for widget_row in widgets:

            widget_id = widget_row.get("widget_id")
            section_id = widget_row.get("section_id")
            stylesheet = widget_row.get("stylesheet")
            refresh_events_meta = {}
            refresh_events = []

            events = self.__manager.table("ui_widget_events") \
                .where("section_id = ? AND widget_id = ?", section_id, widget_id) \
                .retrieve()

            for event in events:
                refresh_event = event.get("refresh_event_id")
                refresh_children = event.get("refresh_children") == 1

                refresh_events.append(refresh_event)
                refresh_events_meta[refresh_event] = RefreshEventMetadata(refresh_children)

            widget_meta = WidgetMetadata(
                widget_id=widget_id,
                section_id=section_id,
                parent_widget_id=widget_row.get("parent_widget_id"),
                controller=widget_row.get("controller"),
                order_id=widget_row.get("order_id"),
                widget_type=widget_row.get("widget_type_id"),
                layout_type=widget_row.get("layout_type_id"),
                grid_columns=widget_row.get("grid_columns"),
                spacing=widget_row.get("spacing"),
                width=widget_row.get("width"),
                height=widget_row.get("height"),
                margin_left=widget_row.get("margin_left"),
                margin_top=widget_row.get("margin_top"),
                margin_right=widget_row.get("margin_right"),
                margin_bottom=widget_row.get("margin_bottom"),
                style_object_name=widget_row.get("style_object_name"),
                content=widget_row.get("content"),
                tooltip=widget_row.get("tooltip"),
                alignment_string=widget_row.get("alignment"),
                stylesheet=self.__parse_stylesheet(stylesheet),
                refresh_events=refresh_events,
                refresh_events_meta=refresh_events_meta
            )

            metadata.append(widget_meta)

        return metadata

    @staticmethod
    def __parse_stylesheet(stylesheet: str):
        """
        Converts a dictionary of CSS properties into a standard QSS string.
        """

        stylesheet_string = ""
        stylesheet_map = {}

        if stylesheet is not None:
            stylesheet_map = json.loads(stylesheet)

        for key, value in stylesheet_map.items():
            stylesheet_string += f"{key}: {value};\n"

        return stylesheet_string
