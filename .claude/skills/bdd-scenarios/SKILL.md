---
name: bdd-scenarios
description: How to write Gherkin scenarios that pin a rule down. Use when writing or reviewing a feature file, when a requirement mentions a threshold, a limit or a date, or when a scenario is vague.
---

# Writing scenarios that pin a rule down

A scenario is an example with an answer. If two people can read it and expect different outcomes, it is not finished.

## One rule, one scenario, real values

Bad, because nobody can check it:

```gherkin
Scenario: Large orders get a discount
  Given a large order
  When the customer pays
  Then a discount is applied
```

Good, because it is either true or false:

```gherkin
Scenario: A basket over the threshold gets 10 percent off
  Given a basket with a total of 120.00 euro
  When the customer checks out
  Then the amount due is 108.00 euro
```

## Every threshold needs three examples

"More than 100" and "100 or more" are different rules, and requests rarely say which is meant. Write the value just below, the value exactly on and the value just above the threshold. Use a `Scenario Outline` with an `Examples` table when only the numbers differ:

```gherkin
Scenario Outline: The discount depends on the basket total
  Given a basket with a total of <total> euro
  When the customer checks out
  Then the amount due is <due> euro

  Examples:
    | total  | due    |
    | 99.99  | 99.99  |
    | 100.00 | 100.00 |
    | 100.01 | 90.01  |
```

The third row also settles a question nobody asked: what happens to half a cent.

## Checklist before a scenario goes to a person

- Does every `Then` name a value somebody can compare?
- Is there an example on each side of every limit, and one exactly on it?
- What about nothing at all: an empty basket, a zero, a missing field?
- Does a step name a function, a table or a screen element? Rewrite it as something a user would say.
- Does one scenario test two rules? Split it.
- Is anything in the request open to two readings? Do not choose. Write it down as a question.

## Steps

- `Given` describes the situation, `When` the one action, `Then` what can be observed. One `When` per scenario.
- Reuse the wording of steps that already exist. Two phrasings of the same step are two step definitions to maintain.
