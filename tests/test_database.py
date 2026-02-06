
class TestDatabase:

    def test_database_loads(self, module_patch):

        prop_mock = module_patch("prop")
        manager_mock = module_patch("DatabaseManager")

        import kui_db_plugin.database as db_module

        prop_mock.assert_called_once_with("datasource.db-path")
        manager_mock.assert_called_once_with(prop_mock.return_value)
        assert db_module.db == manager_mock.return_value
