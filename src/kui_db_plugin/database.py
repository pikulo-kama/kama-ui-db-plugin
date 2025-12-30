from kdb.manager import DatabaseManager
from kui.core.shortcut import prop


db = DatabaseManager(prop("datasource.db-path"))
