# Why it is made this way


- **One role per agent.** An agent that plans, writes, tests and reviews cannot be judged, because you do not know which part went wrong.
- **The test comes first.** An agent that writes code and then tests writes tests that fit its code. They pass and prove nothing.
- **Who writes does not approve.** The reviewers run with read-only tools and see the specification and the change, not the reasoning that produced it. The example application applies the same rule to its documents.
- **Gates beat instructions.** "Always run the tests" in an instruction file is a request. A pipeline that refuses to merge on a red test is a fact. The file `.claude/settings.json` denies every push and the usual ways to skip a hook, which helps, but a setting can be worked around. The real gate is a protected `main` branch on your server.
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
  side of a limit bring that filling-in to the surface before there is code. In one of our own
  runs (14 November 2026) the spec-writer answered a vague request with six questions instead of a guess.
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
