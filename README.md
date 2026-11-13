# Django agent starter

A small Django and Tailwind application in which coding agents work behaviour first:
a specification a person approves, then failing tests, then code, then a review
by an agent that did not write the code. A person merges.

It is a starting point for your own project and a working example of the method.
Clone it, run one command, and watch a feature go from a sentence to tested code.

Made by [Semantag AI](https://semantag.ai).

## What is in the box

| Part | Where | What it does |
|---|---|---|
| Four agents | `.claude/agents/` | `spec-writer`, `test-writer`, `implementer`, `reviewer`. One role each, and no more tools than the role needs |
| One command | `.claude/commands/feature.md` | `/feature <request>` runs the four agents in order and stops for your approval after the specification |
| One skill | `.claude/skills/bdd-scenarios/` | How to write scenarios that pin a rule down |
| Project instructions | `CLAUDE.md` | The commands, the layout and the rules. The agents name no tool themselves: they read this file |
| An application | `project/`, `apps/` | A document register with a start page, a sign-in, a dashboard and a light and a dark mode |
| Scenarios | `apps/*/tests/features/`, `project/tests/features/` | 99 that need no browser, 23 that drive a real one |
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
git clone https://github.com/semantag/django-agent-starter.git
cd django-agent-starter
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
        |
  you merge        no agent pushes to main
```

`/feature` always ends with exactly one of five outcomes, and only the first one means finished:

| Outcome | What it means |
|---|---|
| `DONE` | Tests pass, the reviewer found nothing that blocks. You still read and merge |
| `WAITING FOR APPROVAL` | The scenarios are written and wait for you |
| `TESTS ALREADY PASS` | Every new scenario passed before any code was written. The behaviour exists, or the scenarios test nothing |
| `TESTS NOT GREEN` | The implementer could not make them pass, or a test was changed along the way |
| `NOT READY` | The reviewer found something that blocks. You decide what happens next |

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

Copy `.claude/` into your repository and write your own `CLAUDE.md` with the same headings:
the commands, where things go, the order of work and the rules. The agents contain no command
and no path, so they work for a stack other than Django as long as your `CLAUDE.md` says how to
run the tests and where feature files and step definitions live.

## Why it is made this way

- **One role per agent.** An agent that plans, writes, tests and reviews cannot be judged, because you do not know which part went wrong.
- **The test comes first.** An agent that writes code and then tests writes tests that fit its code. They pass and prove nothing.
- **Who writes does not approve.** The reviewer runs with read-only tools and sees the specification and the change, not the reasoning that produced it. The example application applies the same rule to its documents.
- **Gates beat instructions.** "Always run the tests" in an instruction file is a request. A pipeline that refuses to merge on a red test is a fact. The file `.claude/settings.json` denies a few commands, which helps, but a setting can be worked around. The real gate is a protected `main` branch on your server.
- **The colours are variables.** Every colour has a light and a dark value in one stylesheet, and the page follows the system until a visitor chooses. No JavaScript library, no web font, no Node.
- **Usable without a mouse, and without the script.** A skip link, a visible focus, a menu that closes on Escape and stays out of the way of the Tab key while it is closed, and scenarios that work out the contrast of the text colours and field edges in both themes. With JavaScript off the menu is simply there. Nobody has listened to it with a screen reader yet.

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

Semantag AI gives a training on exactly that, for development teams that work with agents:
[semantag.ai](https://semantag.ai/nl/?utm_source=github&utm_medium=readme&utm_campaign=django-agent-starter#contact).

## Checked with

| | |
|---|---|
| Last checked | 13 November 2026 |
| Claude Code | 2.1.323 |
| Model | Claude Fable 5.2 |
| Python, Django, Tailwind | 3.14, 6.1, 4.3 |

Agents behave differently from one model version to the next. If a run goes wrong for you,
the five outcomes above are there so that it says so instead of reporting success.

## Licence

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). If you pass this code on, in
its original form or changed, the NOTICE file goes with it.

Copyright 2026 Semantag AI B.V., [semantag.ai](https://semantag.ai).
