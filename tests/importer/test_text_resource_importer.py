from pytest_mock import MockerFixture


class TestTextResourceImporter:

    def test_importer_calls_transformer(self, mocker: MockerFixture, module_patch):

        from kui_db_plugin.importer.text_resource_importer import TextResourceImporter

        transformer_mock = module_patch("JSONTextResourceDataTransformer")
        transformer_mock.return_value.flatten.side_effect = lambda data: data

        importer = TextResourceImporter()
        expected_data = {
            "title": {
                "en_US": "Title",
                "uk_UA": "TitleUA",
            }
        }

        formatted_data = importer._format_data(expected_data, mocker.MagicMock(), mocker.MagicMock())

        transformer_mock.assert_called_once()
        transformer_mock().flatten.assert_called_once_with(expected_data)
        assert formatted_data == expected_data
