"""Fixtures and steps for the scenarios that drive a real browser."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from playwright.sync_api import Page
from pytest_bdd import given, parsers, when

from apps.documents.models import Document

PASSWORD = "a-password-for-the-test-run"


@pytest.fixture(scope="session", autouse=True)
def _async_unsafe():
    """Let the framework do database work while the browser library's event loop runs.

    The browser library runs an event loop in the test thread, and the framework then refuses
    database work there unless told otherwise. The test database is created at session level,
    after the browser has started, so the flag has to be set for the session. It is autouse in
    this folder only: `mise run test` deselects these scenarios and never sets it.
    """
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
        yield


@pytest.fixture
def running_site(transactional_db, live_server):
    """Start the site and empty the database afterwards. Only the browser scenarios ask for this."""


@pytest.fixture
def site(live_server, page: Page):
    """Give a step the address of the running site and the browser page in one go."""

    class Site:
        def address(self, name: str, *args: object) -> str:
            return live_server.url + reverse(name, args=args)

        def open(self, name: str, *args: object) -> None:
            page.goto(self.address(name, *args))

        def sign_in(self, name: str) -> None:
            page.get_by_label("Name").fill(name)
            page.get_by_label("Password").fill(PASSWORD)
            page.get_by_role("button", name="Sign in").click()
            # Wait for the next page and its stylesheet. A step that starts earlier can meet a
            # page whose closed menu is not yet hidden, which made a keyboard scenario flaky.
            page.wait_for_url(lambda url: "/login/" not in url)
            page.wait_for_load_state("load")

    return Site()


@given(parsers.parse("the user {name:w}"))
def user(name: str) -> None:
    get_user_model().objects.create_user(username=name, password=PASSWORD)


@given(parsers.parse('the user {name:w}, who submitted the document "{title}"'))
def user_with_document(name: str, title: str) -> None:
    author = get_user_model().objects.create_user(username=name, password=PASSWORD)
    Document.objects.create(title=title, submitted_by=author)


@given("the visitor has opened the sign-in page")
@given("a visitor who has opened the sign-in page")
@when("the visitor opens the sign-in page")
def open_sign_in(site) -> None:
    site.open("login")


@when(parsers.parse("the visitor signs in as {name:w}"))
def sign_in(site, name: str) -> None:
    site.sign_in(name)


@given("a visitor who has opened the start page")
def open_start_page(site) -> None:
    site.open("documents:home")


@pytest.fixture
def plain_page(browser, live_server):
    """A phone-sized page in a browser that runs no script at all."""
    context = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
    yield context.new_page()
    context.close()
