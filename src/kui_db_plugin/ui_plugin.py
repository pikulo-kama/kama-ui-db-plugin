from kui.core.app import KamaApplication
from kui_db_plugin.database import db

from kui_db_plugin.provider.metadata import DatabaseTableMetadataProvider
from kui_db_plugin.provider.section import DatabaseTableSectionProvider
from kui_db_plugin.provider.style import load_colors, load_fonts, load_dynamic_resources
from kui_db_plugin.provider.tr import DatabaseTableTextResourceProvider


_application = KamaApplication()

_application.metadata_provider = DatabaseTableMetadataProvider(db)
_application.section_provider = DatabaseTableSectionProvider(db)
_application.text_resources.set_provider(DatabaseTableTextResourceProvider(db))

load_colors(_application)
load_fonts(_application)
load_dynamic_resources(_application)
