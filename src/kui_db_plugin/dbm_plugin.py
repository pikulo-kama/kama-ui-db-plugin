from importlib import resources
from kamadbm.cli import DatabaseCLI

from kui_db_plugin.extractor.text_resource_extractor import TextResourceExtractor
from kui_db_plugin.extractor.widgets_extractor import WidgetsExtractor
from kui_db_plugin.importer.text_resource_importer import TextResourceImporter
from kui_db_plugin.importer.widgets_importer import WidgetsImporter


_cli = DatabaseCLI()

_cli.add_importer(TextResourceImporter())
_cli.add_importer(WidgetsImporter())

_cli.add_extractor(TextResourceExtractor())
_cli.add_extractor(WidgetsExtractor())

import kui_db_plugin.migration as migrations
migrations_path = resources.files(migrations)
_cli.add_migration_path(str(migrations_path))
