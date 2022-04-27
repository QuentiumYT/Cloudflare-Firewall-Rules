# If you want to run this script, move it one folder above (next to cf.py)

import os, dotenv

from cf_rules import Cloudflare

dotenv.load_dotenv(".env")

cf = Cloudflare("expressions")
cf.auth(os.environ.get("EMAIL"), os.environ.get("KEY"))

# TODO Have some rules in the expressions folder

# First delete all existing rules
cf.purge_rules("main-domain.com")

# Then import all the rules from your expressions folder
cf.import_rules("main-domain.com", "block")
