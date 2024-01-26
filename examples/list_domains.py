import os
from datetime import datetime

import dotenv
from cf_rules import Cloudflare

dotenv.load_dotenv(".env")

cf = Cloudflare("my_expressions")
cf.auth_key(os.environ.get("EMAIL"), os.environ.get("KEY"))

# Get domains

domains = cf.get_domains()

print(f"There are {domains['count']} domains available for your account:")

print(" ".join(domains["domains"]))

# Same as

domains = cf.domains

print(f"There are {len(domains)} domains available for your account:")

print(" ".join([x.name for x in domains]))



for domain in domains:
    print(f"{domain['name']} is {domain['status']}")
    created = datetime.fromisoformat(domain['created_on'].replace("Z", ""))
    print("Created on " + created.strftime("%Y-%m-%d %H:%M:%S"))
