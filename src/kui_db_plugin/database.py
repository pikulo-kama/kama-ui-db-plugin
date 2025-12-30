from kdb.manager import DatabaseManager
from kui.core.app import prop


db = DatabaseManager(prop("datasource.db-path"))
