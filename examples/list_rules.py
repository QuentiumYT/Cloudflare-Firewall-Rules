import os
from datetime import datetime

import dotenv
from cf_rules import Cloudflare

dotenv.load_dotenv(".env")

cf = Cloudflare("my_expressions")
cf.auth_key(os.environ.get("EMAIL"), os.environ.get("KEY"))

# Get rules

rules = cf.get_rules("example.com")

print(f"There are {rules['count']} rules available for your account:")

print(" ".join([x["description"] for x in rules["result"]]))

# Same as

rules = cf.rules("example.com")

print(f"There are {len(rules)} rules available for your account:")

print(" ".join([x.description for x in rules]))



for rule in rules:
    print(f"{rule['description']} is {'active' if rule['enabled'] else 'inactive'}")
    updated = datetime.fromisoformat(rule['last_updated'].replace("Z", ""))
    print("Created on " + updated.strftime("%Y-%m-%d %H:%M:%S"))
