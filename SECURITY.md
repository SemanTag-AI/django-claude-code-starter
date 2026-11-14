# Security

## Reporting a problem

If you find a security problem in this repository, report it privately: on GitHub, open the tab
**Security** of this repository and choose **Report a vulnerability**. If that is not possible,
mail info@semantag.ai.

Please do not open a public issue for it. A public issue tells everybody how the problem works
before there is a fix, and everybody who already uses the starter is exposed until then.

Say what you found, how to reproduce it and what an attacker could do with it. You get an answer
within five working days.

## What to expect

This is a starter and an example. It is read and maintained when there is time, and there is no
promise that a fix arrives by a certain date. If you build on it, the security of what you build
is yours.

## What is deliberately not secure

These are choices, not oversights. Change them before real people or real documents are involved.

- `mise run demo` creates two users whose password is printed in the README. It refuses to run
  with debug off.
- There is no limit on how often somebody may try a password, no second factor, no registration
  and no password reset.
- The settings for a server have been checked with the deployment check of the framework and run
  in the container of this repository. They have not run behind a real proxy with HTTPS.
- `.claude/settings.json` denies a few commands to an agent. A setting can be worked around. The
  real gates are a protected `main` branch and the checks in CI.
