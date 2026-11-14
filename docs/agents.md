# Agents to add

Five requests to paste into Claude Code, in this folder. Adjust them to your project, and read
the file Claude writes before you use it.

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
