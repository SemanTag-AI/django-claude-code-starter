# Contributing

This repository is an example, kept small on purpose. Issues and pull requests are welcome, and
there is no promise that they are answered or merged.

If you send a change, work the way the repository does:

1. Start with a feature file that says what should happen, with real values and an example on
   each side of every limit. See `.claude/skills/bdd-scenarios/SKILL.md`.
2. Add step definitions and see them fail because the behaviour is missing.
3. Write the code that makes them pass. Do not change a test to get there.
4. Run `mise run lint`, `mise run check`, `mise run test` and, when a template, the stylesheet or
   the script changed, `mise run test:e2e`.

A change that makes the starter bigger needs a reason. A change that makes it smaller or clearer
does not.

Security problems go to the address in [SECURITY.md](SECURITY.md), not into an issue.

By sending a change you agree that it is licensed under the Apache License 2.0, like the rest.
