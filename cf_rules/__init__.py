from pkg_resources import get_distribution

__version__ = get_distribution("cf_rules").version

__all__ = (
    "Cloudflare",
    "Utils",
    "Error",
)

from cf_rules.cf import Cloudflare
from cf_rules.utils import Utils, Error
