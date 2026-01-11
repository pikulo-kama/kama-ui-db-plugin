from kamadbm.command import CommandContext
from kamadbm.importer import RegularImporter
from kui.transformer.widget import JSONWidgetDataTransformer


class WidgetsImporter(RegularImporter):
    """
    Importer for ui_widgets table.
    """

    def _format_data(self, data: list[dict], metadata: dict, context: CommandContext):
        transformer = JSONWidgetDataTransformer()
        transformed_data = transformer.flatten(data)

        return self.__process_events(transformed_data, context)

    @staticmethod
    def __process_events(data: list[dict], context: CommandContext):

        for widget in data:
            section_id = widget.get("section_id")
            widget_id = widget.get("widget_id")
            refresh_events = widget.get("refresh_events", [])
            recursive_refresh_events = widget.get("recursive_refresh_events", [])

            if "refresh_events" in widget:
                del widget["refresh_events"]

            if "recursive_refresh_events" in widget:
                del widget["recursive_refresh_events"]

            events_table = context.database.table("ui_widget_events") \
                .where(f"section_id == '{section_id}'") \
                .retrieve()

            events_table.remove_all() \
                .save()

            for event in refresh_events:
                events_table.add(
                    section_id=section_id,
                    widget_id=widget_id,
                    refresh_event_id=event,
                    refresh_children=0
                )

            for event in recursive_refresh_events:
                events_table.add(
                    section_id=section_id,
                    widget_id=widget_id,
                    refresh_event_id=event,
                    refresh_children=1
                )

            events_table.save()

        return data
