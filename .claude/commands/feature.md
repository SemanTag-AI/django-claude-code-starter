---
description: Take one feature from a sentence to reviewed, tested code. Specification first, then failing tests, then code, then review.
argument-hint: <what the feature should do, in one or two sentences>
---

Work this request through four steps, one agent per step, in this order:

$ARGUMENTS

Run each agent in the foreground and wait for its reply before you start the next. Pass every agent the request and the path of the feature file. Do the work of no step yourself.

## Step 1. Specification

Use the spec-writer agent.

If it reports that an existing feature file already covers the request, go to step 2 with that file and write nothing new.

Otherwise show the scenarios and the open questions to the person, and stop. End with the outcome WAITING FOR APPROVAL. Continue with step 2 only after the person has said the scenarios are right. If they ask for changes, send the changes to the spec-writer agent and show the result again.

## Step 2. Failing tests

Use the test-writer agent.

- RED FOR THE RIGHT REASON: go to step 3.
- PARTLY RED: go to step 3, and keep the list of scenarios that already passed and the reason for each. It goes into your final report, so that the person can see which examples did not prove anything by themselves.
- ALREADY PASSING: stop. End with the outcome TESTS ALREADY PASS. Nothing failed, so the behaviour exists or the scenarios test nothing. Change no code. If the person asks you to go on anyway, there is nothing to implement: the outcome stays TESTS ALREADY PASS, whatever a review of the existing code says.
- CANNOT TEST: stop and report the step that cannot be tested. End with the outcome WAITING FOR APPROVAL, because the specification needs another look.

## Step 3. Implementation

Before you start, note the state of the feature file and the step definitions, for example with `git stash create` or by committing them. Then use the implementer agent.

When it replies, compare the feature file and the step definitions with the state you noted. If either changed, restore them, and end with the outcome TESTS NOT GREEN: a test that was changed to pass proves nothing.

- GREEN and nothing changed in the tests: go to step 4.
- NOT GREEN: stop. End with the outcome TESTS NOT GREEN and the last test output. Do not loosen a test and do not start a second attempt by yourself.

## Step 4. Review

Use the reviewer agent. Tell it which feature file was approved and which files changed.

- READY FOR A PERSON TO READ: end with the outcome DONE.
- NOT READY: end with the outcome NOT READY and the findings. Fix nothing by yourself. The person decides what happens next.

## How to end

Always end with exactly one of these five outcomes on its own line, followed by what the person needs in order to act:

- `OUTCOME: DONE`, with the test command, its last lines of output, the files that changed, any scenarios that already passed before the implementation, and the reviewer's remarks. Say that a person still has to read and merge.
- `OUTCOME: WAITING FOR APPROVAL`, with the scenarios and the open questions.
- `OUTCOME: TESTS ALREADY PASS`, with the scenarios that passed.
- `OUTCOME: TESTS NOT GREEN`, with the last test output.
- `OUTCOME: NOT READY`, with the reviewer's findings.

Never report DONE without test output. Do not commit, push or merge.
