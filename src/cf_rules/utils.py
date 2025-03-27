import os


class Utils:
    def __init__(self, directory: str = None) -> None:
        """Utils class to manage Cloudflare data

        >>> utils = Utils("my_expressions")
        """

        self.directory = directory or "expressions"

        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

    def change_directory(self, directory: str) -> None:
        """Change the directory where the expressions are stored

        >>> utils.change_directory("my_expressions2")
        """

        self.directory = directory

        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

    @staticmethod
    def escape(string) -> str:
        """Escape a string

        Simply replace slashes with underscores for the file name

        >>> utils.escape("Test/1")
        >>> "Test_1"
        """

        # return "".join(c if c.isalnum() else "_" for c in string)
        return string.replace("/", "_")

    @staticmethod
    def unescape(string: str) -> str:
        """Unescape a string

        Simply replace underscores with slashes for the rule name

        >>> utils.unescape("Test_1")
        >>> "Test/1"
        """

        # return string.replace("___", " - ").replace("_", " ")
        return string.replace("_", "/")

    @staticmethod
    def beautify(expression: str) -> str:
        """Beautify a Cloudflare expression

        >>> utils.beautify("(cf.client.bot) or (cf.threat_score ge 1)")
        # (cf.client.bot) or
        # (cf.threat_score ge 1)
        """

        return expression.replace(" or ", " or\n").replace(" and ", " and\n")

    def write_expression(self, rule_file: str, rule_expression: str, header: dict | None = None) -> None:
        """Write an expression to a readable text file

        >>> utils.write_expression("IsBot", "(cf.client.bot)")
        >>> utils.write_expression("IsBot", "(cf.client.bot)", header={"action": "managed_challenge", "enabled": "True"})
        """

        if not rule_file.endswith(".txt"):
            rule_file += ".txt"

        filename = f"{self.directory}/{self.escape(rule_file)}"

        with open(filename, "w", encoding="utf-8") as file:
            if header:
                data = " ".join(f"{x}:{y}" for x, y in header.items())
                file.write(f"#! {data} !#\n")
            file.write(rule_expression)

    def read_expression(self, rule_file: str) -> tuple[str, str]:
        """Read an expression from a file

        >>> utils.read_expression("IsBot")
        >>> "(cf.client.bot)"
        """

        if not rule_file.endswith(".txt"):
            rule_file += ".txt"

        filename = f"{self.directory}/{self.escape(rule_file)}"

        if not os.path.isfile(filename):
            # pylint: disable=import-outside-toplevel
            from .error import Error

            raise Error(f"No such file in folder '{self.directory}'")

        with open(filename, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
            header = self.process_header(first_line)

            expression = [x.strip() for x in file.readlines() if not x.strip().startswith("#")]

            # If the first line is not a header or a comment, we add it to the expression
            if not header and not first_line.startswith("#"):
                expression.insert(0, first_line)

        return header, " ".join(expression)

    def process_header(self, header_line: str) -> dict | None:
        """Process the header of an expression file if it exists
        It retrieves all header data and returns a dictionary

        >>> utils.process_header("#! action:block enabled:True !#")
        >>> {"action": "block", "enabled": "True"}
        """

        if header_line.startswith("#!") and header_line.endswith("!#"):
            header_data = header_line[2:-2].strip()
            header = dict([x.split(":") for x in header_data.split(" ")])

            if "action" in header:
                # List of all available actions for Cloudflare
                available_actions = ["managed_challenge", "js_challenge", "challenge", "block", "skip", "log"]

                if header["action"] not in available_actions:
                    del header["action"]
                    print("The action in the header is not valid, ignoring it...")
                    print("List of available actions: " + ", ".join(available_actions))
            if "enabled" in header:
                header["enabled"] = header["enabled"].lower() == "true"
        else:
            header = None

        return header

    @staticmethod
    def get_json_key(json: dict, keys: list[str | int]) -> object:
        """Get an element from a json using a list of keys

        >>> utils.get_json_key({"a": {"b": {"c": "d"}}}, ["a", "b", "c"])
        >>> "d"
        >>> utils.get_json_key({"a": ["b", "c"]}, ["a", 1])
        >>> "c"
        """

        for key in keys:
            if (
                isinstance(key, str)
                and key in json
                or not isinstance(key, str)
                and isinstance(key, int)
                and len(json) > key
            ):
                json = json[key]
        return json
