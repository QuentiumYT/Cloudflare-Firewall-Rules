import os

import dotenv
from cf_rules import Cloudflare, Utils

utils = Utils()

utils.write_expression("Path.txt", """(http.request.uri.path eq "/test")""")
u = utils.read_expression("Bad Bots.txt")

print(u)



dotenv.load_dotenv(".env")

cf = Cloudflare()
cf.auth_key(os.environ.get("EMAIL"), os.environ.get("KEY"))

c = cf.domains
print([x.name for x in c])

# c = cf.get_domains()
# print(c["count"])

# c = cf.get_domain("example.com")
# cf.set_plan("example.com")
# print(cf.plan, cf.rules("example.com"), cf.active_rules)

# c = cf.get_rules("example.com")
# c = cf.get_rule("example.com", rule_name="Bad Bots")
# cf.export_rules("example.com")
# cf.export_rule("example.com", rule_name="Bad Bots")

# cf.utils.change_directory("expressions2")
# cf.export_rule("example.com", rule_name="Bad IP")

# c = cf.create_rule("example.com", "Bad IP.txt", "Not allowed IP")
# c = cf.import_rule("example.com", "Bad Bots.txt", action="block")
# c = cf.update_rule("example.com", "Bad Bots.txt")
# c = cf.import_rules("example.com")
