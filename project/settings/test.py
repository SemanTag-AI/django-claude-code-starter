"""Settings for the test run: an in-memory database and no dependence on the machine."""

from .base import *  # noqa: F403

DEBUG = False
SECRET_KEY = "test-run-only-not-a-secret"  # noqa: S105
ALLOWED_HOSTS = ["testserver"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
# The slow default hasher protects real passwords. A test has none.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
