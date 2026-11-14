"""Settings for a server. They refuse to start until every secret and address is given.

Checked with the framework's deployment check and run in the container of this
repository. They have not run behind a real proxy with HTTPS: read them before you rely on them.
"""

from .base import *  # noqa: F403
from .env import env, required

DEBUG = False

SECRET_KEY = required("secret_key")
ALLOWED_HOSTS = required("allowed_hosts")
CSRF_TRUSTED_ORIGINS = env.csrf_trusted_origins

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": required("database_name"),
        "USER": required("database_user"),
        "PASSWORD": required("database_password"),
        "HOST": required("database_host"),
        "PORT": env.database_port,
        # Keep a connection for a minute instead of opening one per request.
        "CONN_MAX_AGE": 60,
    },
}

# Static files are collected once, when the image is made, and served by the application
# itself with far-future caching. No separate file server is needed. The middleware has to
# come right after the security middleware, which is the first one in the base settings.
MIDDLEWARE = [MIDDLEWARE[0], "whitenoise.middleware.WhiteNoiseMiddleware", *MIDDLEWARE[1:]]  # noqa: F405
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# HTTPS everywhere, and browsers remember it for a year. DJANGO_HTTPS=false switches all of
# this off at once, to try the image on your own machine. The health address is exempt from
# the redirect, because the check that calls it comes from inside over plain HTTP.
SECURE_SSL_REDIRECT = env.https
SECURE_REDIRECT_EXEMPT = [r"^healthz/$"]
SESSION_COOKIE_SECURE = env.https
CSRF_COOKIE_SECURE = env.https
SECURE_HSTS_SECONDS = 365 * 24 * 3600 if env.https else 0
# Subdomains are covered too, as the deployment check asks. The browsers' preload list is a
# promise that takes months to withdraw, so it is opt-in through DJANGO_HSTS_PRELOAD.
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.https
SECURE_HSTS_PRELOAD = env.https and env.hsts_preload
if not SECURE_HSTS_PRELOAD:
    # The deployment check asks for preload. Leaving it off is a choice, see above.
    SILENCED_SYSTEM_CHECKS = ["security.W021"]
if env.behind_proxy:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# A container writes to its standard output and something else collects it.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
