"""Step definitions for submit.feature."""

from django.test import Client
from django.urls import reverse
from pytest_bdd import parsers, scenarios, then, when

from apps.documents.choices import Status
from apps.documents.models import Document

from .conftest import document_titled, shown, user_named

scenarios("../features/submit.feature")


def submit(client: Client, context: dict, title: str, tags: list[str]) -> None:
    form = {"title": title, "body": "What the document says.", "tags": tags}
    context["response"] = client.post(reverse("documents:new"), form, follow=True)


@when(parsers.parse('she submits a document with the title "{title}" and the tags "{tags}"'))
def submit_with_tags(client: Client, context: dict, title: str, tags: str) -> None:
    submit(client, context, title, tags.split(", "))


@when('she submits a document with the title "" and the tags "policy"')
def submit_without_title(client: Client, context: dict) -> None:
    submit(client, context, "", ["policy"])


@when(parsers.parse('she submits a document with the title "{title}" and no tags'))
def submit_without_tags(client: Client, context: dict, title: str) -> None:
    submit(client, context, title, [])


@when(parsers.parse("she submits a document with a title of {length:d} characters"))
def submit_long_title(client: Client, context: dict, length: int) -> None:
    submit(client, context, "a" * length, [])


@then(parsers.parse('the register holds a document "{title}" that waits for a review'))
def holds_waiting(context: dict, title: str) -> None:
    assert context["response"].status_code == 200
    assert document_titled(title).status == Status.WAITING


@then(parsers.parse('the document "{title}" was submitted by {name}'))
def submitted_by(title: str, name: str) -> None:
    assert document_titled(title).submitted_by == user_named(name)


@then(parsers.parse('the document "{title}" carries the tags "{tags}"'))
def carries_tags(title: str, tags: str) -> None:
    assert document_titled(title).tags == tags.split(", ")


@then("the register holds no documents")
def holds_nothing() -> None:
    assert Document.objects.count() == 0


@then("the form says the title is required")
def title_required(context: dict) -> None:
    assert context["response"].status_code == 200
    assert "This field is required." in shown(context["response"], "field-error")


@then(parsers.parse('the form says "{value}" is not a valid choice'))
def not_a_valid_choice(context: dict, value: str) -> None:
    assert context["response"].status_code == 200
    assert any(value in error and "not a valid choice" in error for error in shown(context["response"], "field-error"))


@then("the form says the title is too long")
def title_too_long(context: dict) -> None:
    assert context["response"].status_code == 200
    assert any("at most 200 characters" in error for error in shown(context["response"], "field-error"))


@then(parsers.parse('the page shows the title "{title}" as plain text'))
def title_as_text(context: dict, title: str) -> None:
    body = context["response"].content.decode()
    assert context["response"].status_code == 200
    assert title in shown(context["response"], "document-title")
    assert title not in body
