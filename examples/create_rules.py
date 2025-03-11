import os

import dotenv
from cf_rules import Cloudflare

dotenv.load_dotenv(".env")

local_rule_file = "Bad Bots.txt"
# "Bad Bots.txt" must exist in your expressions folder
remote_rule_name = "Handle Bad Bots"

cf = Cloudflare("expressions")
cf.auth_key(os.environ.get("EMAIL"), os.environ.get("KEY"))

domains = cf.domains # List of domains as objects

# Update your rule for all domains
for domain in domains:
    # WARNING If you have a better plan (pro, business or enterprise), don't forget to set your plan
    # It will increase your rules limit for the import_rule method
    cf.set_plan(domain.name)
    # import_rule is an alias of create_rule
    c = cf.import_rule(domain, local_rule_file, remote_rule_name, "block")
    print(c)
