"""Steps and fixtures that every feature of the documents app shares."""

import html
import re
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from pytest_bdd import given, parsers, then, when

from apps.documents.choices import Status
from apps.documents.models import Document

PASSWORD = "a-password-for-the-test-run"

PAGES = {
    "the start page": "documents:home",
    "the dashboard": "documents:dashboard",
    "the list of documents": "documents:list",
    "the form for a new document": "documents:new",
    "the sign-in page": "login",
    "the health address": "health",
}


@pytest.fixture(autouse=True)
def _database(db):
    """Every scenario in this app reads or writes the register."""


@pytest.fixture
def context() -> dict:
    """What one scenario remembers between its steps."""
    return {}


def user_named(name: str):
    return get_user_model().objects.get(username=name)


def document_titled(title: str) -> Document:
    return Document.objects.get(title=title)


def address_of(page: str) -> str:
    """Translate the name a scenario uses for a page into its address."""
    if match := re.fullmatch(r'the document "(.+)"', page):
        return reverse("documents:detail", args=[document_titled(match.group(1)).pk])
    return reverse(PAGES[page])


def shown(response, test_id: str) -> list[str]:
    """Return the text of every element on the page that carries this data-test value."""
    found = re.findall(rf'data-test="{re.escape(test_id)}"[^>]*>([^<]*)<', response.content.decode())
    return [html.unescape(text).strip() for text in found]


def make_document(title: str, submitter: str, days_ago: int = 0, status: str = Status.WAITING) -> Document:
    submitted_at = timezone.now() - timedelta(days=days_ago)
    reviewed = status != Status.WAITING
    reviewer = get_user_model().objects.exclude(username=submitter).first() if reviewed else None
    return Document.objects.create(
        title=title,
        submitted_by=user_named(submitter),
        submitted_at=submitted_at,
        status=status,
        reviewed_by=reviewer,
        reviewed_at=submitted_at + timedelta(days=1) if reviewed else None,
    )


@given(parsers.re(r"the users? (?P<names>[a-z]+(?: and [a-z]+)*)"))
def users(names: str) -> None:
    for name in names.split(" and "):
        get_user_model().objects.create_user(username=name, password=PASSWORD)


@given(parsers.parse('a document "{title}" that {submitter} submitted and that waits for a review'))
def waiting_document(title: str, submitter: str) -> None:
    make_document(title, submitter)


@given(parsers.parse("{name} is signed in"))
def signed_in(client: Client, name: str) -> None:
    client.force_login(user_named(name))


@when(parsers.re(r"(?:he|she|a visitor) opens (?P<page>.+)"))
def open_page(client: Client, context: dict, page: str) -> None:
    if page == "a document that does not exist":
        address = reverse("documents:detail", args=[999_999])
    else:
        address = address_of(page)
    context["response"] = client.get(address)


@when(parsers.re(r'(?:he|she|a visitor) sends an? (?P<decision>approval|rejection) of the document "(?P<title>.+)"'))
def send_review(client: Client, context: dict, decision: str, title: str) -> None:
    value = {"approval": Status.APPROVED, "rejection": Status.REJECTED}[decision]
    send_decision(client, context, value, title)


def send_decision(client: Client, context: dict, decision: str, title: str) -> None:
    address = reverse("documents:review", args=[document_titled(title).pk])
    context["response"] = client.post(address, {"decision": decision}, follow=True)


@then("the page opens")
def page_opens(context: dict) -> None:
    assert context["response"].status_code == 200


@then("the visitor is sent to the sign-in page")
def sent_to_sign_in(context: dict) -> None:
    response = context["response"]
    target = response.redirect_chain[-1][0] if getattr(response, "redirect_chain", None) else response.url
    assert target.startswith(reverse("login"))


@then(parsers.parse('the document "{title}" still waits for a review'))
def still_waiting(title: str) -> None:
    document = document_titled(title)
    assert document.status == Status.WAITING
    assert document.reviewed_by is None
