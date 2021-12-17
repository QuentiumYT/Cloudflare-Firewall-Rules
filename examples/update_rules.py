# If you want to run this script, move it one folder above (next to cf.py)

import os, dotenv

from cf import Cloudflare

dotenv.load_dotenv(".env")

rule_to_update = "Handle Bad Bots"

cf = Cloudflare(os.environ.get("EMAIL"), os.environ.get("KEY"), "expressions_main")

# Export all rules from the main domain
s = cf.export_rules("main-domain.com")

# TODO Edit your rules before updating them back to Cloudflare

domains = cf.domains["domains"]

# Update your rule for all domains
for domain in domains:
    s = cf.update_rule(domain, rule_to_update, "Bad Bots")
    print(s)
