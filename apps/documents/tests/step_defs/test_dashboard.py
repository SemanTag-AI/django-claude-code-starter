"""Step definitions for dashboard.feature."""

from pytest_bdd import given, parsers, scenarios, then

from .conftest import document_titled, make_document, shown

scenarios("../features/dashboard.feature")


def rows(datatable: list[list[str]]) -> list[dict[str, str]]:
    header, *lines = datatable
    return [dict(zip(header, line, strict=True)) for line in lines]


@given("these documents:")
def these_documents(datatable: list[list[str]]) -> None:
    for row in rows(datatable):
        make_document(row["title"], row["submitted by"], int(row["days ago"]), row["status"])


@then("the dashboard shows these numbers:")
def numbers(context: dict, datatable: list[list[str]]) -> None:
    assert context["response"].status_code == 200
    for row in rows(datatable):
        assert shown(context["response"], f"tile-{row['tile']}") == [row["number"]], row["tile"]


@then(parsers.parse('the list of documents to review holds "{title}"'))
def to_review_holds(context: dict, title: str) -> None:
    assert context["response"].status_code == 200
    assert title in shown(context["response"], "to-review-title")


@then(parsers.parse('the list of documents to review does not hold "{title}"'))
def to_review_does_not_hold(context: dict, title: str) -> None:
    assert context["response"].status_code == 200
    assert title not in shown(context["response"], "to-review-title")


@then(parsers.parse('the document "{title}" is marked as overdue'))
def marked_overdue(context: dict, title: str) -> None:
    marker = f'data-test="overdue-badge" data-document="{document_titled(title).pk}"'
    assert marker in context["response"].content.decode()


@then("the dashboard says there are no documents yet")
def no_documents(context: dict) -> None:
    assert shown(context["response"], "no-documents") != []


@then("the list of documents to review holds, in this order:")
def to_review_in_order(context: dict, datatable: list[list[str]]) -> None:
    assert shown(context["response"], "to-review-title") == [row["title"] for row in rows(datatable)]


@then(parsers.parse("the dashboard says that {number:d} documents wait for his review"))
def for_you(context: dict, number: int) -> None:
    assert shown(context["response"], "for-you-count") == [str(number)]
