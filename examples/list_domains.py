# If you want to run this script, move it one folder above (next to cf.py)

import os, dotenv
from datetime import datetime

from cf import Cloudflare

dotenv.load_dotenv(".env")

cf = Cloudflare(os.environ.get("EMAIL"), os.environ.get("KEY"), "expressions_main")

domains = cf.domains

print(f"There are {domains['count']} domains available for your account.")

print(" ".join(domains["domains"]))

for domain in domains["result"]:
    print(f"{domain['name']} is {domain['status']}")
    created = datetime.fromisoformat(domain['created_on'].replace("Z", ""))
    print("Created on " + created.strftime("%Y-%m-%d %H:%M:%S"))
