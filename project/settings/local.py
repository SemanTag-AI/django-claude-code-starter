"""Settings for development on your own machine."""

from .base import *  # noqa: F403
from .env import env, required

DEBUG = env.debug

if not DEBUG:
    # Debug off is a step towards a server. The key that ships with the code stops here.
    SECRET_KEY = required("secret_key")
