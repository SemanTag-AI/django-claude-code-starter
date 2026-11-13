"""Step definitions for access.feature."""

import html
import re

from django.test import Client
from django.urls import reverse
from pytest_bdd import given, parsers, scenarios, then, when

from .conftest import PAGES, PASSWORD, shown, user_named

scenarios("../features/access.feature")


@when(parsers.parse("{name} signs in with the right password"))
def sign_in(client: Client, context: dict, name: str) -> None:
    context["response"] = client.post(reverse("login"), {"username": name, "password": PASSWORD}, follow=True)


@when(parsers.parse("{name} signs in with a wrong password"))
def sign_in_wrong(client: Client, context: dict, name: str) -> None:
    context["response"] = client.post(reverse("login"), {"username": name, "password": "not-the-password"})


@given(parsers.parse("{name} was signed in and has signed out"))
def signed_out(client: Client, name: str) -> None:
    client.force_login(user_named(name))
    assert client.post(reverse("logout")).status_code == 302


@then("the sign-in page says the name and password do not match")
def no_match(context: dict) -> None:
    assert context["response"].status_code == 200
    assert any("correct username and password" in error for error in shown(context["response"], "form-error"))


@then("the page is not found")
def not_found(context: dict) -> None:
    assert context["response"].status_code == 404


@then("the page shows no leftover template code")
def no_template_code(context: dict) -> None:
    body = context["response"].content.decode()
    for leftover in ("{#", "#}", "{%", "%}", "{{", "}}"):
        assert leftover not in body, leftover


@given("a visitor who has opened the start page")
def opened_start_page(client: Client, context: dict) -> None:
    context["response"] = client.get(reverse("documents:home"))


@given("a visitor who was sent to the sign-in page from the list of documents")
def sent_from_the_list(client: Client, context: dict) -> None:
    context["response"] = client.get(reverse("documents:list"), follow=True)


@when(parsers.parse("{name} signs in with the form on that page"))
def sign_in_with_the_form(client: Client, context: dict, name: str) -> None:
    """Send what the form on the page would send: to its own address, with its own hidden fields."""
    body = context["response"].content.decode()
    form = re.search(r'<form[^>]*data-test="sign-in-form"[^>]*>(.*?)</form>', body, re.DOTALL)
    assert form, "the page has no sign-in form"
    action = re.search(r'action="([^"]*)"', form.group(0)).group(1)
    following = re.search(r'name="next" value="([^"]*)"', form.group(1)).group(1)
    fields = {"username": name, "password": PASSWORD, "next": html.unescape(following)}
    context["response"] = client.post(html.unescape(action), fields, follow=True)


@then(parsers.parse("he is sent to {page}"))
def sent_to(context: dict, page: str) -> None:
    response = context["response"]
    target = response.redirect_chain[-1][0] if getattr(response, "redirect_chain", None) else response.url
    assert target == reverse(PAGES[page])


@then("the page says what the register is for")
def says_purpose(context: dict) -> None:
    assert any(len(text) > 20 for text in shown(context["response"], "purpose"))


@then("the page offers the sign-in")
def offers_sign_in(context: dict) -> None:
    assert 'data-test="sign-in-form"' in context["response"].content.decode()


@then(parsers.parse('the title of the page is "{title}"'))
def title_is(context: dict, title: str) -> None:
    found = re.search(r"<title>([^<]*)</title>", context["response"].content.decode())
    assert found and html.unescape(found.group(1)).strip() == title
