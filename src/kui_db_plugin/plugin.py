from kui.core.app import KamaApplication
from kui_db_plugin.database import db

from kui_db_plugin.metadata import DatabaseTableMetadataProvider
from kui_db_plugin.section import DatabaseTableSectionProvider


_application = KamaApplication()

_application.metadata_provider = DatabaseTableMetadataProvider(db)
_application.section_provider = DatabaseTableSectionProvider(db)
