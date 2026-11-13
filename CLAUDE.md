# Project instructions

This file is what every agent reads before it works in this repository. The
agents in `.claude/agents/` name no tool and no path themselves: they follow
what is written here. Change the stack, and this is the file to change.

## Commands

| Job | Command |
|---|---|
| Install dependencies and git hooks | `mise run install` |
| Run every scenario that needs no browser | `mise run test` |
| Run the scenarios that drive a real browser | `mise run test:e2e` |
| Check formatting and lint rules | `mise run lint` |
| Fix formatting | `uv run ruff format .` |
| Run the framework checks and look for a missing migration | `mise run check` |
| Run the deployment check on the staging and production settings | `mise run check:deploy` |
| Write a migration after a model change | `uv run python manage.py makemigrations` |
| Compile the stylesheet | `mise run css` |
| Run the development server | `mise run dev` |
| Fill an empty register with demo data | `mise run demo` |
| Scan every commit for credentials | `mise run secrets` |
| Make the container image | `mise run docker:build` |
| Run the register and its database in containers | `mise run docker:up` |

There are two test commands, and each scenario is covered by exactly one of them:

- `mise run test` runs every scenario that is not marked `e2e`.
- `mise run test:e2e` runs the scenarios marked `e2e`, in a real browser. `mise run test` leaves them out without saying so.

A change to a template, the stylesheet or the script needs both. So does any feature with a
scenario marked `e2e`. The scenarios without a browser read the HTML. They cannot see a page
that looks broken. Use these two commands and nothing else, so that everybody runs the same thing.

## Protected files

Once step definitions exist for an approved feature file, these do not change until a person has
read the result:

- everything in a `tests` folder: feature files, step definitions and the `conftest.py` files next to them
- `pyproject.toml` and `mise.toml`, because they decide which tests run and how
- any `conftest.py` anywhere in the repository

## Where things go

- A feature file: `apps/<app>/tests/features/<name>.feature`
- Its step definitions: `apps/<app>/tests/step_defs/test_<name>.py`. Steps that several features share live in `conftest.py` next to them.
- Scenarios that need a browser carry the marker `e2e` and live in `apps/theme/tests/`.
- Business rules: a plain module in the app, such as `apps/documents/rules.py`. Views call rules; rules know nothing about views.
- Numbers for a page: a function that returns a Pydantic model, such as `apps/documents/summary.py`. The view does no arithmetic.
- Templates: `apps/<app>/templates/<app>/`. A page behind the sign-in extends `base.html` from `apps/theme`; a page for everybody extends `theme/public.html`.
- Styling: Tailwind classes in the template. Colours are variables in `apps/theme/css/source.css`, each with a light and a dark value. Use the names (`bg-surface`, `text-muted`), not a fixed colour, or the dark mode breaks.
- A test finds an element by its role, its label or its `data-test` attribute, never by a class.
- Settings: `project/settings/`. `local` for your machine, `test` for the test run, `production` for a server and `staging` for a rehearsal of one. `staging` imports `production` and changes as little as it can.
- A new colour needs a light and a dark value and a row in `apps/theme/tests/features/contrast.feature`.

## Order of work

1. The specification comes first: a feature file a person has approved.
2. Then step definitions that fail because the behaviour is missing, not because of a typo or an import error.
3. Then the code that makes them pass.
4. Then a review by an agent that did not write the code, and a merge by a person.

## Rules

- Never change a protected file to make a failing test pass. If a test looks wrong, stop and say why.
- Never skip the git hooks (`--no-verify`, `-n`) and never force-push.
- Never write "done" without the command you ran and its output.
- A person merges. No agent merges or pushes to `main`.
- A rule that protects something is enforced on the server. Hiding a button is a courtesy, not a control.
- Every page of the register asks for a signed-in user. Only the start page, the sign-in page and the health address are open.
- A rule that must never be broken is also a constraint in the database, so that it holds when the code has a bug.
- A value a server cannot run without has no default. The settings stop and name it (`required` in `project/settings/env.py`).

## Code style

- Python: Google style docstrings, type hints on every function, 120 characters per line. `ruff` decides the rest.
- Views are class-based.
- A fixed set of choices is an `enum.StrEnum`. A structured value that crosses a boundary is a Pydantic `BaseModel`.
- Configuration is read in `project/settings/env.py` and nowhere else.
- A function that depends on the time takes the time as an argument, so that a test can choose it.
- No JavaScript library and no web font. The script in `apps/theme/static/theme/app.js` is all there is.
- Every page works with the keyboard alone and with JavaScript off. A menu button names what it opens in `aria-controls`.
