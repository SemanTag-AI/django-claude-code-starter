# Django Claude Code starter

A small Django and Tailwind application in which Claude Code agents work behaviour first:
a specification a person approves, then failing tests, then code, then a review
by an agent that did not write the code. A person merges.

It is a starting point for your own project and a working example of the method.
Clone it, run one command, and watch a feature go from a sentence to tested code.

If it helps you, give it a star. That is how other teams find it, and how we see what is worth working out further.

Made by [Semantag AI](https://semantag.ai/en/?utm_source=github&utm_medium=readme&utm_campaign=django-claude-code-starter). It is not a product of Anthropic and is not endorsed by
Anthropic. Claude and Claude Code are trademarks of Anthropic.

## What is in the box

| Part | Where | What it does |
|---|---|---|
| Five agents | `.claude/agents/` | `spec-writer`, `test-writer`, `implementer`, `reviewer`, `security-reviewer`. One role each, and no more tools than the role needs. A minimal set, meant to be extended: see [Add the agents you need](#add-the-agents-you-need) |
| One command | `.claude/commands/feature.md` | `/feature <request>` runs the agents in order and stops for your approval after the specification |
| One skill | `.claude/skills/bdd-scenarios/` | How to write scenarios that pin a rule down |
| Project instructions | `CLAUDE.md` | The commands, the layout and the rules. The agents name no tool themselves: they read this file |
| An application | `project/`, `apps/` | A document register with a start page, a sign-in, a dashboard and a light and a dark mode |
| Scenarios | `apps/*/tests/`, `project/tests/`, `tests/e2e/` | 99 that need no browser, 23 that drive a real one. See [Tests](#tests) |
| Settings | `project/settings/` | `local`, `test`, `staging` and `production`. The last two refuse to start until every secret and address is given |
| A container | `Dockerfile`, `compose.yaml` | The register with PostgreSQL, to run the whole thing on your own machine |
| Gates | `.pre-commit-config.yaml`, `.github/workflows/ci.yml` | Lint, checks, both sets of scenarios, a secret scan and a start of the container, outside the agents |

## The example: a document register

Somebody submits a document with a title, a text and tags. A colleague approves or rejects it.
Two rules carry the example:

- **Whoever submitted a document does not review it.** The page hides the buttons from the
  submitter, and the server refuses the request if she sends it anyway. The second half is the
  control. The database refuses it as well, for the day the code has a bug.
  See [`review.feature`](apps/documents/tests/features/review.feature).
- **A document that has waited more than 30 full days is overdue.** On day 30 it is not, not even
  at 30 days and 23 hours. On day 31 it is. See [`overdue.feature`](apps/documents/tests/features/overdue.feature).

The rules are plain functions in [`apps/documents/rules.py`](apps/documents/rules.py).
The first two commits of this repository show the order they were made in: the specification
and the failing steps first, the rules and the pages second.

There is no file upload, no search and no processing of what a document says. It is a register.

## Start

You need [mise](https://mise.jdx.dev/) and, for the agents, [Claude Code](https://code.claude.com/docs). Node is not needed.

```bash
git clone https://github.com/SemanTag-AI/django-claude-code-starter.git
cd django-claude-code-starter
mise trust
mise run install   # dependencies and git hooks
mise run test      # 99 scenarios, all green
mise run demo      # two users and twelve documents to look around in
mise run dev       # http://127.0.0.1:8000, with the Tailwind watcher
```

The start page says what the register is for and holds the sign-in. Use `alice` or `bob` with
the password `review-me-please`. Sign in as one, submit a document, and try to approve it.
Then sign in as the other.

That password is public, which is why `mise run demo` refuses to run with debug off. Do not
put this application on a server anybody else can reach without replacing the users.

`mise run dev` downloads the Tailwind CLI once, about 110 MB, into `.tailwind/`.
`mise run test:e2e` runs the browser scenarios and downloads Chromium the first time.

## Tests

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
| `mise run test` | The 99 scenarios that need no browser | A few seconds |
| `mise run test:e2e` | The 23 scenarios marked `e2e`, in Chromium | About ten seconds, plus the download of Chromium the first time |

### One feature, start to finish

[`overdue.feature`](apps/documents/tests/features/overdue.feature) pins down one rule, with an
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

[`test_overdue.py`](apps/documents/tests/step_defs/test_overdue.py) gives every sentence its
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

### One scenario in a browser

From [`theme.feature`](tests/e2e/features/theme.feature). The steps in
[`test_theme.py`](tests/e2e/step_defs/test_theme.py) drive Chromium with
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

### How pytest is set up

All of it is in [`pyproject.toml`](pyproject.toml), under `[tool.pytest.ini_options]`:

| Setting | What it does |
|---|---|
| `DJANGO_SETTINGS_MODULE = "project.settings.test"` | The test settings: a database in memory, a fast password hasher, no `.env` needed |
| `testpaths = ["apps", "project", "tests"]` | Where pytest looks |
| `addopts = "-ra -m 'not e2e'"` | Leaves the browser scenarios out of `mise run test`, and lists anything skipped at the end |
| `markers = ["e2e: ..."]` | The marker that `mise run test:e2e` selects with `-m e2e` |

### Run part of it

```bash
uv run pytest apps/documents/tests/step_defs/test_overdue.py      # one feature
uv run pytest -k "full_days"                                       # scenarios whose name matches
uv run pytest -m e2e tests/e2e/step_defs/test_theme.py --headed    # watch the browser do it
```

The project instructions ask agents to use the two `mise` commands only, so that every run is
the same. These are for you, while you look around.

## Run it in containers

With Docker, and without installing anything else:

```bash
cp .env.example .env     # then fill in the two values; the file says how
mise run docker:up       # or: docker compose up --build --detach --wait
```

Open http://localhost:8080. This runs the `production` settings with PostgreSQL and gunicorn,
as a user without root rights, with the migrations applied before the application starts.
The demo users do not exist here, because debug is off. Make a user of your own:

```bash
docker compose exec web python manage.py createsuperuser
```

`docker compose down` stops it and keeps the data. Add `--volumes` to throw the data away.

## Settings

| File | For | Debug | Database |
|---|---|---|---|
| `local` | Your machine | On, unless `DJANGO_DEBUG=false` | SQLite |
| `test` | The test run | Off | SQLite, a file of its own |
| `staging` | A rehearsal server | Off | PostgreSQL |
| `production` | A server | Off | PostgreSQL |

`staging` is `production` with one difference: browsers are told to insist on HTTPS for an hour
instead of a year. Both stop with the name of the variable when a value is missing, and both
refuse the key that ships with the code. Everything that can be set is listed in
[`project/settings/env.py`](project/settings/env.py). `mise run check:deploy` runs the
deployment check of the framework on both.

## The pipeline

```text
you: /feature <request>
        |
  spec-writer      writes a feature file in Gherkin            may only write the spec
        |
  you approve      the cheapest moment to catch a misunderstanding
        |
  test-writer      writes step definitions and sees them fail  for the right reason
        |
  implementer      writes code until they pass                 may not touch a test
        |
  reviewer         reads the change against the spec           can read, cannot edit
  security-        reads the change as an attacker would       can read, cannot edit
  reviewer
        |
  you merge        no agent pushes to main
```

`/feature` always ends with exactly one of five outcomes, and only the first one means finished:

| Outcome | What it means |
|---|---|
| `DONE` | Tests pass, neither reviewer found anything that blocks. You still read and merge |
| `WAITING FOR APPROVAL` | The scenarios are written and wait for you |
| `TESTS ALREADY PASS` | Every new scenario passed before any code was written. The behaviour exists, or the scenarios test nothing |
| `TESTS NOT GREEN` | The implementer could not make them pass, or a test was changed along the way |
| `NOT READY` | A reviewer found something that blocks. You decide what happens next |

## Add the agents you need

This is a minimal example. Five agents is the smallest set that shows the method: one writes the
specification, one the tests, one the code, and two read the result. Your team will need more,
or different ones. That is expected, and it is not much work.

An agent is one Markdown file in `.claude/agents/`: a name, a description of when to use it, the
tools it may use, and its instructions. You do not have to write it yourself. In Claude Code, in
this folder, describe the agent you want and Claude writes the file. Read it before you use it.

Three rules keep an agent useful:

- **One role.** If you cannot say in one sentence when to use it, it is two agents.
- **As few tools as the role allows.** An agent that only reads cannot break anything.
- **No stack in the agent.** Commands and paths belong in `CLAUDE.md`, so that the agent survives a change of stack.

Five requests to start from. Paste one into Claude Code and adjust it:

**A product owner**, if requests arrive as one line and the specification keeps guessing:

```text
Add a product-owner agent in .claude/agents/. It reads a feature request before the spec-writer
does, and lists the questions the request leaves open: who it is for, what happens at the edges,
what is out of scope. It may only read. It does not approve anything: the person running
/feature decides. Then add it to /feature as the first step, before the spec-writer.
```

**A migration reviewer**, once your data matters:

```text
Add a migration-reviewer agent in .claude/agents/. It reads every new database migration in a
change and reports what could lose data or lock a large table, with the file and the line. It may
only read. Run it in step 4 of /feature next to the other reviewers, and let a blocking finding
end the run with NOT READY.
```

**An accessibility reviewer**, if people outside your team use the pages:

```text
Add an accessibility-reviewer agent in .claude/agents/. It reads the templates and the stylesheet
a change touches and checks them against WCAG 2.2 level AA: labels, focus, keyboard use, contrast,
headings. Every finding names the file, the line and who is affected. It may only read. Run it in
step 4 of /feature.
```

**An architect**, once a change can add an app, a model or a connection to another system:

```text
Add an architect agent in .claude/agents/. For a change that adds an app, a model or a
connection to another system, it reads the approved feature file and the project
instructions and proposes where the code goes, which modules change and what the data
model looks like. It may only read and write one design note. Add it to /feature between
the approval of the scenarios and the test-writer, and stop for my approval of the note.
```

**A documentation writer**, if the README falls behind:

```text
Add a documentation-writer agent in .claude/agents/. After /feature ends with DONE, it updates
README.md and CLAUDE.md where the change made them wrong. It may only edit those two files. Add
it to /feature as a last step that runs only after DONE.
```

Every agent you add to `/feature` makes each run slower and costs model time. Add one when you
have seen the problem it solves, not before.

## Try it

Add a rule yourself. In Claude Code, in this folder:

```text
/feature The submitter of a rejected document can submit it again, once. After that it waits for a review like a new document.
```

Read the scenarios it proposes. Who reviews the second time, and may it be the same reviewer?
What happens on a third try? Does the 30 days start again? If the request did not say, the
scenarios should ask. Approve them, and let the rest run.

Do not count on `DONE`. Of our own four runs of this request, three stopped with `NOT READY`
although every test was green: after a second submission the dashboard list "longest wait
first" was sorted on the first date, and no scenario said which date counts. A question nobody
asked, found before a person had to. The fourth ended with `DONE` and nine remarks for whoever
reads the change, among them that a document cannot be edited before it is submitted again.
Both endings are the pipeline doing its job. The same request does not give the same run twice.

Then ask for something that already exists and see that it does not pretend to have worked:

```text
/feature A document that has waited more than 30 days for a review is overdue.
```

## Use the agents in your own project

The agents are written for Claude Code: the folder `.claude/` and the command `/feature` are its
conventions. The method is not tied to it.

Copy `.claude/` into your repository and write your own `CLAUDE.md` with the same headings:
the commands, where things go, the order of work and the rules. The agents contain no command
and no path, so they work for a stack other than Django as long as your `CLAUDE.md` says how to
run the tests and where feature files and step definitions live.

## Why it is made this way

- **One role per agent.** An agent that plans, writes, tests and reviews cannot be judged, because you do not know which part went wrong.
- **The test comes first.** An agent that writes code and then tests writes tests that fit its code. They pass and prove nothing.
- **Who writes does not approve.** The reviewers run with read-only tools and sees the specification and the change, not the reasoning that produced it. The example application applies the same rule to its documents.
- **Gates beat instructions.** "Always run the tests" in an instruction file is a request. A pipeline that refuses to merge on a red test is a fact. The file `.claude/settings.json` denies a few commands, which helps, but a setting can be worked around. The real gate is a protected `main` branch on your server.
- **The colours are variables.** Every colour has a light and a dark value in one stylesheet, and the page follows the system until a visitor chooses. No JavaScript library, no web font, no Node.
- **Usable without a mouse, and without the script.** A skip link, a visible focus, a menu that closes on Escape and stays out of the way of the Tab key while it is closed, and scenarios that work out the contrast of the text colours and field edges in both themes. With JavaScript off the menu is simply there. Nobody has listened to it with a screen reader yet.

## Why behaviour first works so well with language models

- **A model writes convincingly, not necessarily correctly.** A scenario with concrete values
  turns "sounds right" into something that is true or false: overdue on day 31, not on day 30.
- **Gherkin is plain language.** You approve it in a minute, the model reads exactly what you
  approved, and the test runs exactly that. One text for three readers. That is how behaviour
  first bridges business and technology: a product owner, a lawyer or a client reads the same
  sentences the test runs, without reading code.
- **"Done" lives outside the model.** Without a scenario the model decides when it is finished.
  With a failing test, done is a fact it cannot talk its way around.
- **Gaps become questions.** A model fills in missing information silently. Examples on each
  side of a limit bring that filling-in to the surface before there is code. In our own runs
  the spec-writer answered a vague request with six questions instead of a guess.
- **Small steps with precise feedback.** One scenario is a bounded task, and a failing test says
  exactly what is wrong. A model does far better on that than on one large open request.
- **It survives a change of model.** The scenarios stay when you switch models. They are the
  agreement; the model is the one carrying it out.

The limit is just as clear. A vague or wrong scenario gives vague or wrong code that is green.
The specification is the ceiling, which is why a person approves it.

## What it gives, and what it costs

The main gain is a fixed bar. Every change goes through the same steps and the same gates,
whoever asks for it. A junior developer gets the same specification, the same tests up front
and the same two reviewers as a veteran. Quality then depends less on who works on it that
day and more on the setup.

It also moves work, and new bottlenecks appear where it lands:

- **CI/CD.** More changes mean more pipelines. If your runners cannot keep up, everybody waits
  on a runner instead of on the code.
- **Review.** A person reads every change before it is merged. Reading becomes the new work,
  and it is tempting to skim when a lot comes in.
- **Model time.** Every run costs it, and every agent you add makes a change slower and dearer.

Plan for these from the start. Small changes are quicker to read, and a pipeline that stops at
the first red test saves runner time.

## What this is not

It is an example, kept small on purpose. There is no registration, no password reset, no roles
and no support promise. Nothing limits how often somebody may try a password.

There is an image and a compose file to run the whole thing, and there are settings for a
server. That is not a deployment. The settings were checked with the deployment check and run
in the container, over plain HTTP on one machine. HTTPS, a proxy, backups and monitoring are
yours to add, and the part of the settings that only works behind HTTPS has not been seen working.

It shows how a team gets working, tested changes out of agents. The review rule in the example
is an illustration of separating duties. It is not evidence that an organisation meets a
standard. Showing an auditor that every change was specified, reviewed and traceable, which is
what standards such as ISO 27001 and NEN 7510 ask of a development process, takes more gates
than fit in a starter.

Semantag AI gives a training on exactly that, for development teams that work with agents.
[Plan an introduction](https://semantag.ai/en/?utm_source=github&utm_medium=readme&utm_campaign=django-claude-code-starter#contact)
and we lay your own pipeline next to the standard.

Does the rest of your organisation work with AI as well? The course
[Working responsibly with AI](https://semantag.ai/en/cursus/verantwoord-werken-met-ai?utm_source=github&utm_medium=readme&utm_campaign=django-claude-code-starter#contact)
takes one morning or afternoon and is for everybody who uses AI, not only developers.

## Checked with

| | |
|---|---|
| Last checked | 14 November 2026 |
| Claude Code | 2.1.323 |
| Model | Claude Opus 5.5 (14 November 2026), Claude Fable 5.2 (13 November 2026) |
| Python, Django, Tailwind | 3.14, 6.1, 4.3 |

Agents behave differently from one model version to the next. If a run goes wrong for you,
the five outcomes above are there so that it says so instead of reporting success.

## Licence

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). If you pass this code on, in
its original form or changed, the NOTICE file goes with it.

Copyright 2026 Semantag AI B.V., [semantag.ai](https://semantag.ai).
