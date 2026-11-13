"""Step definitions for navigation.feature. They run in a real browser."""

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, scenarios, then, when

pytestmark = pytest.mark.e2e

scenarios("../features/navigation.feature")

PHONE = {"width": 390, "height": 844}


@given(parsers.parse("{name:w} is signed in in the browser"))
def signed_in(site, name: str) -> None:
    site.open("login")
    site.sign_in(name)


@given(parsers.parse("{name:w} is signed in in the browser on a phone"))
def signed_in_on_a_phone(site, page: Page, name: str) -> None:
    page.set_viewport_size(PHONE)
    signed_in(site, name)


@given(parsers.parse('he has opened the document "{title}" from the dashboard'))
def open_document(page: Page, title: str) -> None:
    page.get_by_role("link", name=title).first.click()


@when(parsers.parse('he follows "{link}" in the menu'))
def follow(page: Page, link: str) -> None:
    page.get_by_role("navigation", name="Main").get_by_role("link", name=link, exact=True).click()


@when(parsers.parse('he presses "{button}"'))
def press(page: Page, button: str) -> None:
    page.get_by_role("button", name=button, exact=True).first.click()


@when("he looks at the dashboard")
def look(page: Page) -> None:
    expect(page.get_by_role("heading", level=1, name="Dashboard")).to_be_visible()


@then(parsers.parse('the page with the heading "{heading}" is open'))
def heading_is(page: Page, heading: str) -> None:
    expect(page.get_by_role("heading", level=1, name=heading, exact=True)).to_be_visible()


@then(parsers.parse("the menu shows that {name:w} is signed in"))
def signed_in_as(page: Page, name: str) -> None:
    expect(page.locator('[data-test="signed-in-as"]')).to_have_text(name)


@then(parsers.parse('the menu marks "{link}" as the current page'))
def current_page(page: Page, link: str) -> None:
    current = page.get_by_role("navigation", name="Main").locator('[aria-current="page"]')
    expect(current).to_have_text(link)


@then(parsers.parse('the page says "{text}"'))
def page_says(page: Page, text: str) -> None:
    expect(page.locator('[data-test="message"]')).to_have_text(text)


@then("the page offers no review any more")
def no_review(page: Page) -> None:
    expect(page.locator('[data-test="review-form"]')).to_have_count(0)


@then("the sign-in page is open")
def sign_in_page(page: Page) -> None:
    expect(page.get_by_role("button", name="Sign in")).to_be_visible()


@then("the menu is out of view")
def menu_hidden(page: Page) -> None:
    expect(page.locator("[data-sidebar]")).not_to_be_in_viewport()


@then("the menu is in view")
def menu_shown(page: Page) -> None:
    expect(page.locator("[data-sidebar]")).to_be_in_viewport()
