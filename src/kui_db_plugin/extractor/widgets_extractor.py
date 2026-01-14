from kamadbm.command import CommandContext
from kamadbm.extractor import RegularExtractor
from kui.transformer.widget import JSONWidgetDataTransformer


class WidgetsExtractor(RegularExtractor):
    """
    Extractor for ui_widgets table.
    """

    def _post_extract(self, data: list[dict], context: CommandContext):
        transformer = JSONWidgetDataTransformer()
        data = self.__process_data(data, context)

        return transformer.nest(data)

    @classmethod
    def __process_data(cls, data: list[dict], context: CommandContext):

        processed_template_widgets = []

        for widget in data:
            widget_id = widget.get("id")

            template_header_section = f"{widget_id}__template_header"
            template_body_section = f"{widget_id}__template_body"
            template_footer_section = f"{widget_id}__template_footer"

            template_widgets = context.database.table(context.args.table_name) \
                .where(
                "section = ? OR section = ? OR section = ?",
                template_header_section,
                template_body_section,
                template_footer_section
            ).retrieve()

            cls.__populate_events(widget, context)

            for template_widget in template_widgets:
                template_widget = cls.__populate_events(template_widget.to_json(include_nulls=False), context)
                processed_template_widgets.append(template_widget)

        return data + processed_template_widgets

    @staticmethod
    def __populate_events(widget: dict, context: CommandContext):
        section_id = widget.get("section")
        widget_id = widget.get("id")

        events = context.database.table("ui_widget_events") \
            .where("section_id = ? AND widget_id = ?", section_id, widget_id) \
            .retrieve()

        if not events.is_empty:
            widget["events"] = [event.to_json() for event in events]

        return widget
