"""Step definitions for review.feature."""

from django.test import Client
from django.utils import timezone
from pytest_bdd import given, parsers, scenarios, then, when

from apps.documents.choices import Status
from apps.documents.models import Document

from .conftest import document_titled, send_decision, shown, user_named

scenarios("../features/review.feature")


@given(parsers.parse('{name} has approved the document "{title}"'))
def already_approved(name: str, title: str) -> None:
    Document.objects.filter(title=title).update(
        status=Status.APPROVED, reviewed_by=user_named(name), reviewed_at=timezone.now()
    )


@when(parsers.re(r'(?:he|she) sends the decision "(?P<decision>.+)" for the document "(?P<title>.+)"'))
def send_other_decision(client: Client, context: dict, decision: str, title: str) -> None:
    send_decision(client, context, decision, title)


@then("the page offers no review")
def no_review(context: dict) -> None:
    assert context["response"].status_code == 200
    assert 'data-test="review-form"' not in context["response"].content.decode()


@then("the page offers a review")
def a_review(context: dict) -> None:
    assert context["response"].status_code == 200
    assert 'data-test="review-form"' in context["response"].content.decode()


@then("the request is refused")
def refused(context: dict) -> None:
    assert context["response"].status_code == 403


@then("the request is not accepted")
def not_accepted(context: dict) -> None:
    assert context["response"].status_code == 400


@then(parsers.re(r'the document "(?P<title>.+)" is (?P<status>approved|rejected) by (?P<name>[a-z]+)'))
def reviewed_by(title: str, status: str, name: str) -> None:
    document = document_titled(title)
    assert document.status == status
    assert document.reviewed_by == user_named(name)
    assert document.reviewed_at is not None


@then("the page says the document was already reviewed")
def already_reviewed(context: dict) -> None:
    assert context["response"].status_code == 200
    assert any("already reviewed" in message for message in shown(context["response"], "message"))
