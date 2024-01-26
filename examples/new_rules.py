import os

import dotenv
from cf_rules import Cloudflare

dotenv.load_dotenv(".env")

cf = Cloudflare("expressions")
cf.auth_key(os.environ.get("EMAIL"), os.environ.get("KEY"))

# TODO Have some rules in the expressions folder

# First delete all existing rules
cf.purge_rules("example.com")

# Then import all the rules from your expressions folder
cf.import_rules("example.com", "block")
