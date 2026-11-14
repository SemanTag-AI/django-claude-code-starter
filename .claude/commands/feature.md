---
description: Take one feature from a sentence to reviewed, tested code. Specification first, then failing tests, then code, then review.
argument-hint: <what the feature should do, in one or two sentences>
---

Work this request through four steps, in this order. Each step has its own agent; step 4 has two:

$ARGUMENTS

Run each agent in the foreground and wait for its reply before you start the next. Pass every agent the request and the path of the feature file. Do the work of no step yourself.

The project instructions name the protected files: the tests and what configures them. From the moment the test-writer is done, nobody changes them.

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

Before you start, record a fingerprint of every protected file, for example with `git hash-object <file>` for each of them. Include the files git does not track yet: the feature file and the step definitions are new, and a snapshot that only knows tracked files would miss them. Keep the list. Do not commit.

Then use the implementer agent.

When it replies, take the fingerprints again and compare. A protected file that changed, disappeared or was added counts as a changed test. If that happened, say which file, restore it where git can, and end with the outcome TESTS NOT GREEN: a test that was changed to pass proves nothing.

- GREEN and nothing changed in the tests: go to step 4.
- NOT GREEN: stop. End with the outcome TESTS NOT GREEN and the last test output. Do not loosen a test and do not start a second attempt by yourself.

## Step 4. Review

Use the reviewer agent and the security-reviewer agent. They do not depend on each other, so you may run them at the same time. Tell both which feature file was approved and which files changed, and give both the change itself: the output of `git diff` for the files git tracks and the full text of every new file. They cannot run a command, so what you do not hand over they cannot see.

- Both report nothing that blocks (READY FOR A PERSON TO READ, NO BLOCKING FINDINGS): end with the outcome DONE.
- Either reports NOT READY: end with the outcome NOT READY and the findings of both. Fix nothing by yourself. The person decides what happens next.

## How to end

Always end with exactly one of these five outcomes on its own line, followed by what the person needs in order to act:

- `OUTCOME: DONE`, with the test commands, their last lines of output, the files that changed, any scenarios that already passed before the implementation, and the remarks of both reviewers. Say that a person still has to read and merge.
- `OUTCOME: WAITING FOR APPROVAL`, with the scenarios and the open questions.
- `OUTCOME: TESTS ALREADY PASS`, with the scenarios that passed.
- `OUTCOME: TESTS NOT GREEN`, with the last test output.
- `OUTCOME: NOT READY`, with the findings of the reviewer and the security-reviewer, each under its own heading.

Never report DONE without test output. Do not commit, push or merge.
