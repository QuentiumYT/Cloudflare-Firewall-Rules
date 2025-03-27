import os

import requests

from .error import Error
from .utils import Utils


class DomainObject(dict):
    def __init__(self, *args, **kwargs):
        super(DomainObject, self).__init__(*args, **kwargs)
        self.__dict__ = self


class RuleObject(dict):
    def __init__(self, *args, **kwargs):
        super(RuleObject, self).__init__(*args, **kwargs)
        self.__dict__ = self


class RulesetObject(dict):
    def __init__(self, *args, **kwargs):
        super(RulesetObject, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Cloudflare:
    def __init__(self, folder: str | None = None):
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

        :exception Error: Email or key is not provided

        .. warning::
            This will grant all domains access to this API library, prefer using :func:`auth_token`

        https://dash.cloudflare.com/profile/api-tokens

        * email -> Email account
        * key -> Global API Key

        >>> cf.auth_key("cloudflare@example.com", "your-global-api-key")
        >>> {"success": True, "result": {"id": "a1b2c3", "email": "cloudflare@example.com", ...}}
        # OR
        >>> {"success": False, "errors": [{"code": 6003, "message": "Invalid request headers", ...}]}
        """

        if not email:
            raise Error("You must provide an email")

        if not key:
            raise Error("You must provide an API key")

        self._headers = {
            "X-Auth-Email": email,
            "X-Auth-Key": key,
            "Content-Type": "application/json",
        }

        r = requests.get("https://api.cloudflare.com/client/v4/user", headers=self._headers, timeout=5)

        return r.json()

    def auth_token(self, bearer_token: str) -> dict:
        """Generate a specific token through cloudflare profile (API Tokens section)

        :exception Error: Bearer token is not provided

        .. note::
            This will grant only specific domains/permissions related access to this API library

        https://dash.cloudflare.com/profile/api-tokens

        * bearer_token -> API Token

        >>> cf.auth_token("your-specific-bearer-token")
        >>> {"success": True, "result": {"id": "a1b2c3", "status": "active"}, ...}
        # OR
        >>> {"success": False, "errors": [{"code": 1000, "message": "Invalid API token"}], ...}
        """

        if not bearer_token:
            raise Error("You must provide a bearer token")

        self._headers = {
            "Authorization": "Bearer " + bearer_token,
            "Content-Type": "application/json",
        }

        r = requests.get("https://api.cloudflare.com/client/v4/user/tokens/verify", headers=self._headers, timeout=5)

        return r.json()

    def get_domains(self: str) -> dict:
        """Get all domains

        :exception Error: If not authenticated (use :func:`auth_key(email, key) <auth_key>` or :func:`auth_token(bearer_token) <auth_token>`)

        >>> cf.get_domains()
        >>> {"count": 2, "domains": ["example.com", "example.fr"], "result": [{"id": "a1b2c3", "name": "example.com", ...}, ...]}
        """

        if not hasattr(self, "_headers"):
            raise Error("You must authenticate first, use cf.auth_key(email, key) or cf.auth_token(bearer_token)")

        r = requests.get("https://api.cloudflare.com/client/v4/zones", headers=self._headers, timeout=5)

        zones = self.error.handle(r.json(), ["result"])

        if not zones:
            raise Error("No domain found")

        return {
            "count": len(zones),
            "domains": [x["name"] for x in zones],
            "result": zones,
        }

    @property
    def domains(self) -> list[DomainObject]:
        """Get all domains as a list of :class:`DomainObject`

        Access any value of the object with the dot operator

        Better handling compared to :func:`get_domains`, return directly the result key of the function

        >>> cf.domains
        >>> [{"id": "a1b2c3", "name": "example.com", ...}, {"id": "d4e5f6", "name": "example.fr", ...}]
        """

        return [DomainObject(x) for x in self.get_domains()["result"]]

    def get_domain(self, domain_name: str) -> DomainObject:
        """Get a specific domain as :class:`DomainObject`

        :exception Error: If not authenticated (use :func:`auth_key(email, key) <auth_key>` or :func:`auth_token(bearer_token) <auth_token>`)
        :exception Error: If domain is not found (list all domains using cf.domains)

        .. important::
            This function is the "core" for all other functions,
            it is needed for every other function to work

        >>> cf.get_domain("example.com")
        >>> {"id": "a1b2c3", "name": "example.com", ...}
        >>> domain = cf.get_domain("example.fr")
        >>> domain.name # OR domain["name"]
        >>> "example.fr"
        """

        if not hasattr(self, "_headers"):
            raise Error("You must authenticate first, use cf.auth_key(email, key) or cf.auth_token(bearer_token)")

        r = requests.get(f"https://api.cloudflare.com/client/v4/zones?name={domain_name}", headers=self._headers, timeout=5)

        domain = self.error.handle(r.json(), ["result"])

        if not domain:
            raise Error(f"Domain '{domain_name}' not found")

        domain = domain[0]

        if "error" in domain:
            raise Error(domain["error"])

        return DomainObject(domain)

    def set_plan(self, domain_name: str):
        """Save current website plan

        .. note::
            Will define the current plan of the website in the instance of the class

        >>> cf.set_plan("example.com")
        # Now the maximum available rules for this domain depends on the current plan
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

    def get_rulesets(self, domain_name: str) -> dict:
        """Get all rulesets from a specific domain

        >>> cf.get_rulesets("example.com")
        >>> {"count": 4, "rulesets": ["default", "Cloudflare Normalization Ruleset", ...], "result": [{"id": "a1b2c3", "name": "default", ...}]}
        """

        zone = self.get_domain(domain_name)
        zone_id = zone["id"]

        r = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets", headers=self._headers, timeout=5)

        rulesets = self.error.handle(r.json(), ["result"])

        return {
            "zone_id": zone_id,
            "count": len(rulesets),
            "rulesets": [x["name"] for x in rulesets],
            "result": rulesets,
        }

    def rulesets(self, domain_name: str) -> list[RulesetObject]:
        """Get all rulesets as a list of :class:`RulesetObject`

        Access any value of the object with the dot operator

        Better handling compared to :func:`get_rulesets()`, return directly the result key of the function

        >>> cf.rulesets
        >>> [{"id": "a1b2c3", "name": "default", ...}, {"id": "d4e5f6", "name": "Cloudflare Normalization Ruleset", ...}]
        """

        return [RulesetObject(x) for x in self.get_rulesets(domain_name)["result"]]

    def get_custom_ruleset(self, domain_name: str) -> RulesetObject:
        """Get the custom ruleset from a specific domain as :class:`RulesetObject`

        It should be the only ruleset with the source "firewall_custom" as per Cloudflare's documentation.
        This is the ruleset where all custom rules are stored.

        :exception Error: If no custom ruleset is found

        >>> cf.get_custom_ruleset("example.com")
        >>> {"id": "a1b2c3", "name": "default", "source": "firewall_custom", ...}
        """

        rulesets = self.get_rulesets(domain_name)

        custom_ruleset = [x for x in rulesets["result"] if x.get("source") == "firewall_custom"]

        if not custom_ruleset:
            raise Error("No custom ruleset found")

        custom_ruleset = custom_ruleset[0]

        if "error" in custom_ruleset:
            raise Error(custom_ruleset["error"])

        custom_ruleset["zone_id"] = rulesets["zone_id"]

        return RulesetObject(custom_ruleset)

    def get_rules(self, domain_name: str) -> dict:
        """Get all rules from a specific domain

        :exception Error: If no rules are found

        >>> cf.get_rules("example.com")
        >>> {"count": 3, "rules": ["Bad Bots", "Bad IP", "Bad AS"], "result": [{"id": "a1b2c3", "description": "Bad Bots", ...}, ...]}
        """

        ruleset = self.get_custom_ruleset(domain_name)
        zone_id = ruleset["zone_id"]
        custom_ruleset_id = ruleset["id"]

        r = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{custom_ruleset_id}", headers=self._headers, timeout=5)

        rules = self.error.handle(r.json(), ["result", "rules"])

        if not rules:
            raise Error("No rules found")

        # No rules found (handle silently fails), return empty list
        if isinstance(rules, dict):
            rules = []

        self.active_rules = len(rules)

        return {
            "zone_id": zone_id,
            "custom_ruleset_id": custom_ruleset_id,
            "count": len(rules),
            "rules": [x["description"] for x in rules],
            "result": rules,
        }

    def rules(self, domain_name: str) -> list[RuleObject]:
        """Get all rules as a list of :class:`RuleObject`

        Access any value of the object with the dot operator

        Better handling compared to :func:`get_rules()`, return directly the result key of the function

        >>> cf.rules
        >>> [{"id": "a1b2c3", "description": "Bad Bots", ...}, {"id": "d4e5f6", "description": "Bad IP", ...}, ...]
        """

        return [RuleObject(x) for x in self.get_rules(domain_name)["result"]]

    def get_rule(self, domain_name: str, *, rule_name: str | None = None, rule_id: str | None = None) -> RuleObject:
        """Get a specific rule by name or ID from a specific domain as :class:`RuleObject`

        :exception Error: Rule name or rule ID is not provided
        :exception Error: If no rule is found with the specified name

        >>> cf.get_rule("example.com", rule_name="Bad Bots")
        >>> {"id": "a1b2c3", "enabled": True, "action": "block", "description": "Bad Bots", "expression": "(http.user_agent contains "DotBot")", ...}
        """

        if rule_id:
            rules = self.get_rules(domain_name)
            rule = [x for x in rules["result"] if x["id"] == rule_id]
        elif rule_name:
            rules = self.get_rules(domain_name)
            rule = [x for x in rules["result"] if x["description"] == rule_name]
        else:
            raise Error("You must provide a rule_name or rule_id")

        if not rule:
            raise Error(f"Rule '{rule_name}' not found")

        rule = rule[0]

        if "error" in rule:
            raise Error(rule["error"])

        rule["zone_id"] = rules["zone_id"]
        rule["custom_ruleset_id"] = rules["custom_ruleset_id"]

        return RuleObject(rule)

    def export_rules(self, domain_name: str) -> True:
        """Export all expressions from a specific domain

        .. note::
            Will save all expressions into multiple files in the folder specified in Cloudflare's constructor

        >>> cf.export_rules("example.com")
        # "Bad Bots.txt", "Bad IP.txt", "Bad AS.txt" files created in "my_expressions" folder
        """

        rules = self.get_rules(domain_name)

        for rule in rules["result"]:
            print(f"Exporting {rule['description']}...")

            header = {
                "id": rule["id"],
                "action": rule["action"],
                "enabled": rule["enabled"],
            }

            rule_expression = self.utils.beautify(rule["expression"])

            self.utils.write_expression(rule["description"], rule_expression, header=header)

        return True

    def export_rule(self, domain_name: str, *, rule_name: str | None = None, rule_id: str | None = None) -> True:
        """Export the expression of a rule in a txt file

        :exception Error: Rule name or rule ID is not provided

        .. note::
            Will save the expression into a file in the folder specified in Cloudflare's constructor

        >>> cf.export_rule("example.com", "Bad Bots")
        # "Bad Bots.txt" file created in "my_expressions" folder
        """

        if rule_id:
            rule = self.get_rule(domain_name, rule_id=rule_id)
        elif rule_name:
            rule = self.get_rule(domain_name, rule_name=rule_name)
        else:
            raise Error("You must provide a rule_name or rule_id")

        header = {
            "id": rule["id"],
            "action": rule["action"],
            "enabled": rule["enabled"],
        }

        rule_expression = self.utils.beautify(rule["expression"])

        self.utils.write_expression(rule_name, rule_expression, header=header)

        return True

    def create_rule(self, domain_name: str, rule_file: str, rule_name: str | None = None, action: str | None = None, position: int | None = None) -> bool:
        """Create a rule with a specific expression

        * action -> Please refer to https://developers.cloudflare.com/ruleset-engine/rules-language/actions/

        Available actions as string:
        `managed_challenge, js_challenge, challenge, block, skip, log`

        Action is read from the header of the file by default, but you can specify it manually. Else it will be "managed_challenge"

        * position -> Rule position, with 1 being the first rule in the list

        :exception Error: Rule file is not found
        :exception Error: Rule already exists in remote WAF
        :exception Error: Cannot create more rules (5 used / 5 available depending on the current plan)

        >>> cf.create_rule("example.com", "Bad URL.txt", action="managed_challenge")
        # Create a rule with the expression in "Bad URL.txt" and override the action to "managed_challenge"
        >>> cf.create_rule("example.com", "Bad IP.txt", "Not allowed IP")
        # Create a rule named "Not allowed IP" with the expression in "Bad IP.txt" with the action in the header of the file
        """

        if not rule_name:
            rule_name = rule_file.strip(".txt")

        rules = self.get_rules(domain_name)
        zone_id = rules["zone_id"]
        custom_ruleset_id = rules["custom_ruleset_id"]

        header, expression = self.utils.read_expression(rule_file)

        if not expression:
            raise Error(f"No such file in folder '{self.utils.directory}'")

        if rule_name in rules["rules"]:
            raise Error(f"Rule '{rule_name}' already exists")

        new_rule = {
            "description": rule_name,
            "expression": expression,
        }

        if position:
            new_rule["position"] = {"index": position}

        if header:
            if action or "action" in header:
                new_rule["action"] = action or header["action"]
            else:
                new_rule["action"] = "managed_challenge"
            if "enabled" in header:
                new_rule["enabled"] = header["enabled"]
        else:
            new_rule["action"] = action or "managed_challenge"

        if new_rule["action"] == "skip":
            new_rule["action_parameters"] = {
                "phases": [
                    "http_request_firewall_managed",
                    "http_request_sbfm",
                    "http_ratelimit",
                ],
                "products": [],
                "ruleset": "current",
            }

        if self.active_rules < self.max_rules:
            r = requests.post(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{custom_ruleset_id}/rules", headers=self._headers, json=new_rule, timeout=5)
        else:
            raise Error(f"Cannot create more rules ({self.active_rules} used / {self.max_rules} available)\n"
                        "\t\t\tIf you have a better plan, please register the domain plan using cf.set_plan(\"<your-domain>\")")

        return self.error.handle(r.json(), ["success"])

    def update_rule(self, domain_name: str, rule_file: str, rule_name: str | None = None, action: str | None = None, position: int | None = None) -> bool:
        """Update a rule with a specific expression

        :exception Error: Rule file is not found

        .. todo::
            First modify "Bad Bots.txt" by changing the expression or adding a new rule

        * position -> Rule position, starting from 1

        >>> cf.update_rule("example.com", "Bad Bots.txt")
        # Will update the remote rule "Bad Bots" with the expression in "Bad Bots.txt"
        >>> cf.update_rule("example.com", "Bad IP.txt", "Not allowed IP", "block")
        # Will update the remote rule "Not allowed IP" with the expression in "Bad IP.txt" and override the action to "block"
        """

        if not rule_name:
            rule_name = rule_file.strip(".txt")

        rule = self.get_rule(domain_name, rule_name=rule_name)
        zone_id = rule["zone_id"]
        custom_ruleset_id = rule["custom_ruleset_id"]
        rule_id = rule["id"]

        updated_rule = rule.copy()
        del updated_rule["zone_id"]
        del updated_rule["custom_ruleset_id"]
        del updated_rule["id"]

        header, expression = self.utils.read_expression(rule_file)

        if not expression:
            raise Error(f"No such file in folder '{self.utils.directory}'")

        if header:
            if action or "action" in header:
                updated_rule["action"] = action or header["action"]
            if "enabled" in header:
                updated_rule["enabled"] = header["enabled"]

        if position:
            updated_rule["position"] = {"index": position}

        if updated_rule["action"] == "skip":
            updated_rule["action_parameters"] = {
                "phases": [
                    "http_request_firewall_managed",
                    "http_request_sbfm",
                    "http_ratelimit",
                ],
                "products": [],
                "ruleset": "current",
            }

        updated_rule["expression"] = expression

        r = requests.patch(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{custom_ruleset_id}/rules/{rule_id}", headers=self._headers, json=updated_rule, timeout=5)

        return self.error.handle(r.json(), ["success"])

    def delete_rule(self, domain_name: str, rule_name: str) -> bool:
        """Delete a rule from a specific domain

        >>> cf.delete_rule("example.com", "Bad AS")
        # Will delete the rule "Bad AS" remotely from the domain "example.com"
        """

        rule = self.get_rule(domain_name, rule_name=rule_name)
        zone_id = rule["zone_id"]
        custom_ruleset_id = rule["custom_ruleset_id"]
        rule_id = rule["id"]

        r = requests.delete(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{custom_ruleset_id}/rules/{rule_id}", headers=self._headers, timeout=5)

        return self.error.handle(r.json(), ["success"])

    def purge_rules(self, domain_name: str) -> bool:
        """Purge all rules from a specific domain

        >>> cf.purge_rules("example.com")
        # Will delete all rules remotely from the domain "example.com"
        """

        rules = self.get_rules(domain_name)["rules"]

        for rule in rules:
            self.delete_rule(domain_name, rule)

        self.active_rules = 0

        return True

    def import_rules(self, domain_name: str, actions_all: str | None = None) -> bool:
        """Import all expressions from all txt file

        * actions_all -> Set the same action for all imported rules, \
        please refer to https://developers.cloudflare.com/ruleset-engine/rules-language/actions/

        Available actions as string:
        `managed_challenge, js_challenge, challenge, block, skip, log`

        :exception Error: Cannot create more rules (5 used / 5 available depending on the current plan)

        .. note::
            If you have a better plan, please register your plan using the method :func:`set_plan(domain_name) <set_plan>`

        >>> cf.import_rules("example.com")
        # Will use the action in the header specific for every file
        >>> cf.import_rules("example.com", "block")
        # Will import all rules and use the "block" action
        """

        files = os.listdir(self.utils.directory)

        rules = self.get_rules(domain_name)["rules"]

        self.active_rules = len(rules)

        for file in files:
            if file.endswith(".txt"):
                print(f"Importing {file}...")

                if file.strip(".txt") not in rules:
                    if self.active_rules < self.max_rules:
                        if actions_all:
                            self.import_rule(domain_name, file, action=actions_all)
                        else:
                            self.import_rule(domain_name, file)
                        self.active_rules += 1
                    else:
                        raise Error(f"Cannot create more rules ({self.active_rules} used / {self.max_rules} available)\n"
                                    "\t\t\tIf you have a better plan, please register the domain plan using cf.set_plan(\"<your-domain>\")")

        return True

    import_rule = create_rule
    """Import a rule with a specific expression
    
    Alias for :func:`create_rule`
    
    >>> cf.import_rule("example.com", "Bad URL.txt", action="managed_challenge")
    # Import a rule with the expression in "Bad URL.txt", will use the action in the header if specified or force it using the action argument
    """
