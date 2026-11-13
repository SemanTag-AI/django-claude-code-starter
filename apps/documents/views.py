"""Views of the documents app."""

from django.http import HttpRequest, HttpResponse
from django.views import View


class NotWrittenYetView(View):
    """Stands in for every page until the page exists."""

    def dispatch(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        """Answer every request with 501 Not Implemented."""
        return HttpResponse("This page is not written yet.", status=501)
