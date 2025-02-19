import os
import sys
from unittest.mock import mock_open, patch

import pytest

# Add the src directory to the Python path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/file")),
)

from jsd_diff import JSDDiff


class TestJSDDiff:
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"key1": "value1", "key2": "value2"}',
    )
    def test_load_jsd(self, mock_file):
        jsd_diff = JSDDiff("source.jsd", "destination.jsd")
        schema = jsd_diff.load_jsd("source.jsd")
        assert schema == {"key1": "value1", "key2": "value2"}
        mock_file.assert_called_with("source.jsd", "r")

    @patch("builtins.open", new_callable=mock_open, read_data='{"key1": "value1"}')
    def test_load_schemas(self, mock_file):
        jsd_diff = JSDDiff("source.jsd", "destination.jsd")
        jsd_diff.load_schemas()
        assert jsd_diff.source_schema == {"key1": "value1"}
        assert jsd_diff.destination_schema == {"key1": "value1"}
        assert mock_file.call_count == 2

    def test_perform_diff(self):
        jsd_diff = JSDDiff("source.jsd", "destination.jsd")
        jsd_diff.source_schema = {"key1": "value1", "key2": "value2"}
        jsd_diff.destination_schema = {"key1": "value1"}
        differences = jsd_diff.perform_diff()
        expected_diff = [
            "--- source.jsd\n",
            "+++ destination.jsd\n",
            "@@ -1,4 +1,3 @@\n",
            " {\n",
            '-    "key1": "value1",\n',
            '-    "key2": "value2"\n',
            '+    "key1": "value1"\n',
            " }\n",
        ]
        assert differences == expected_diff

    @patch("builtins.open", new_callable=mock_open)
    def test_output_diff_text(self, mock_file):
        jsd_diff = JSDDiff("source.jsd", "destination.jsd")
        differences = [
            "--- source.jsd",
            "+++ destination.jsd",
            "@@ -1,4 +1,3 @@",
            " {",
            '     "key1": "value1",',
            '     "key2": "value2"',
            " }",
        ]
        jsd_diff.output_diff_text(differences)
        mock_file.assert_called_with("diff.txt", "w")
        mock_file().write.assert_any_call(
            "Differences between source.jsd and destination.jsd:\n\n"
        )
        for line in differences:
            mock_file().write.assert_any_call(f"{line}\n")

    @patch("builtins.open", new_callable=mock_open)
    def test_output_diff_html(self, mock_file):
        jsd_diff = JSDDiff("source.jsd", "destination.jsd")
        differences = [
            "--- source.jsd",
            "+++ destination.jsd",
            "@@ -1,4 +1,3 @@",
            " {",
            '     "key1": "value1",',
            '     "key2": "value2"',
            " }",
        ]
        jsd_diff.output_diff_html(differences)
        mock_file.assert_called_with("diff.html", "w")
        html_output = (
            "<html><body><h1>Differences between source.jsd and destination.jsd:</h1><pre>"
            '--- source.jsd<br>+++ destination.jsd<br>@@ -1,4 +1,3 @@<br> {<br>     "key1": "value1",<br>     "key2": "value2"<br> }<br>'
            "</pre></body></html>"
        )
        mock_file().write.assert_called_with(html_output)


if __name__ == "__main__":
    pytest.main()
