from kdb.manager import DatabaseManager
from kui.core.app import KamaApplication

from kui_db_plugin.metadata import DatabaseTableMetadataProvider
from kui_db_plugin.section import DatabaseTableSectionProvider


application = KamaApplication()
db_manager = DatabaseManager(application.config.get("datasource.db-path"))

application.metadata_provider = DatabaseTableMetadataProvider(db_manager)
application.section_provider = DatabaseTableSectionProvider(db_manager)
