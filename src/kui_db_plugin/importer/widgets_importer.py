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
        template_sections = set([
            record.get("section_id")
            for record in transformed_data
            if "__template" in record.get("section_id")
        ])

        for section_id in template_sections:
            context.database.table(metadata.get("table_name")) \
                .where(f"section_id = ?", section_id) \
                .retrieve() \
                .remove_all() \
                .save()

        return self.__process_events(transformed_data, context)

    @staticmethod
    def __process_events(data: list[dict], context: CommandContext):

        for widget in data:
            section_id = widget.get("section_id")
            widget_id = widget.get("widget_id")
            refresh_events = widget.get("refresh_events", [])
            recursive_refresh_events = widget.get("recursive_refresh_events", [])
            all_events = refresh_events + recursive_refresh_events

            if "refresh_events" in widget:
                del widget["refresh_events"]

            if "recursive_refresh_events" in widget:
                del widget["recursive_refresh_events"]

            events_table = context.database.table("ui_widget_events") \
                .where(f"section_id = ? AND widget_id = ?", section_id, widget_id) \
                .retrieve()

            events_table.remove_all() \
                .save()

            for event in all_events:
                events_table.add(
                    section_id=section_id,
                    widget_id=widget_id,
                    refresh_event_id=event,
                    refresh_children=1 if event in recursive_refresh_events else 0
                )

            events_table.save()

        return data
