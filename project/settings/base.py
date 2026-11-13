"""Settings shared by every environment. Not meant to run by themselves: pick local, test, staging or production."""

from pathlib import Path

from .env import env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env.secret_key
DEBUG = False
ALLOWED_HOSTS = env.allowed_hosts

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_tailwind_cli",
    "apps.theme",
    "apps.documents",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"
WSGI_APPLICATION = "project.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# The pages of the register need a signed-in user. The start page, the sign-in page and the health address do not.
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "documents:dashboard"
LOGOUT_REDIRECT_URL = "login"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "assets"]

# Tailwind CSS through the standalone CLI: no Node, no npm. The version is pinned
# so that a fresh clone builds the same stylesheet as the one that was tested.
TAILWIND_CLI_VERSION = "4.3.5"
TAILWIND_CLI_PATH = BASE_DIR / ".tailwind"
# The source lives outside STATICFILES_DIRS on purpose: collectstatic must not pick it up.
TAILWIND_CLI_SRC_CSS = BASE_DIR / "apps" / "theme" / "css" / "source.css"
TAILWIND_CLI_DIST_CSS = "css/tailwind.css"
