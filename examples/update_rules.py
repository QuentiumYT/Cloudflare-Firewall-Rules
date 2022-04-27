# If you want to run this script, move it one folder above (next to cf.py)

import os, dotenv

from cf_rules import Cloudflare

dotenv.load_dotenv(".env")

rule_to_update = "Handle Bad Bots"

cf = Cloudflare("expressions_main")
cf.auth(os.environ.get("EMAIL"), os.environ.get("KEY"))

# Export all rules from the main domain
s = cf.export_rules("main-domain.com")

# TODO Edit your rules before updating them back to Cloudflare

# Update your rule for all domains
for domain in cf.domains:
    s = cf.update_rule(domain.name, rule_to_update, "Bad Bots")
    print(s)
