from kui.core.app import KamaApplication
from kui_db_plugin.database import db

from kui_db_plugin.metadata import DatabaseTableMetadataProvider
from kui_db_plugin.section import DatabaseTableSectionProvider


application = KamaApplication()

application.metadata_provider = DatabaseTableMetadataProvider(db)
application.section_provider = DatabaseTableSectionProvider(db)
