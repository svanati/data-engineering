import json
import os
import sys
from unittest.mock import mock_open, patch

import pytest

# Add the src directory to the Python path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/file")),
)
from jsd_validator import JSDValidator


class TestJSDValidator:
    """
    Test suite for the JSDValidator class.
    """

    @patch("builtins.open", new_callable=mock_open, read_data='{"type": "object"}')
    def test_load_jsd_valid(self, mock_file):
        """
        Test loading a valid JSD src.

        Parameters:
        ----------
        mock_file : unittest.mock.MagicMock
            Mocked src object.
        """
        validator = JSDValidator("dummy_path.jsd")
        validator.load_jsd()
        assert validator.schema == {"type": "object"}
        mock_file.assert_called_with("dummy_path.jsd", "r")

    @patch("builtins.open", new_callable=mock_open)
    def test_load_jsd_file_not_found(self, mock_file):
        """
        Test loading a JSD src that does not exist.

        Parameters:
        ----------
        mock_file : unittest.mock.MagicMock
            Mocked src object.
        """
        mock_file.side_effect = FileNotFoundError
        validator = JSDValidator("dummy_path.jsd")
        with pytest.raises(FileNotFoundError):
            validator.load_jsd()

    @patch("builtins.open", new_callable=mock_open, read_data='{"type": "invalid"}')
    def test_load_jsd_invalid_json(self, mock_file):
        """
        Test loading a JSD src with invalid JSON content.

        Parameters:
        ----------
        mock_file : unittest.mock.MagicMock
            Mocked src object.
        """
        mock_file.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        validator = JSDValidator("dummy_path.jsd")
        with pytest.raises(ValueError):
            validator.load_jsd()

    @patch.object(JSDValidator, "load_jsd", return_value=None)
    def test_validate_jsd_valid(self, mock_load):
        """
        Test validating a valid JSD schema.

        Parameters:
        ----------
        mock_load : unittest.mock.MagicMock
            Mocked load_jsd method.
        """
        validator = JSDValidator("dummy_path.jsd")
        validator.schema = {"type": "object"}
        valid, message = validator.validate_jsd()
        assert valid
        assert "is a valid JSON schema." in message

    @patch.object(JSDValidator, "load_jsd", return_value=None)
    def test_validate_jsd_invalid(self, mock_load):
        """
        Test validating an invalid JSD schema.

        Parameters:
        ----------
        mock_load : unittest.mock.MagicMock
            Mocked load_jsd method.
        """
        validator = JSDValidator("dummy_path.jsd")
        validator.schema = {"type": "invalid"}
        valid, message = validator.validate_jsd()
        assert not valid
        assert "Schema error" in message

    @patch("builtins.print")
    def test_output_result_valid(self, mock_print):
        """
        Test outputting the result of a valid JSD validation.

        Parameters:
        ----------
        mock_print : unittest.mock.MagicMock
            Mocked print function.
        """
        validator = JSDValidator("dummy_path.jsd")
        validator.output_result(True, "Valid JSON schema.")
        mock_print.assert_called_with("Validation successful: Valid JSON schema.")

    @patch("builtins.print")
    def test_output_result_invalid(self, mock_print):
        """
        Test outputting the result of an invalid JSD validation.

        Parameters:
        ----------
        mock_print : unittest.mock.MagicMock
            Mocked print function.
        """
        validator = JSDValidator("dummy_path.jsd")
        validator.output_result(False, "Schema error.")
        mock_print.assert_called_with("Validation failed: Schema error.")


if __name__ == "__main__":
    pytest.main()
