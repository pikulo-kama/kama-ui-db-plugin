import json

from kdb.manager import DatabaseManager
from kui.core.filter import KamaFilter
from kui.core.metadata import WidgetMetadata, RefreshEventMetadata
from kui.core.provider import MetadataProvider
from kui.transformer.widget import WidgetMetadataTransformer


class DatabaseTableMetadataProvider(MetadataProvider):

    def __init__(self, db_manager: DatabaseManager):
        self.__manager = db_manager

    def provide(self, query: KamaFilter) -> list[WidgetMetadata]:

        metadata = []
        metadata_transformer = WidgetMetadataTransformer()
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
            controller_args = widget_json.get("args") or "{}"

            widget_json["refresh_events"] = refresh_events
            widget_json["refresh_events_meta"] = refresh_events_meta
            widget_json["stylesheet"] = self._parse_stylesheet(stylesheet)
            widget_json["args"] = json.loads(controller_args)

            widget_json = metadata_transformer.transform_single(widget_json)
            metadata.append(WidgetMetadata(**widget_json))

        return metadata
