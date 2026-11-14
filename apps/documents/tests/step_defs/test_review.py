"""Step definitions for review.feature."""

from django.db import IntegrityError, transaction
from django.test import Client
from django.urls import reverse
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


def write_straight_into_the_register(context: dict, title: str, **values: object) -> None:
    """Go around the pages and the rules, the way a bug or a script would."""
    try:
        with transaction.atomic():
            Document.objects.filter(title=title).update(status=Status.APPROVED, reviewed_at=timezone.now(), **values)
    except IntegrityError as refusal:
        context["refusal"] = refusal


@when(parsers.parse('a review of the document "{title}" by {name} is written straight into the register'))
def review_by_submitter(context: dict, title: str, name: str) -> None:
    write_straight_into_the_register(context, title, reviewed_by=user_named(name))


@when(parsers.parse('an approval of the document "{title}" without a reviewer is written straight into the register'))
def approval_without_reviewer(context: dict, title: str) -> None:
    write_straight_into_the_register(context, title)


@then("the register refuses it")
def register_refuses(context: dict) -> None:
    assert "refusal" in context, "the register accepted what it should have refused"


@then("the answer does not repeat what he sent")
def not_repeated(context: dict) -> None:
    assert b"<script>" not in context["response"].content


@when(
    parsers.parse(
        'the status "{status}" with {name} as reviewer is written straight into the register for the document "{title}"'
    )
)
def unknown_status(context: dict, status: str, name: str, title: str) -> None:
    try:
        with transaction.atomic():
            Document.objects.filter(title=title).update(
                status=status, reviewed_by=user_named(name), reviewed_at=timezone.now()
            )
    except IntegrityError as refusal:
        context["refusal"] = refusal


@given("bob is signed in in a client that checks forged requests", target_fixture="client")
def strict_client() -> Client:
    strict = Client(enforce_csrf_checks=True)
    strict.force_login(user_named("bob"))
    return strict


@when(parsers.parse('he sends an approval of the document "{title}" without the form\'s token'))
def approval_without_token(client: Client, context: dict, title: str) -> None:
    address = reverse("documents:review", args=[document_titled(title).pk])
    context["response"] = client.post(address, {"decision": "approved"})
