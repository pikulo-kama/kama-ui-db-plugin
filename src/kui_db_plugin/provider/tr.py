from kamatr.provider import TextResourceProvider
from kamatr.resource import TextResource, TextTranslation
from kdb.manager import DatabaseManager


class DatabaseTableTextResourceProvider(TextResourceProvider):

    def __init__(self, manager: DatabaseManager):
        self.__manager = manager

    def provide(self) -> list[TextResource]:

        resource_map: dict[str, TextResource] = {}
        resources_table = self.__manager.retrieve_table("text_resources")

        for resource_row in resources_table:

            key: str = resource_row.get("key")
            locale: str = resource_row.get("locale")
            text: str = resource_row.get("text")

            resource = resource_map.get(key)

            if resource is None:
                resource = TextResource(
                    resource_key=key,
                    translations=[]
                )

            translation = TextTranslation(locale, text)
            resource.translations.append(translation)

            resource_map[key] = resource

        return list(resource_map.values())
