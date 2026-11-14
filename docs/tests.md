# Tests

Every behaviour starts as a scenario in plain English. A scenario lives in a `.feature` file;
its step definitions turn each sentence into Python. [pytest-bdd](https://pytest-bdd.readthedocs.io/)
connects the two, and pytest runs them.

```text
apps/documents/tests/
  features/            what the register does: access, review, overdue, submit, dashboard
  step_defs/           one test_<name>.py per feature file, plus conftest.py with shared steps
apps/theme/tests/
  features/            contrast.feature: every text colour is readable in both themes
project/tests/
  features/            deployment.feature: the server settings refuse to start half configured
tests/e2e/
  features/            navigation.feature, theme.feature: scenarios in a real browser
  step_defs/           conftest.py starts the site and gives each scenario a fresh database
```

| Command | Runs | How long |
|---|---|---|
| `mise run test` | The 103 scenarios that need no browser | A few seconds |
| `mise run test:e2e` | The 24 scenarios marked `e2e`, in Chromium | About ten seconds, plus the download of Chromium the first time |

## One feature, start to finish

[`overdue.feature`](../apps/documents/tests/features/overdue.feature) pins down one rule, with an
example on each side of the limit:

```gherkin
Feature: Documents that wait too long for a review are overdue
  As somebody who is responsible for the register
  I want to see which documents have waited more than 30 days for a review
  So that no document stays unreviewed without anybody noticing

  The rule is "more than 30 full days", not "30 days or more". The second
  example pins that down, because it is the question people answer differently.
  The third pins down "full": 30 days and 23 hours is still day 30.

  Scenario Outline: A waiting document becomes overdue after 30 full days
    Given a document that was submitted <age> ago and waits for a review
    When somebody looks at the register today
    Then the document is <state>

    Examples:
      | age                  | state       |
      | 29 days              | not overdue |
      | 30 days              | not overdue |
      | 30 days and 23 hours | not overdue |
      | 31 days              | overdue     |
      | 0 days               | not overdue |

  Scenario Outline: A document that was reviewed is never overdue
    Given a document that was submitted 90 days ago and was <decision>
    When somebody looks at the register today
    Then the document is not overdue

    Examples:
      | decision |
      | approved |
      | rejected |
```

[`test_overdue.py`](../apps/documents/tests/step_defs/test_overdue.py) gives every sentence its
meaning. `scenarios(...)` turns each scenario, and each row of an `Examples` table, into a test:

```python
"""Step definitions for overdue.feature."""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from pytest_bdd import given, parsers, scenarios, then, when

from apps.documents.choices import Status
from apps.documents.models import Document
from apps.documents.rules import is_overdue

scenarios("../features/overdue.feature")


def document_from(context: dict, age: timedelta, status: str) -> None:
    users = get_user_model().objects
    author = users.create_user(username="author")
    reviewed = status != Status.WAITING
    context["now"] = timezone.now()
    context["document"] = Document.objects.create(
        title="Access policy",
        submitted_by=author,
        submitted_at=context["now"] - age,
        status=status,
        reviewed_by=users.create_user(username="reviewer") if reviewed else None,
        reviewed_at=context["now"] if reviewed else None,
    )


@given(
    parsers.re(
        r"a document that was submitted (?P<days>\d+) days(?: and (?P<hours>\d+) hours)? ago and waits for a review"
    )
)
def waiting(context: dict, days: str, hours: str | None) -> None:
    document_from(context, timedelta(days=int(days), hours=int(hours or 0)), Status.WAITING)


@given(parsers.parse("a document that was submitted {days:d} days ago and was {decision}"))
def reviewed(context: dict, days: int, decision: str) -> None:
    document_from(context, timedelta(days=days), Status(decision))


@when("somebody looks at the register today")
def look(context: dict) -> None:
    context["overdue"] = is_overdue(context["document"], context["now"])


@then("the document is overdue")
def overdue(context: dict) -> None:
    assert context["overdue"] is True


@then("the document is not overdue")
def not_overdue(context: dict) -> None:
    assert context["overdue"] is False
```

## One scenario in a browser

From [`theme.feature`](../tests/e2e/features/theme.feature). The steps in
[`test_theme.py`](../tests/e2e/step_defs/test_theme.py) drive Chromium with
[Playwright](https://playwright.dev/python/), and check the colour the browser actually paints,
so a page without its stylesheet fails too:

```gherkin
  Scenario: The switch changes the theme
    Given a visitor whose system prefers the light theme
    And the visitor has opened the sign-in page
    When the visitor uses the theme switch
    Then the page is shown in the dark theme
    And the theme switch says that the dark mode is on
```

## How pytest is set up

All of it is in [`pyproject.toml`](../pyproject.toml), under `[tool.pytest.ini_options]`:

| Setting | What it does |
|---|---|
| `DJANGO_SETTINGS_MODULE = "project.settings.test"` | The test settings: a database in memory, a fast password hasher, no `.env` needed |
| `testpaths = ["apps", "project", "tests"]` | Where pytest looks |
| `addopts = "-ra -m 'not e2e'"` | Leaves the browser scenarios out of `mise run test`, and lists anything skipped at the end |
| `markers = ["e2e: ..."]` | The marker that `mise run test:e2e` selects with `-m e2e` |

## Run part of it

```bash
uv run pytest apps/documents/tests/step_defs/test_overdue.py      # one feature
uv run pytest -k "full_days"                                       # scenarios whose name matches
uv run pytest -m e2e tests/e2e/step_defs/test_theme.py --headed    # watch the browser do it
```

The project instructions ask agents to use the two `mise` commands only, so that every run is
the same. These are for you, while you look around.
