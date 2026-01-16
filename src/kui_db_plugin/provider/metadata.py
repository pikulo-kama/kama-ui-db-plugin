from kdb.manager import DatabaseManager
from kui.core.filter import KamaFilter
from kui.core.metadata import WidgetMetadata, RefreshEventMetadata
from kui.core.provider import MetadataProvider


_rename_keys = {
    "id": "widget_id",
    "type": "widget_type",
    "layout": "layout_type",
    "section": "section_id",
    "parent": "parent_widget_id",
    "style_id": "style_object_name",
    "alignment": "alignment_string",
    "args": "controller_args"
}


class DatabaseTableMetadataProvider(MetadataProvider):

    def __init__(self, db_manager: DatabaseManager):
        self.__manager = db_manager

    def provide(self, query: KamaFilter) -> list[WidgetMetadata]:

        metadata = []
        widgets = self.__manager.table("ui_widgets") \
            .where(query.to_sql()) \
            .retrieve()

        for widget_row in widgets:

            widget_id = widget_row.get("id")
            section_id = widget_row.get("section")
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

            widget_json = widget_row.to_json()

            stylesheet = widget_json.get("stylesheet") or "{}"
            stylesheet = self._parse_stylesheet(stylesheet)

            widget_json["refresh_events"] = refresh_events
            widget_json["refresh_events_meta"] = refresh_events_meta
            widget_json["stylesheet"] = stylesheet

            for key, target_key in _rename_keys.items():
                if key in widget_json:
                    widget_json[target_key] = widget_json.pop(key)

            metadata.append(WidgetMetadata(**widget_json))

        return metadata
