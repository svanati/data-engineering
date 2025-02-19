import argparse
import json

import jsonschema


class JSDValidator:
    """
    A class to validate JSON Schema Definition (JSD) files.
    """

    def __init__(self, schema_path):
        """
        Initialize the JSDValidator with the path to the schema src.

        Parameters:
        ----------
        schema_path : str
            The path to the JSON schema src.
        """
        self.schema_path = schema_path
        self.validator_class = jsonschema.Draft7Validator
        self.schema = None

    def load_jsd(self):
        """
        Load the JSD src.

        Raises:
        ------
        FileNotFoundError
            If the src at schema_path does not exist.
        ValueError
            If there is an error decoding the JSON src.
        """
        try:
            with open(self.schema_path, "r") as file:
                self.schema = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.schema_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in {self.schema_path}: {e}")

    def validate_jsd(self):
        """
        Validate the JSD src against the provided JSON schema validator.

        Returns:
        -------
        tuple
            A tuple containing a boolean indicating if the schema is valid and a message.

        Raises:
        ------
        jsonschema.exceptions.SchemaError
            If there is a schema error in the JSON src.
        """
        try:
            self.validator_class.check_schema(self.schema)
            return True, f"{self.schema_path} is a valid JSON schema."
        except jsonschema.exceptions.SchemaError as e:
            return False, f"Schema error in {self.schema_path}: {e.message}"

    def output_result(self, valid, message):
        """
        Output the validation result.

        Parameters:
        ----------
        valid : bool
            Indicates if the schema is valid.
        message : str
            The validation message.
        """
        if valid:
            print(f"Validation successful: {message}")
        else:
            print(f"Validation failed: {message}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a JSD schema src.")
    parser.add_argument("schema_path", help="Path to the JSD schema src.")
    args = parser.parse_args()

    validator = JSDValidator(args.schema_path)
    try:
        validator.load_jsd()
        valid, message = validator.validate_jsd()
        validator.output_result(valid, message)
    except Exception as e:
        print(f"An error occurred: {e}")
