from pytest_mock import MockerFixture


class TestTextResourceExtractor:

    def test_extractor_calls_transformer(self, mocker: MockerFixture, module_patch):

        from kui_db_plugin.extractor.text_resource_extractor import TextResourceExtractor

        transformer_mock = module_patch("JSONTextResourceDataTransformer")
        transformer_mock.return_value.nest.side_effect = lambda data: data

        extractor = TextResourceExtractor()
        expected_data = [
            {
                "key": "title",
                "locale": "en_US",
                "value": "Title"
            },
            {
                "key": "title",
                "locale": "uk_UA",
                "value": "TitleUA"
            }
        ]

        formatted_data = extractor._post_extract(expected_data, mocker.MagicMock())

        transformer_mock.assert_called_once()
        transformer_mock().nest.assert_called_once_with(expected_data)
        assert formatted_data == expected_data
