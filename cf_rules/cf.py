import requests, os

from cf_rules.utils import Utils, Error

class DomainObject(dict):
    def __init__(self, *args, **kwargs):
        super(DomainObject, self).__init__(*args, **kwargs)
        self.__dict__ = self

class RuleObject(dict):
    def __init__(self, *args, **kwargs):
        super(RuleObject, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Cloudflare:
    def __init__(self, folder: str = None):
        """Initialize Cloudflare class

        Specify a folder argument where expressions will be saved

        >>> cf = Cloudflare("my_expressions")
        """

        self.utils = Utils(folder)
        self.error = Error()

        self.plan = "free"
        self.max_rules = 5
        self.active_rules = 0

    def auth_key(self, email: str, key: str) -> dict:
        """Get your global API Key through cloudflare profile (API Keys section)

        .. warning::
            This will grant all domains access to this API library, prefer using :func:`auth_token`

        https://dash.cloudflare.com/profile/api-tokens

        * email -> Email account
        * key -> Global API Key

        >>> cf.auth_key("cloudflare@example.com", "your-global-api-key")
        >>> {"success": True, {"result": {"id": "123", "email": "cloudflare@example.com", ...}}
        # OR
        >>> {"success": False, "errors": [{"code": 6003, "message": "Invalid request headers", ...}]}
        """

        if not email:
            raise SystemExit("You must provide an email")

        if not key:
            raise SystemExit("You must provide an API key")

        self._headers = {
            "X-Auth-Email": email,
            "X-Auth-Key": key,
            "Content-Type": "application/json"
        }

        r = requests.get("https://api.cloudflare.com/client/v4/user", headers=self._headers)

        return r.json()

    auth = auth_key

    def auth_token(self, bearer_token: str) -> dict:
        """Generate a specific token through cloudflare profile (API Tokens section)

        .. note::
            This will grant only specific domains/permissions access to this API library

        https://dash.cloudflare.com/profile/api-tokens

        * bearer_token -> API Token

        >>> cf.auth_token("your-specific-bearer-token")
        >>> {"success": True, {"result": {"id": "123", "status": "active"}}, ...}
        # OR
        >>> {"success": False, "errors": [{"code": 9109, "message": "Invalid access token", ...}]}
        """

        if not bearer_token:
            raise SystemExit("You must provide a bearer token")

        self._headers = {
            "Authorization": "Bearer " + bearer_token,
            "Content-Type": "application/json"
        }

        r = requests.get("https://api.cloudflare.com/client/v4/user/tokens/verify", headers=self._headers)

        return r.json()

    auth_bearer = auth_token

    def beautify(self, expression: str) -> str:
        """Beautify a cloudflare expression

        >>> cf.beautify("(cf.client.bot) or (cf.threat_score ge 1)")
        # (cf.client.bot) or
        # (cf.threat_score ge 1)
        """

        return expression.replace(" or ", " or\n").replace(" and ", " and\n")

    def get_domains(self: str) -> dict:
        """Get all domains

        >>> cf.get_domains()
        >>> {"count": 1, "domains": ["example.com"], "result": [{"id": "123", "name": "example.com", ...}]}
        """

        if not hasattr(self, "_headers"):
            raise SystemExit("You must authenticate first, use cf.auth_key(email, key) or cf.auth_token(bearer)")

        r = requests.get("https://api.cloudflare.com/client/v4/zones", headers=self._headers)

        zones_count = self.error.handle(r.json(), ["result_info", "count"])
        zones = [x["name"] for x in self.error.handle(r.json(), ["result"])]

        return {
            "count": zones_count,
            "domains": zones,
            "result": self.error.handle(r.json(), ["result"])
        }

    @property
    def domains(self) -> list[DomainObject]:
        """Get all domains as a list of :class:`DomainObject`

        Access any value of the object with the dot operator

        Better handling compared to :func:`get_domains`, return directly the result key of the function

        >>> cf.domains
        >>> [{"id": "123", "name": "example.com", ...}, {"id": "456", "name": "example.net", ...}]
        """

        return [DomainObject(x) for x in self.get_domains()["result"]]

    def get_domain(self, domain_name: str) -> DomainObject:
        """Get a specific domain as :class:`DomainObject`

        :exception SystemExit: If domain is not found (list all domains using cf.domains)

        .. important::
            This function is the "core" for all other functions, it raise a SystemExit exception because nothing else can work without a domain

        >>> cf.get_domain("example.com")
        >>> {"id": "123", "name": "example.com", ...}
        >>> domain = cf.get_domain("example.com")
        >>> domain.name # OR domain["name"]
        >>> "example.com"
        """

        if not hasattr(self, "_headers"):
            raise SystemExit("You must authenticate first, use cf.auth_key(email, key) or cf.auth_token(bearer)")

        r = requests.get(f"https://api.cloudflare.com/client/v4/zones/?name={domain_name}", headers=self._headers)

        domain = self.error.handle(r.json(), ["result", 0])

        if not domain:
            raise SystemExit(f"Domain '{domain_name}' not found")

        return DomainObject(domain)

    def set_plan(self, domain_name: str) -> True:
        """Save current website plan

        .. note::
            Will define the current plan of the website in the instance of the class

        >>> cf.set_plan("example.com")
        """

        self.plan = self.get_domain(domain_name)["plan"]["legacy_id"]

        match self.plan:
            case "free":
                self.max_rules = 5
            case "pro":
                self.max_rules = 20
            case "business":
                self.max_rules = 100
            case "enterprise":
                self.max_rules = 1000

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

    def rules(self, domain_name: str) -> list[RuleObject]:
        """Get all rules as a list of :class:`RuleObject`

        Access any value of the object with the dot operator

        Better handling compared to :func:`get_rules()`, return directly the result key of the function

        >>> cf.rules
        >>> [{"id": "123", "description": "Test", ...}, {"id": "456", "description": "Test2", ...}]
        """

        return [RuleObject(x) for x in self.get_rules(domain_name)["result"]]

    def get_rule(self, domain_name: str, rule_name: str) -> RuleObject:
        """Get a specific rule from a specific domain as :class:`RuleObject`

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

        return RuleObject(rule)

    def export_rules(self, domain_name: str) -> True:
        """Export all expressions from a specific domain

        .. note::
            Will save all expressions into multiple files in the folder specified in the constructor

        >>> cf.export_rules("example.com")
        # "Test.txt", "Bad Bots.txt", "Bad AS.txt" files created in "my_expressions/" folder
        """

        rules = self.get_rules(domain_name)

        for rule in rules["result"]:
            header = {
                "action": rule["action"],
                "paused": rule["paused"]
            }
            if "priority" in rule:
                header["priority"] = rule["priority"]

            rule_expression = self.beautify(rule["filter"]["expression"])

            self.utils.write_expression(rule["description"], rule_expression, header=header)

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

        header = {
            "action": rule["action"],
            "paused": rule["paused"],
            "priority": rule["priority"]
        }
        rule_expression = self.beautify(rule["filter"]["expression"])

        self.utils.write_expression(rule_name, rule_expression, header=header)

        return True

    def create_rule(self, domain_name: str, rule_name: str, rule_file: str, action: str = None) -> bool:
        """Create a rule with a specific expression

        * action -> Please refer to https://developers.cloudflare.com/firewall/cf-firewall-rules/actions/

        Available actions as string:
        `block, challenge, js_challenge, managed_challenge, allow, log, bypass`

        >>> cf.create_rule("example.com", "Second Test", "Test2")
        # Create a rule with the expression in "Test2.txt", will use the action in the header if specified
        >>> cf.create_rule("example.com", "Second Test", "Test2", "managed_challenge")
        """

        zone = self.get_domain(domain_name)
        zone_id = zone["id"]

        header, expression = self.utils.read_expression(rule_file)

        new_rule = [{
            "description": rule_name,
            "filter": {
                "expression": expression
            }
        }]

        if header:
            if action or "action" in header:
                new_rule[0]["action"] = action if action else header["action"]
            if "paused" in header:
                new_rule[0]["paused"] = header["paused"]
            if "priority" in header:
                new_rule[0]["priority"] = header["priority"]
        else:
            new_rule[0]["action"] = action if action else "managed_challenge"

        if self.active_rules < self.max_rules:
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

        rule = self.get_rule(domain_name, rule_name)

        if rule:
            updated_rule = rule.copy()
            rule_id = updated_rule["id"]
        else:
            return {"error": "Rule not found"}

        header, expression = self.utils.read_expression(rule_file)

        if header:
            if "action" in header:
                updated_rule["action"] = header["action"]
            if "paused" in header:
                updated_rule["paused"] = header["paused"]
            if "priority" in header:
                updated_rule["priority"] = header["priority"]

        updated_rule["filter"]["expression"] = expression

        r = requests.put(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/rules/{rule_id}", headers=self._headers, json=updated_rule)

        return self.error.handle(r.json(), ["success"])

    def delete_rule(self, domain_name: str, rule_name: str) -> bool:
        """Delete a rule from a specific domain

        >>> cf.delete_rule("example.com", "Second Test")
        """

        zone = self.get_domain(domain_name)
        zone_id = zone["id"]

        rule = self.get_rule(domain_name, rule_name)

        if rule:
            rule_id = rule["id"]
        else:
            return {"error": "Rule not found"}

        r = requests.delete(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/rules/{rule_id}", headers=self._headers)

        return self.error.handle(r.json(), ["success"])

    def purge_rules(self, domain_name: str) -> bool:
        """Purge all rules from a specific domain

        >>> cf.purge_rules("example.com")
        """

        rules = self.get_rules(domain_name)["rules"]

        for rule in rules:
            self.delete_rule(domain_name, rule)

        self.active_rules = 0

        return True

    def import_rules(self, domain_name: str, actions_all: str = None) -> bool:
        """Import all expressions from all txt file

        * actions_all -> Set the same action for all imported rules, please refer to https://developers.cloudflare.com/firewall/cf-firewall-rules/actions/

        Available actions as string:
        `block, challenge, js_challenge, managed_challenge, allow, log, bypass`

        .. note::
            If you have a better plan, please register your plan using the method :func:`set_plan`

        >>> cf.import_rules("example.com")
        # Will use the action in the header specific for every file
        >>> cf.import_rules("example.com", "block")
        # Set all rules to block action
        """

        files = os.listdir(self.utils.directory)

        rules = [self.utils.escape(x)
                 for x in self.get_rules(domain_name)["rules"]]

        self.active_rules = len(rules)

        for file in files:
            if file.endswith(".txt"):
                name = self.utils.unescape(file.split(".")[0])
                if not name in rules:
                    if self.active_rules < self.max_rules:
                        print("Creating rule:", name)
                        if actions_all:
                            self.create_rule(domain_name, name, name, actions_all)
                        else:
                            self.create_rule(domain_name, name, name)
                        self.active_rules += 1
                    else:
                        print("Cannot create more rules ({} used / {} available)".format(self.active_rules, self.max_rules))
                        print("If you have a better plan, please register the domain plan using cf.set_plan(\"<your-domain>\")")
                        break

        return True

    import_rule = create_rule
    """Import a rule with a specific expression
    
    Alias for :func:`create_rule`
    
    >>> cf.import_rule("example.com", "Second Test", "Test2", "managed_challenge")
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
