import argparse
import difflib
import json


class JSDDiff:
    """
    A class to perform a diff between two JSON Schema Definition (JSD) files.
    """

    def __init__(self, source_path, destination_path):
        """
        Initialize the JSDDiff with paths to the source and destination schema files.

        Parameters:
        ----------
        source_path : str
            The path to the source JSON schema src.
        destination_path : str
            The path to the destination JSON schema src.
        """
        self.source_path = source_path
        self.destination_path = destination_path
        self.source_schema = None
        self.destination_schema = None

    def load_jsd(self, path):
        """
        Load the JSD src.

        Parameters:
        ----------
        path : str
            The path to the JSON schema src.

        Returns:
        -------
        dict
            The loaded JSON schema.

        Raises:
        ------
        FileNotFoundError
            If the src at the given path does not exist.
        ValueError
            If there is an error decoding the JSON src.
        """
        try:
            with open(path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON in {path}: {e}")

    def load_schemas(self):
        """
        Load both source and destination JSD files.
        """
        self.source_schema = self.load_jsd(self.source_path)
        self.destination_schema = self.load_jsd(self.destination_path)

    def perform_diff(self):
        source_json = json.dumps(self.source_schema, indent=4) + "\n"
        dest_json = json.dumps(self.destination_schema, indent=4) + "\n"

        source_lines = source_json.splitlines(True)
        dest_lines = dest_json.splitlines(True)

        diff = difflib.unified_diff(
            source_lines,
            dest_lines,
            fromfile=self.source_path,
            tofile=self.destination_path,
        )

        return list(diff)

    def output_diff(self, differences, output_format="text"):
        """
        Output the differences in the destination schema.

        Parameters:
        ----------
        differences : list
            The list of differences.
        output_format : str, optional
            The format to output the differences (default is "text").
        """
        if output_format == "html":
            self.output_diff_html(differences)
        else:
            self.output_diff_text(differences)

    def output_diff_text(self, differences):
        """
        Output the differences as text.

        Parameters:
        ----------
        differences : list
            The list of differences.
        """
        file_path = "diff.txt"
        with open(file_path, "w") as file:
            file.write(
                f"Differences between {self.source_path} and {self.destination_path}:\n\n"
            )
            for line in differences:
                file.write(f"{line}\n")
        print(f"Diff src written to: {file_path}")

    def output_diff_html(self, differences):
        """
        Output the differences as HTML.

        Parameters:
        ----------
        differences : list
            The list of differences.
        """
        file_path = "diff.html"
        html_output = f"<html><body><h1>Differences between {self.source_path} and {self.destination_path}:</h1><pre>"
        for line in differences:
            html_output += f"{line}<br>"
        html_output += "</pre></body></html>"

        with open(file_path, "w") as file:
            file.write(html_output)
        print(f"Diff src written to: {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Perform a diff between two JSD schema files and output the differences in the destination src."
    )
    parser.add_argument("source_path", help="Path to the source JSD schema src.")
    parser.add_argument(
        "destination_path", help="Path to the destination JSD schema src."
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "html"],
        default="text",
        help="Output format for the differences (default: text).",
    )
    args = parser.parse_args()

    jsd_diff = JSDDiff(args.source_path, args.destination_path)
    try:
        jsd_diff.load_schemas()
        differences = jsd_diff.perform_diff()
        jsd_diff.output_diff(differences, args.output_format)
    except Exception as e:
        print(f"An error occurred: {e}")
