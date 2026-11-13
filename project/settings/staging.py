"""Settings for a rehearsal server: the production settings, with one difference.

A rehearsal address comes and goes. Telling browsers to insist on HTTPS for a year, and
offering the address for the preload list of browsers, would outlive it. An hour is enough.
"""

from .production import *  # noqa: F403

if SECURE_HSTS_SECONDS:  # noqa: F405
    SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_PRELOAD = False
# The deployment check asks for preload. On a rehearsal server leaving it off is the point.
SILENCED_SYSTEM_CHECKS = ["security.W021"]
