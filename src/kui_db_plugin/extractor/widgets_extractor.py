from kamadbm.command import CommandContext
from kamadbm.extractor import RegularExtractor
from kui.transformer.widget import JSONWidgetDataTransformer


class WidgetsExtractor(RegularExtractor):
    """
    Extractor for ui_widgets table.
    """

    def _post_extract(self, data: list[dict], context: CommandContext):
        transformer = JSONWidgetDataTransformer()
        data = self.__populate_events(data, context)

        return transformer.nest(data)

    @staticmethod
    def __populate_events(data: list[dict], context: CommandContext):
        widgets = []
        db = context.database

        for widget in data:
            section_id = widget.get("section_id")
            widget_id = widget.get("widget_id")

            events = db.table("ui_widget_events") \
                .where("section_id = ? AND widget_id = ?", section_id, widget_id) \
                .retrieve()

            widget["events"] = [event.to_json() for event in events]

        return widgets
