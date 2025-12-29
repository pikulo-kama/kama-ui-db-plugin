from kamadbm.command import CommandContext
from kamadbm.importer import RegularImporter


class TextResourceImporter(RegularImporter):
    """
    Importer for text_resources table.
    """

    def _format_data(self, data: dict[str, dict], metadata: dict, context: CommandContext):

        resources = []

        for resource_key, resource_data in data.items():
            for locale_id, resource_value in resource_data.items():

                resources.append({
                    "key": resource_key,
                    "locale": locale_id,
                    "text": resource_value
                })

        return resources
