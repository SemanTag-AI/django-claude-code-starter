"""Everything the project reads from its environment, in one place.

Settings come from environment variables with the prefix ``DJANGO_``, or from a
``.env`` file next to ``manage.py``. Nothing else in the project reads the
environment directly, so this class is the full list of what can be configured.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    """Values that differ per machine. Every field has a default that is safe locally."""

    model_config = SettingsConfigDict(env_prefix="DJANGO_", env_file=".env", extra="ignore")

    #: Replace this before the project faces a network. The default only works with debug on.
    secret_key: str = "local-development-only-not-a-secret"  # noqa: S105
    debug: bool = False
    allowed_hosts: list[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1"])


env = Env()
