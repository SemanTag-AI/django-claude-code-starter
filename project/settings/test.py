"""Settings for the test run: a database of its own and no dependence on the machine."""

from .base import *  # noqa: F403

DEBUG = False
SECRET_KEY = "test-run-only-not-a-secret"  # noqa: S105
ALLOWED_HOSTS = ["testserver"]
# A file, not memory: the browser scenarios run the site in a second thread, and both
# threads have to see the same tables.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        "TEST": {"NAME": BASE_DIR / ".test.sqlite3"},  # noqa: F405
    },
}
# The slow default hasher protects real passwords. A test has none.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
