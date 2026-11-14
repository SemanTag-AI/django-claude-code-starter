"""Step definitions for theme.feature. They run in a real browser."""

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, scenarios, then, when

pytestmark = [pytest.mark.e2e, pytest.mark.usefixtures("running_site")]

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


@then("the theme switch says that the dark mode is on")
def switch_says_dark(page: Page) -> None:
    """One name that does not change, and a pressed state that does: that is what a screen reader announces."""
    expect(page.get_by_role("button", name="Dark mode", pressed=True)).to_be_visible()


@given("a visitor whose browser runs no scripts and whose system prefers the dark theme", target_fixture="plain_dark")
def plain_dark(browser, site):
    context = browser.new_context(java_script_enabled=False, color_scheme="dark")
    yield context.new_page()
    context.close()


@when("that visitor opens the sign-in page")
def plain_dark_opens(plain_dark: Page, site) -> None:
    plain_dark.goto(site.address("login"))


@then("that page is shown in the dark theme")
def plain_dark_shown(plain_dark: Page) -> None:
    expect(plain_dark.locator("body")).to_have_css("background-color", BACKGROUND["dark"])
