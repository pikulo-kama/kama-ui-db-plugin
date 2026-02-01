from kamadbm.command import CommandContext
from kamadbm.extractor import RegularExtractor
from kui.transformer.tr import JSONTextResourceDataTransformer


class TextResourceExtractor(RegularExtractor):
    """
    Extractor for text_resources table.
    """

    def _post_extract(self, data: list[dict[str, str]], context: CommandContext):
        transformer = JSONTextResourceDataTransformer()
        return transformer.nest(data)
