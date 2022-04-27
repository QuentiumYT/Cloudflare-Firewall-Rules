# If you want to run this script, move it one folder above (next to cf.py)

import os, dotenv

from cf_rules import Cloudflare

dotenv.load_dotenv(".env")

rule_to_create_name = "Handle Bad Bots"
# "Bad Bots.txt" must exist in your expressions folder
rule_to_create_file = "Bad Bots"

cf = Cloudflare("expressions")
cf.auth(os.environ.get("EMAIL"), os.environ.get("KEY"))

domains = cf.domains # List of domains as objects

# Update your rule for all domains
for domain in domains:
    # WARNING If you have a better plan (pro, business or enterprise), don't forget to set your plan
    # It will increase your rules limit for the import_rule method
    cf.set_plan(domain)
    # import_rule is an alias of create_rule
    s = cf.import_rule(domain, rule_to_create_name, rule_to_create_file)
    print(s)
