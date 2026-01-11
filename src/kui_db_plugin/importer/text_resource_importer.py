from kamadbm.command import CommandContext
from kamadbm.importer import RegularImporter
from kui.transformer.tr import JSONTextResourceDataTransformer


class TextResourceImporter(RegularImporter):
    """
    Importer for text_resources table.
    """

    def _format_data(self, data: dict[str, dict[str, str]], metadata: dict, context: CommandContext):
        transformer = JSONTextResourceDataTransformer()
        return transformer.flatten(data)
