import requests, os

class Cloudflare:
    def __init__(self, email, key, folder=None):
        """Generate a specific token through cloudflare profile
        https://dash.cloudflare.com/profile/api-tokens
        * email -> Email account
        * key -> Global API Key
        """

        self._headers = {
            "X-Auth-Email": email,
            "X-Auth-Key": key,
            "Content-Type": "application/json"
        }

        self.utils = Utils(folder)
        self.error = Error()

        self.plan = "free"
        self.rules = 5
        self.active_rules = 0

    def beautify(self, expression):
        """Beautify a cloudflare expression"""

        return expression.replace(" or ", " or\n").replace(" and ", " and\n")

    def get_domains(self):
        """Get all domains"""

        r = requests.get("https://api.cloudflare.com/client/v4/zones/", headers=self._headers)

        zones_count = self.error.handle(r.json(), ["result_info", "count"])
        zones = [x["name"] for x in self.error.handle(r.json(), ["result"])]

        return {
            "count": zones_count,
            "domains": zones,
            "result": self.error.handle(r.json(), ["result"])
        }

    @property
    def domains(self):
        return self.get_domains()

    def get_domain(self, domain_name):
        """Get a specific domain"""

        r = requests.get(f"https://api.cloudflare.com/client/v4/zones/?name={domain_name}", headers=self._headers)

        zone = self.error.handle(r.json(), ["result", 0])

        if not zone:
            exit(f"Domain '{domain_name}' not found")

        return zone

    def set_plan(self, domain_name):
        """Save current website plan"""

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

    def get_rules(self, domain_name):
        """Get all rules from a specific domain"""

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

    def get_rule(self, domain_name, rule_name):
        """Get a specific rule from a specific domain"""

        zone = self.get_domain(domain_name)
        zone_id = zone["id"]

        r = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/rules?description={rule_name}", headers=self._headers)

        rule = self.error.handle(r.json(), ["result", 0])

        if not rule:
            exit(f"Rule '{rule_name}' not found")

        return rule

    def export_rules(self, domain_name):
        """Export all expressions from a specific domain"""

        rules = self.get_rules(domain_name)

        for rule in rules["result"]:
            rule_expression = self.beautify(rule["filter"]["expression"])

            self.utils.write_expression(rule["description"], rule_expression)

        return True

    def export_rule(self, domain_name, rule_name, custom_name=None):
        """Export the expression of a rule in a txt file"""

        rule = self.get_rule(domain_name, rule_name)
        if custom_name:
            rule_name = custom_name
        else:
            rule_name = rule["description"]
        rule_expression = self.beautify(rule["filter"]["expression"])

        self.utils.write_expression(custom_name, rule_expression)

        return True

    def create_rule(self, domain_name, rule_name, rule_file, action="block"):
        """Create a rule with a specific expression"""

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

    def update_rule(self, domain_name, rule_name, rule_file):
        """Update a rule with a specific expression"""

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

    def import_rules(self, domain_name, actions_all="block"):
        """Import all expressions from all txt file"""

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
                        break

        return True

    import_rule = create_rule



class Utils:
    def __init__(self, directory=None):
        self.directory = directory if directory else "expressions"

        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

    def escape(self, string):
        """Escape a string"""

        # return "".join(c if c.isalnum() else "_" for c in string)
        return string.replace("/", "_")

    def unescape(self, string):
        """Unescape a string"""

        # return string.replace("___", " - ").replace("_", " ")
        return string.replace("_", "/")

    def write_expression(self, rule_name, rule_expression):
        """Write an expression to a readable text file"""

        with open(f"{self.directory}/{self.escape(rule_name)}.txt", "w") as file:
            file.write(rule_expression)

    def read_expression(self, rule_file):
        """Read an expression from a file"""

        filename = f"{self.directory}/{self.escape(rule_file)}.txt"

        if os.path.isfile(filename):
            with open(filename, "r") as file:
                expression = [x.strip() for x in file.readlines()]
        else:
            print(f"No such file in folder '{self.directory}'")
            return

        return " ".join(expression)

    def get_json_key(self, json, keys):
        """Get an element from a json using a list of keys"""

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
        self.utils = Utils()

    def handle(self, request_json, keys):
        if request_json["success"]:
            return self.utils.get_json_key(request_json, keys)
        else:
            return {"error": self.utils.get_json_key(request_json, ["errors", 0, "message"])}
