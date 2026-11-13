"""Step definitions for theme.feature. They run in a real browser."""

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, scenarios, then, when

pytestmark = pytest.mark.e2e

scenarios("../features/theme.feature")

# What the browser reports as the page background per theme. A page without its
# stylesheet has neither, so these also catch a stylesheet that was not built.
BACKGROUND = {"light": "rgb(248, 250, 252)", "dark": "rgb(2, 6, 23)"}


@given(parsers.parse("a visitor whose system prefers the {scheme} theme"))
def system_prefers(page: Page, scheme: str) -> None:
    page.emulate_media(color_scheme=scheme)


@given("the visitor has used the theme switch")
@when("the visitor uses the theme switch")
def use_switch(page: Page) -> None:
    page.locator("[data-theme-toggle]").first.click()


@when("the visitor reloads the page")
def reload(page: Page) -> None:
    page.reload()


@then(parsers.parse("the page is shown in the {scheme} theme"))
def shown_in(page: Page, scheme: str) -> None:
    html = page.locator("html")
    if scheme == "dark":
        expect(html).to_have_class("dark")
    else:
        expect(html).not_to_have_class("dark")
    expect(page.locator("body")).to_have_css("background-color", BACKGROUND[scheme])


@then(parsers.parse('the theme switch offers "{label}"'))
def switch_offers(page: Page, label: str) -> None:
    switch = page.locator("[data-theme-toggle]").first
    expect(switch).to_have_text(label)
    expect(switch).to_have_attribute("aria-pressed", "true")
