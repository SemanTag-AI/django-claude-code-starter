"""Step definitions for deployment.feature.

Settings are read once, when the process starts. So every scenario starts a process of
its own, with exactly the environment the scenario describes and no ``.env`` file.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/deployment.feature")

ROOT = Path(__file__).resolve().parents[3]

COMPLETE = {
    "DJANGO_SECRET_KEY": "a-key-for-this-scenario-only-that-is-long-enough-to-be-one",
    "DJANGO_ALLOWED_HOSTS": "register.example.org",
    "DJANGO_DATABASE_NAME": "register",
    "DJANGO_DATABASE_USER": "register",
    "DJANGO_DATABASE_PASSWORD": "a-password-for-this-scenario-only",
    "DJANGO_DATABASE_HOST": "database.example.org",
}
VARIABLE = {
    "the secret key": "DJANGO_SECRET_KEY",
    "the hosts": "DJANGO_ALLOWED_HOSTS",
    "the database name": "DJANGO_DATABASE_NAME",
    "the database user": "DJANGO_DATABASE_USER",
    "the database password": "DJANGO_DATABASE_PASSWORD",
    "the database host": "DJANGO_DATABASE_HOST",
}
SHOW = (
    "import json, importlib, sys;"
    "s = importlib.import_module(sys.argv[1]);"
    "print(json.dumps({'debug': s.DEBUG, 'hosts': s.ALLOWED_HOSTS, 'hsts': getattr(s, 'SECURE_HSTS_SECONDS', 0),"
    " 'engine': s.DATABASES['default']['ENGINE']}))"
)


@pytest.fixture
def values() -> dict[str, str]:
    """The environment of the process a scenario is about to start."""
    return {}


def start(values: dict[str, str], *command: str) -> subprocess.CompletedProcess:
    """Run a command with only the given values, and without any ``.env`` file."""
    environment = {"PATH": os.environ["PATH"], "DJANGO_ENV_FILE": os.devnull, **values}
    return subprocess.run([sys.executable, *command], cwd=ROOT, env=environment, capture_output=True, text=True)  # noqa: S603


@given("a server with the complete set of values")
def complete(values: dict[str, str]) -> None:
    values.update(COMPLETE)


@given(parsers.parse("a server with the complete set of values, except {value}"))
def complete_except(values: dict[str, str], value: str) -> None:
    values.update(COMPLETE)
    del values[VARIABLE[value]]


@given("a server with the complete set of values, but the secret key that ships with the code")
def complete_with_development_key(values: dict[str, str]) -> None:
    from project.settings.env import DEVELOPMENT_SECRET_KEY

    values.update(COMPLETE)
    values["DJANGO_SECRET_KEY"] = DEVELOPMENT_SECRET_KEY


@given(parsers.parse('a server with the complete set of values, and the hosts "{hosts}"'))
def complete_with_hosts(values: dict[str, str], hosts: str) -> None:
    values.update(COMPLETE)
    values["DJANGO_ALLOWED_HOSTS"] = hosts


@given("a laptop with no values at all")
def nothing(values: dict[str, str]) -> None:
    assert values == {}


@given("a laptop where only debug is switched off")
def debug_off(values: dict[str, str]) -> None:
    values["DJANGO_DEBUG"] = "false"


@given("a laptop where debug is switched off and a secret key of its own is given")
def debug_off_with_key(values: dict[str, str]) -> None:
    values["DJANGO_DEBUG"] = "false"
    values["DJANGO_SECRET_KEY"] = COMPLETE["DJANGO_SECRET_KEY"]


@when(parsers.parse("the application starts with the {name} settings"), target_fixture="started")
def application_starts(values: dict[str, str], name: str) -> subprocess.CompletedProcess:
    return start(values, "-c", SHOW, f"project.settings.{name}")


@when(parsers.parse("somebody asks for the demo data with the {name} settings"), target_fixture="started")
def ask_for_demo_data(values: dict[str, str], name: str) -> subprocess.CompletedProcess:
    return start(values, "manage.py", "seed_demo", f"--settings=project.settings.{name}")


def shown(started: subprocess.CompletedProcess) -> dict:
    assert started.returncode == 0, started.stderr[-600:]
    return json.loads(started.stdout)


@then("it starts")
def it_starts(started: subprocess.CompletedProcess) -> None:
    shown(started)


@then(parsers.parse("debug is {state}"))
def debug_is(started: subprocess.CompletedProcess, state: str) -> None:
    assert shown(started)["debug"] is (state == "on")


@then(parsers.parse("browsers are told to use HTTPS for {duration}"))
def https_for(started: subprocess.CompletedProcess, duration: str) -> None:
    assert shown(started)["hsts"] == {"a year": 365 * 24 * 3600, "an hour": 3600}[duration]


@then(parsers.parse("it refuses and names {variable}"))
def refuses_and_names(started: subprocess.CompletedProcess, variable: str) -> None:
    assert started.returncode != 0, "it started"
    assert variable in started.stderr, started.stderr[-600:]


@then(parsers.parse('it answers to "{first}" and to "{second}"'))
def answers_to(started: subprocess.CompletedProcess, first: str, second: str) -> None:
    assert shown(started)["hosts"] == [first, second]


@then("it refuses and says why")
def refuses_and_says_why(started: subprocess.CompletedProcess) -> None:
    assert started.returncode != 0, "it created the demo users"
    assert "public password" in started.stderr, started.stderr[-600:]
