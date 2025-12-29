from typing import Any

from kamadbm.command import CommandContext
from kamadbm.extractor import RegularExtractor


class TextResourceExtractor(RegularExtractor):
    """
    Extractor for text_resources table.
    """

    def _post_extract(self, data: Any, context: CommandContext):
        formatted_data = {}

        for record in sorted(data, key=lambda r: r.get("key")):
            key = record.get("key")
            locale = record.get("locale")
            value = record.get("text")

            translations = formatted_data.get(key, {})
            translations[locale] = value

            formatted_data[key] = translations

        return formatted_data
