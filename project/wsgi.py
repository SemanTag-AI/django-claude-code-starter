"""WSGI entry point."""

import os

from django.core.wsgi import get_wsgi_application

# A server that forgets to choose gets the settings that refuse to start half configured,
# not the ones with debug on.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.production")

application = get_wsgi_application()
