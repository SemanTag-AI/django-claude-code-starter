"""Step definitions for overdue.feature."""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from pytest_bdd import given, parsers, scenarios, then, when

from apps.documents.choices import Status
from apps.documents.models import Document
from apps.documents.rules import is_overdue

scenarios("../features/overdue.feature")


def document_from(context: dict, days: int, status: str) -> None:
    author = get_user_model().objects.create_user(username="author")
    context["now"] = timezone.now()
    context["document"] = Document.objects.create(
        title="Access policy",
        submitted_by=author,
        submitted_at=context["now"] - timedelta(days=days),
        status=status,
    )


@given(parsers.parse("a document that was submitted {days:d} days ago and waits for a review"))
def waiting(context: dict, days: int) -> None:
    document_from(context, days, Status.WAITING)


@given(parsers.parse("a document that was submitted {days:d} days ago and was {decision}"))
def reviewed(context: dict, days: int, decision: str) -> None:
    document_from(context, days, Status(decision))


@when("somebody looks at the register today")
def look(context: dict) -> None:
    context["overdue"] = is_overdue(context["document"], context["now"])


@then("the document is overdue")
def overdue(context: dict) -> None:
    assert context["overdue"] is True


@then("the document is not overdue")
def not_overdue(context: dict) -> None:
    assert context["overdue"] is False
