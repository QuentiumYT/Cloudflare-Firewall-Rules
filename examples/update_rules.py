import os

import dotenv
from cf_rules import Cloudflare

dotenv.load_dotenv(".env")

local_rule_file = "Bad IP.txt"
# "Bad IP.txt" must exist in your expressions folder
remote_rule_name = "Not allowed IP"

cf = Cloudflare("expressions_main")
cf.auth_key(os.environ.get("EMAIL"), os.environ.get("KEY"))

# Export all rules from the main domain
s = cf.export_rules("example.com")

# TODO Edit your rules before updating them back to Cloudflare

# Update your rule for all domains
for domain in cf.domains:
    s = cf.update_rule(domain.name, local_rule_file, remote_rule_name)
    print(s)
