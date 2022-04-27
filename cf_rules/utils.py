import os

class Utils:
    def __init__(self, directory: str = None) -> None:
        """Utils class to manage Cloudflare data

        >>> utils = Utils("my_expressions")
        """

        self.directory = directory if directory else "expressions"

        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

    def change_directory(self, directory: str) -> None:
        """Change the directory where the expressions are stored

        >>> utils.change_directory("my_expressions2")
        """

        self.directory = directory

        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

    def escape(self, string) -> str:
        """Escape a string

        Simply replace slashes with underscores for the file name

        >>> utils.escape("Test/1")
        >>> "Test_1"
        """

        # return "".join(c if c.isalnum() else "_" for c in string)
        return string.replace("/", "_")

    def unescape(self, string: str) -> str:
        """Unescape a string

        Simply replace underscores with slashes for the rule name

        >>> utils.unescape("Test_1")
        >>> "Test/1"
        """

        # return string.replace("___", " - ").replace("_", " ")
        return string.replace("_", "/")

    def write_expression(self, rule_name: str, rule_expression: str, header: dict | None = None) -> None:
        """Write an expression to a readable text file

        >>> utils.write_expression("IsBot", "(cf.client.bot)")
        >>> utils.write_expression("IsBot", "(cf.client.bot)", header={"action": "allow"})
        """

        with open(f"{self.directory}/{self.escape(rule_name)}.txt", "w") as file:
            if header:
                data = " ".join(f"{x}:{y}" for x, y in header.items())
                file.write(f"#! {data} !#\n")
            file.write(rule_expression)

    def read_expression(self, rule_file: str) -> tuple[str | None, str]:
        """Read an expression from a file

        >>> utils.read_expression("IsBot")
        >>> "(cf.client.bot)"
        """

        filename = f"{self.directory}/{self.escape(rule_file)}.txt"

        if os.path.isfile(filename):
            with open(filename, "r") as file:
                header = self.process_header(file.readline().strip())

                expression = [x.strip() for x in file.readlines()
                              if not x.strip().startswith("#")]
        else:
            print(f"No such file in folder '{self.directory}'")
            return

        return header, " ".join(expression)

    def process_header(self, header_line: str) -> dict | None:
        """Process the header of an expression file if it exists
        It retrieves all header data and returns a dictionary

        >>> utils.process_header("#! action:block paused:False priority:42 !#")
        >>> {"action": "block", "paused": "False", "priority": "42"}
        """

        if header_line.startswith("#!") and header_line.endswith("!#"):
            header_data = header_line[2:-2].strip()
            header = {x: y for x, y in [x.split(":") for x in header_data.split(" ")]}

            if "action" in header:
                # List of all available actions for Cloudflare
                available_actions = ["block", "challenge", "js_challenge", "managed_challenge", "allow", "log", "bypass"]

                if header["action"] not in available_actions:
                    del header["action"]
                    print("The action in the header is not valid, ignoring it...")
                    print("List of available actions: " + ", ".join(available_actions))
            if "paused" in header:
                header["paused"] = False if header["paused"].lower() == "false" else True
            if "priority" in header:
                if header["priority"].isdigit():
                    header["priority"] = int(header["priority"])
                else:
                    del header["priority"]
        else:
            header = None

        return header

    def get_json_key(self, json: dict, keys: list[str | int]) -> dict | bool:
        """Get an element from a json using a list of keys

        >>> utils.get_json_key({"a": {"b": {"c": "d"}}}, ["a", "b", "c"])
        >>> "d"
        >>> utils.get_json_key({"a": ["b", "c"]}, ["a", 1])
        >>> "c"
        """

        for key in keys:
            if isinstance(key, str):
                if key in json:
                    json = json[key]
                else:
                    return False
            elif isinstance(key, int):
                if len(json) > key:
                    json = json[key]
                else:
                    return False

        return json



class Error:
    def __init__(self):
        """Error class to handle Cloudflare errors

        >>> error = Error()
        """

        self.utils = Utils()

    def handle(self, request_json: dict, keys: list[str | int]) -> any:
        """Handle errors from a request response

        :exception SystemExit: If auth error

        >>> error.handle({"success": True, "result": {"a": "b"}}, ["success"])
        >>> True

        >>> error.handle({"success": False, "errors": [{"code": "invalid_parameter", "message": "Invalid parameter"}]}, ["success"])
        >>> False

        >>> error.handle({"success": False, "errors": [{"code": 9109, "message": "Invalid access token"}], "messages": [], "result": None})
        >>> "Invalid access token"
        """

        if request_json["errors"]:
            # Authentication error, Invalid access token
            if any(x == request_json["errors"][0]["code"] for x in [10000, 9109]):
                raise SystemExit(request_json["errors"][0]["message"])

        if request_json["success"]:
            return self.utils.get_json_key(request_json, keys)
        else:
            return {"error": self.utils.get_json_key(request_json, ["errors", 0, "message"])}
