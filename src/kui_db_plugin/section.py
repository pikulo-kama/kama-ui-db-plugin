from kdb.manager import DatabaseManager
from kui.core.controller import WidgetController
from kui.core.provider import ControllerSectionProvider, Section


class DatabaseTableSectionProvider(ControllerSectionProvider):

    def __init__(self, manager: DatabaseManager):
        self.__manager = manager

    def provide(self, controller: WidgetController) -> list[Section]:

        sections = []
        section_table = self.__manager.table("ui_sections") \
            .where("controller = ?", controller.__class__.__name__) \
            .order_by("order_id") \
            .retrieve()

        for section_row in section_table:
            section = Section(
                section_id=section_row.get("section_id"),
                section_label=section_row.get("section_label"),
                section_icon=section_row.get("section_icon"),
            )
            sections.append(section)

        return sections
