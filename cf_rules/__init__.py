__title__ = "cf_rules"
__description__ = "A Cloudflare wrapper to bulk add / edit your firewall rules using Cloudflare's API."
__url__ = "https://quentiumyt.github.io/Cloudflare-Firewall-Rules/"
__version__ = "1.2.2"

__author__ = "Quentin Lienhardt"
__author_email__ = "pro@quentium.fr"
__license__ = "Apache 2.0"
__copyright__ = "Copyright 2022 Quentin Lienhardt"

__all__ = (
    "Cloudflare",
    "Utils",
    "Error",
)

from cf_rules.cf import Cloudflare
from cf_rules.utils import Utils, Error
