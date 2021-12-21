# If you want to run this script, move it one folder above (next to cf.py)

import os, dotenv

from cf import Cloudflare, Utils

utils = Utils()

# u = utils.write_expression("+test", """(http.request.uri.path eq "/test")""")
# u = utils.read_expression("Bad Bots")

# print(u)



dotenv.load_dotenv(".env")

cf = Cloudflare()
cf.auth(os.environ.get("EMAIL"), os.environ.get("KEY"))

# c = cf.domains # OR c = cf.get_domains()
# print(c)

# c = cf.get_domain("test.fr")
# cf.set_plan("test.fr")
# print(cf.plan, cf.rules, cf.active_rules)

# c = cf.get_rules("test.fr")
# c = cf.get_rule("test.fr", "Bad Bots")
# cf.export_rules("test.fr")
# cf.export_rule("test.fr", "Bad Bots")

# cf.utils.change_directory("expressions2")
# cf.export_rule("test.fr", "Test/1")

# c = cf.create_rule("test.fr", "Test/1", "+test", action="js_challenge")
# c = cf.import_rule("test.fr", "Bots", "Bad Bots")
# c = cf.update_rule("test.fr", "Bad Bots", "Bad Bots")
# c = cf.import_rules("test.fr")
