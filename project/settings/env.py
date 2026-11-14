"""Everything the project reads from its environment, in one place.

Values come from environment variables with the prefix ``DJANGO_``, or from a file
``.env`` next to ``manage.py``. Nothing else in the project reads the environment, so
this class is the full list of what can be configured.
"""

import os
from pathlib import Path
from typing import Annotated

from django.core.exceptions import ImproperlyConfigured
from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

#: Ships with the code, so it is no secret. The server settings refuse to start with it.
DEVELOPMENT_SECRET_KEY = "local-development-only-not-a-secret"  # noqa: S105

_ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"

#: A list that is written as ``one,two`` in the environment.
CommaSeparated = Annotated[list[str], NoDecode]


class Env(BaseSettings):
    """Values that differ per machine. On a laptop every one of them has a usable default."""

    # DJANGO_ENV_FILE points at another file, or at nothing. The tests use it to start clean.
    model_config = SettingsConfigDict(
        env_prefix="DJANGO_", env_file=os.environ.get("DJANGO_ENV_FILE", _ENV_FILE), extra="ignore"
    )

    secret_key: str = DEVELOPMENT_SECRET_KEY
    #: Only the local settings read this. On a server debug is off and cannot be switched on.
    debug: bool = True
    allowed_hosts: CommaSeparated = ["localhost", "127.0.0.1"]
    #: Full origins such as ``https://register.example.org``, for forms posted over HTTPS.
    csrf_trusted_origins: CommaSeparated = []

    #: Off only to try the server settings on your own machine over plain HTTP.
    https: bool = True
    #: On when a proxy in front ends the HTTPS connection and passes ``X-Forwarded-Proto``.
    #: Never on without such a proxy: anybody could then send that header.
    behind_proxy: bool = False
    #: Ask browsers to put the domain, and every subdomain, on their built-in HTTPS list.
    #: Hard to undo, so off unless you mean it.
    hsts_preload: bool = False

    database_name: str = ""
    database_user: str = ""
    database_password: str = ""
    database_host: str = ""
    database_port: int = 5432

    @field_validator("allowed_hosts", "csrf_trusted_origins", mode="before")
    @classmethod
    def _split_on_commas(cls, value: object) -> object:
        """Turn ``one, two`` into ``["one", "two"]`` and leave a real list alone."""
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        return value


env = Env()


def required(name: str) -> object:
    """Return a value that a server cannot run without, or stop with the name of what is missing.

    Raises:
        ImproperlyConfigured: if the value was not given, is empty, or is the development key.
    """
    value = getattr(env, name)
    if name not in env.model_fields_set or not value or value == DEVELOPMENT_SECRET_KEY:
        variable = f"DJANGO_{name.upper()}"
        raise ImproperlyConfigured(f"Set the environment variable {variable}. These settings do not start without it.")
    return value
