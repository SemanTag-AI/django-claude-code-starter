"""Step definitions for contrast.feature. They read the stylesheet source, not a browser."""

import re
from pathlib import Path

from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/contrast.feature")

SOURCE = Path(__file__).resolve().parents[2] / "css" / "source.css"
BLOCK = {"light": ":root", "dark": ".dark"}


def colours_of(theme: str) -> dict[str, str]:
    """Read the colour variables of one theme from the stylesheet source."""
    block = re.search(rf"^{re.escape(BLOCK[theme])} \{{(.*?)^\}}", SOURCE.read_text(), re.DOTALL | re.MULTILINE)
    assert block, f"no block {BLOCK[theme]} in {SOURCE.name}"
    colours = dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6});", block.group(1)))
    assert colours, f"no colours in block {BLOCK[theme]}"
    return colours


def luminance(colour: str) -> float:
    """Relative luminance as the Web Content Accessibility Guidelines define it."""

    def channel(pair: str) -> float:
        value = int(pair, 16) / 255
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = (channel(colour[i : i + 2]) for i in (1, 3, 5))
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


@given(parsers.parse("the colours of the {theme} theme"), target_fixture="colours")
def colours(theme: str) -> dict[str, str]:
    return colours_of(theme)


@when(parsers.parse('the contrast of "{text}" on "{background}" is worked out'), target_fixture="ratio")
def ratio(colours: dict[str, str], text: str, background: str) -> float:
    lighter, darker = sorted((luminance(colours[text]), luminance(colours[background])), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


@then(parsers.parse("it is at least {minimum:g} to 1"))
def at_least(ratio: float, minimum: float) -> None:
    assert ratio >= minimum, f"{ratio:.2f} to 1"
