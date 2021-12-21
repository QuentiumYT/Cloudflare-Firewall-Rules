import requests, os

class Cloudflare:
    def __init__(self, folder: str = None):
        """Initialize Cloudflare class

        Specify a folder argument where expressions will be saved

        >>> cf = Cloudflare("my_expressions")
        """

        self.utils = Utils(folder)
        self.error = Error()

        self.plan = "free"
        self.rules = 5
        self.active_rules = 0

    def auth(self, email: str, key: str) -> None:
        """Get your global API Key through cloudflare profile (API Keys section)

        .. warning::
            This will grant all domains access to this API library

        https://dash.cloudflare.com/profile/api-tokens

        * email -> Email account
        * key -> Global API Key

        >>> cf.auth("cloudflare@example.com", "your-global-api-key")
        """

        self._headers = {
            "X-Auth-Email": email,
            "X-Auth-Key": key,
            "Content-Type": "application/json"
        }

    def auth_bearer(self, bearer: str) -> None:
        """Generate a specific token through cloudflare profile (API Tokens section)

        .. warning::
            This will grant only specific domains/permissions access to this API library

        https://dash.cloudflare.com/profile/api-tokens

        * bearer -> Bearer token

        >>> cf.auth_bearer("your-specific-bearer-token")
        """

        self._headers = {
            "Authorization": "Bearer " + bearer,
            "Content-Type": "application/json"
        }

    def beautify(self, expression: str) -> str:
        """Beautify a cloudflare expression

        >>> cf.beautify("(cf.client.bot) or (cf.threat_score ge 1)")
        # (cf.client.bot) or
          (cf.threat_score ge 1)
        """

        return expression.replace(" or ", " or\n").replace(" and ", " and\n")

    def get_domains(self: str) -> dict:
        """Get all domains

        >>> cf.get_domains()
        >>> {"count": 1, "domains": ["example.com"], "result": [{"id": "---", "name": "example.com", ...}]}
        """

        r = requests.get("https://api.cloudflare.com/client/v4/zones/", headers=self._headers)

        zones_count = self.error.handle(r.json(), ["result_info", "count"])
        zones = [x["name"] for x in self.error.handle(r.json(), ["result"])]

        return {
            "count": zones_count,
            "domains": zones,
            "result": self.error.handle(r.json(), ["result"])
        }

    @property
    def domains(self) -> dict:
        """Get all domains

        Alias for :func:`get_domains`

        >>> cf.get_domains()
        >>> {"count": 1, "domains": ["example.com"], "result": [{"id": "123", "name": "example.com", ...}]}
        """

        return self.get_domains()

    def get_domain(self, domain_name: str) -> dict:
        """Get all domains

        :exception SystemExit: If domain not found (:func:`get_domains`)

        .. important::
            This function is the "core" for all other functions, it raise a SystemExit exception because nothing else can work without a domain

        >>> cf.get_domain("example.com")
        >>> {"id": "---", "name": "example.com", ...}
        """

        r = requests.get(f"https://api.cloudflare.com/client/v4/zones/?name={domain_name}", headers=self._headers)

        zone = self.error.handle(r.json(), ["result", 0])

        if not zone:
            raise SystemExit(f"Domain '{domain_name}' not found")

        return zone

    def set_plan(self, domain_name: str) -> True:
        """Save current website plan

        .. note::
            Will define the current plan of the website in the instance of the class

        >>> cf.set_plan("example.com")
        """

        self.plan = self.get_domain(domain_name)["plan"]["legacy_id"]

        match self.plan:
            case "free":
                self.rules = 5
            case "pro":
                self.rules = 20
            case "business":
                self.rules = 100
            case "enterprise":
                self.rules = 1000

        return True

    def get_rules(self, domain_name: str) -> dict:
        """Get all rules from a specific domain

        >>> cf.get_rules("example.com")
        >>> {"count": 3, "rules": ["Test", "Bad Bots", "Bad AS"], "result": [{"id": "123", "description": "Test", ...}]}
        """

        zone = self.get_domain(domain_name)
        zone_id = zone["id"]

        r = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/rules", headers=self._headers)

        rules_count = self.error.handle(r.json(), ["result_info", "count"])
        rules = [x["description"] for x in self.error.handle(r.json(), ["result"])]

        self.active_rules = rules_count

        return {
            "count": rules_count,
            "rules": rules,
            "result": self.error.handle(r.json(), ["result"])
        }

    def get_rule(self, domain_name: str, rule_name: str) -> dict | str:
        """Get a specific rule from a specific domain



        >>> cf.get_rule("example.com", "Bad Bots")
        >>> {"id": "123", "paused": False, "description": "Bad Bots", "action": "block", "filter": {"id": "456", "expression": "(http.user_agent contains "python-requests/")" ...}}
        """

        zone = self.get_domain(domain_name)
        zone_id = zone["id"]

        r = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/rules?description={rule_name}", headers=self._headers)

        rule = self.error.handle(r.json(), ["result", 0])

        if not rule:
            print(f"Rule '{rule_name}' not found")
            return

        return rule

    def export_rules(self, domain_name: str) -> True:
        """Export all expressions from a specific domain

        .. note::
            Will save all expressions into multiple files in the folder specified in the constructor

        >>> cf.export_rules("example.com")
        # "Test.txt", "Bad Bots.txt", "Bad AS.txt" files created in "my_expressions/" folder
        """

        rules = self.get_rules(domain_name)

        for rule in rules["result"]:
            rule_expression = self.beautify(rule["filter"]["expression"])

            self.utils.write_expression(rule["description"], rule_expression)

        return True

    def export_rule(self, domain_name: str, rule_name: str, custom_name: str = None) -> True:
        """Export the expression of a rule in a txt file    

        .. note::
            Will save the expression into a file in the folder specified in the constructor

        >>> cf.export_rule("example.com", "Bad Bots")
        # "Bad Bots.txt" file created in "my_expressions/" folder
        """

        rule = self.get_rule(domain_name, rule_name)
        if custom_name:
            rule_name = custom_name
        else:
            rule_name = rule["description"]
        rule_expression = self.beautify(rule["filter"]["expression"])

        self.utils.write_expression(rule_name, rule_expression)

        return True

    def create_rule(self, domain_name: str, rule_name: str, rule_file: str, action: str = "block") -> bool:
        """Create a rule with a specific expression

        * action -> Please refer to https://developers.cloudflare.com/firewall/cf-firewall-rules/actions/

        >>> cf.create_rule("example.com", "Second Test", "Test2", "challenge")
        """

        zone = self.get_domain(domain_name)
        zone_id = zone["id"]

        new_rule = [{
            "description": rule_name,
            "action": action,
            "filter": {
                "expression": self.utils.read_expression(rule_file)
            }
        }]

        if self.active_rules < self.rules:
            r = requests.post(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/rules", headers=self._headers, json=new_rule)

        return self.error.handle(r.json(), ["success"])

    def update_rule(self, domain_name: str, rule_name: str, rule_file: str) -> bool:
        """Update a rule with a specific expression

        .. todo::
            First modify "Test2.txt" by changing the expression or adding a new rule

        >>> cf.update_rule("example.com", "Second Test", "Test2")
        """

        zone = self.get_domain(domain_name)
        zone_id = zone["id"]

        filter = self.get_rule(domain_name, rule_name)
        if filter:
            filter = filter["filter"]
            filter_id = filter["id"]
        else:
            return {"error": "Filter not found"}

        new_filter = filter.copy()
        new_filter["expression"] = self.utils.read_expression(rule_file)

        r = requests.put(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/filters/{filter_id}", headers=self._headers, json=new_filter)

        return self.error.handle(r.json(), ["success"])

    def import_rules(self, domain_name: str, actions_all: str = "block") -> bool:
        """Import all expressions from all txt file

        * actions_all -> Set the same action for all imported rules, please refer to https://developers.cloudflare.com/firewall/cf-firewall-rules/actions/

        .. note::
            If you have a better plan, please register your plan using the method :func:`set_plan`

        >>> cf.import_rules("example.com", "js_challenge")
        """

        files = os.listdir(self.utils.directory)

        rules = [self.utils.escape(x)
                 for x in self.get_rules(domain_name)["rules"]]

        self.active_rules = len(rules)

        for file in files:
            if file.endswith(".txt"):
                name = self.utils.unescape(file.split(".")[0])
                if not name in rules:
                    if self.active_rules < self.rules:
                        print("Creating rule:", name)
                        self.create_rule(domain_name, name, name, actions_all)
                        self.active_rules += 1
                    else:
                        print("Cannot create more rules ({} used / {} available)".format(self.active_rules, self.rules))
                        print("If you have a better plan, please register the domain plan using cf.set_plan(\"<your-domain>\")")
                        break

        return True

    import_rule = create_rule
    """Import a rule with a specific expression
    
    Alias for :func:`create_rule`
    
    >>> cf.import_rule("example.com", "Second Test", "Test2", "challenge")
    """



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

    def write_expression(self, rule_name: str, rule_expression: str) -> None:
        """Write an expression to a readable text file

        >>> utils.write_expression("IsBot", "(cf.client.bot)")
        """

        with open(f"{self.directory}/{self.escape(rule_name)}.txt", "w") as file:
            file.write(rule_expression)

    def read_expression(self, rule_file: str) -> str:
        """Read an expression from a file

        >>> utils.read_expression("IsBot")
        >>> "(cf.client.bot)"
        """

        filename = f"{self.directory}/{self.escape(rule_file)}.txt"

        if os.path.isfile(filename):
            with open(filename, "r") as file:
                expression = [x.strip() for x in file.readlines()]
        else:
            print(f"No such file in folder '{self.directory}'")
            return

        return " ".join(expression)

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

    def handle(self, request_json: dict, keys: list[str | int]) -> bool | dict:
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
            if any(x in request_json["errors"][0]["code"] for x in [10000, 9109]):
                raise SystemExit(request_json["errors"][0]["message"])

        if request_json["success"]:
            return self.utils.get_json_key(request_json, keys)
        else:
            return {"error": self.utils.get_json_key(request_json, ["errors", 0, "message"])}
