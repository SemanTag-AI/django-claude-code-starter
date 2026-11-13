"""Step definitions for access.feature."""

from django.test import Client
from django.urls import reverse
from pytest_bdd import parsers, scenarios, then, when

from .conftest import PASSWORD, shown

scenarios("../features/access.feature")


@when(parsers.parse("{name} signs in with the right password"))
def sign_in(client: Client, context: dict, name: str) -> None:
    context["response"] = client.post(reverse("login"), {"username": name, "password": PASSWORD}, follow=True)


@when(parsers.parse("{name} signs in with a wrong password"))
def sign_in_wrong(client: Client, context: dict, name: str) -> None:
    context["response"] = client.post(reverse("login"), {"username": name, "password": "not-the-password"})


@when("he signs out")
def sign_out(client: Client, context: dict) -> None:
    context["response"] = client.post(reverse("logout"))


@then("the sign-in page says the name and password do not match")
def no_match(context: dict) -> None:
    assert context["response"].status_code == 200
    assert any("correct username and password" in error for error in shown(context["response"], "form-error"))


@then("the page is not found")
def not_found(context: dict) -> None:
    assert context["response"].status_code == 404
