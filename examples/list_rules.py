# If you want to run this script, move it one folder above (next to cf.py)

import os, dotenv
from datetime import datetime

from cf_rules import Cloudflare

dotenv.load_dotenv(".env")

cf = Cloudflare("my_expressions")
cf.auth(os.environ.get("EMAIL"), os.environ.get("KEY"))

# Get rules

rules = cf.get_rules("ultraperformance.fr")

print(f"There are {rules['count']} rules available for your account:")

print(" ".join([x["description"] for x in rules["result"]]))

# Same as

rules = cf.rules("ultraperformance.fr")

print(f"There are {len(rules)} domains available for your account:")

print(" ".join([x.description for x in rules]))



for rule in rules:
    print(f"{rule['description']} is {'paused' if rule['paused'] else 'active'}")
    created = datetime.fromisoformat(rule['created_on'].replace("Z", ""))
    print("Created on " + created.strftime("%Y-%m-%d %H:%M:%S"))
