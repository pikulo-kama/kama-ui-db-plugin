from kui.core.app import KamaApplication
from kui_db_plugin.database import db

from kui_db_plugin.provider.metadata import DatabaseTableMetadataProvider
from kui_db_plugin.provider.section import DatabaseTableSectionProvider
from kui_db_plugin.provider.style import load_colors, load_fonts, load_dynamic_images
from kui_db_plugin.provider.tr import DatabaseTableTextResourceProvider


_application = KamaApplication()

_application.provider.metadata = DatabaseTableMetadataProvider(db)
_application.provider.section = DatabaseTableSectionProvider(db)
_application.translations.set_provider(DatabaseTableTextResourceProvider(db))

load_colors(_application)
load_fonts(_application)
load_dynamic_images(_application)
