"""Settings for a rehearsal server: the production settings, with a shorter HTTPS promise.

A rehearsal address comes and goes. Telling browsers to insist on HTTPS for a year, for every
subdomain, or offering the address for their preload list, would outlive it. An hour is enough.
"""

from .production import *  # noqa: F403

if SECURE_HSTS_SECONDS:  # noqa: F405
    SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_PRELOAD = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# A rehearsal address should not bind its parent domain either. The deployment check asks
# for both; leaving them off is the point here.
SILENCED_SYSTEM_CHECKS = ["security.W005", "security.W021"]
