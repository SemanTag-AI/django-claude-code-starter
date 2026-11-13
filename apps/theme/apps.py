"""The theme app: the base template and the Tailwind source."""

from django.apps import AppConfig


class ThemeConfig(AppConfig):
    """Holds what every page shares."""

    name = "apps.theme"
