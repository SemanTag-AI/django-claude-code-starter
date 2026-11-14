# Django Claude Code starter

A small Django and Tailwind application in which Claude Code agents work behaviour first:
a specification a person approves, then failing tests, then code, then a review
by an agent that did not write the code. A person merges.

It is a starting point for your own project and a working example of the method.
Clone it, run one command, and watch a feature go from a sentence to tested code.

Made by [Semantag AI](https://semantag.ai/en/?utm_source=github&utm_medium=readme&utm_campaign=django-claude-code-starter). It is not a product of Anthropic and is not endorsed by
Anthropic. Claude and Claude Code are trademarks of Anthropic.

## Start

You need [mise](https://mise.jdx.dev/) and, for the agents, [Claude Code](https://code.claude.com/docs). Node is not needed.

```bash
git clone https://github.com/SemanTag-AI/django-claude-code-starter.git
cd django-claude-code-starter
mise trust
mise run install   # dependencies and git hooks
mise run test      # 103 scenarios, all green
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

If it helps you, give it a star. That is how other teams find it, and how we see what is
worth working out further.

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

## Try it

Add a rule yourself. In Claude Code, in this folder:

```text
/feature The submitter of a rejected document can submit it again, once. After that it waits for a review like a new document.
```

Read the scenarios it proposes. Who reviews the second time, and may it be the same reviewer?
What happens on a third try? Does the 30 days start again? If the request did not say, the
scenarios should ask. Approve them, and let the rest run.

Do not count on `DONE`. Of our own four runs of this request (13 and 14 November 2026), three stopped with `NOT READY`
although every test was green: after a second submission the dashboard list "longest wait
first" was sorted on the first date, and no scenario said which date counts. A question nobody
asked, found before a person had to. The fourth ended with `DONE` and nine remarks for whoever
reads the change, among them that a document cannot be edited before it is submitted again.
Both endings are the pipeline doing its job. The same request does not give the same run twice.

Then ask for something that already exists and see that it does not pretend to have worked:

```text
/feature A document that has waited more than 30 days for a review is overdue.
```

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

One request to start from. Paste it into Claude Code and adjust it:

**A product owner**, if requests arrive as one line and the specification keeps guessing:

```text
Add a product-owner agent in .claude/agents/. It reads a feature request before the spec-writer
does, and lists the questions the request leaves open: who it is for, what happens at the edges,
what is out of scope. It may only read. It does not approve anything: the person running
/feature decides. Then add it to /feature as the first step, before the spec-writer.
```

Four more, for a migration reviewer, an accessibility reviewer, an architect and a documentation
writer, are in [docs/agents.md](docs/agents.md).

Every agent you add to `/feature` makes each run slower and costs model time. Add one when you
have seen the problem it solves, not before.

## Use the agents in your own project

The agents are written for Claude Code: the folder `.claude/` and the command `/feature` are its
conventions. The method is not tied to it.

Copy `.claude/` into your repository and write your own `CLAUDE.md` with the same headings:
the commands, where things go, the order of work and the rules. The agents name no
stack command and no path, so they work for a stack other than Django as long as your `CLAUDE.md` says how to
run the tests and where feature files and step definitions live.

## What is in the box

| Part | Where | What it does |
|---|---|---|
| Five agents | `.claude/agents/` | `spec-writer`, `test-writer`, `implementer`, `reviewer`, `security-reviewer`. One role each, and no more tools than the role needs. A minimal set, meant to be extended: see [Add the agents you need](#add-the-agents-you-need) |
| One command | `.claude/commands/feature.md` | `/feature <request>` runs the agents in order and stops for your approval after the specification |
| One skill | `.claude/skills/bdd-scenarios/` | How to write scenarios that pin a rule down |
| Project instructions | `CLAUDE.md` | The commands, the layout and the rules. The agents name no tool themselves: they read this file |
| An application | `project/`, `apps/` | A document register with a start page, a sign-in, a dashboard and a light and a dark mode |
| Scenarios | `apps/*/tests/`, `project/tests/`, `tests/e2e/` | 103 that need no browser, 24 that drive a real one. See [docs/tests.md](docs/tests.md) |
| Settings | `project/settings/` | `local`, `test`, `staging` and `production`. The last two refuse to start until every secret and address is given |
| A container | `Dockerfile`, `compose.yaml` | The register with PostgreSQL, to run the whole thing on your own machine. See [docs/running.md](docs/running.md) |
| Gates | `.pre-commit-config.yaml`, `.github/workflows/ci.yml` | Lint, checks, both sets of scenarios, a secret scan and a start of the container, outside the agents |

## Read further

| | |
|---|---|
| [docs/tests.md](docs/tests.md) | Where the scenarios live, one feature file with its step definitions in full, how pytest is set up |
| [docs/running.md](docs/running.md) | Running it in containers, and the settings for a laptop, a test run, staging and production |
| [docs/why.md](docs/why.md) | Why it is made this way, why behaviour first works so well with language models, and what it costs |
| [docs/agents.md](docs/agents.md) | Five agents you can add with one request to Claude Code |

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

Semantag AI trains development teams to make this auditable, and runs a course on working
responsibly with AI for everybody else: [training for development teams](https://semantag.ai/en/?utm_source=github&utm_medium=readme&utm_campaign=django-claude-code-starter#contact),
[course Working responsibly with AI](https://semantag.ai/en/cursus/verantwoord-werken-met-ai?utm_source=github&utm_medium=readme&utm_campaign=django-claude-code-starter#contact).

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
