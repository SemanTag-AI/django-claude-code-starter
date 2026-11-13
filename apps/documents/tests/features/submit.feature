Feature: Submitting a document for review
  As somebody who writes documents
  I want to submit a document with a title and tags
  So that a colleague can review it

  Background:
    Given the users alice and bob
    And alice is signed in

  Scenario: A submitted document waits for a review
    When she submits a document with the title "Backup procedure" and the tags "procedure, report"
    Then the register holds a document "Backup procedure" that waits for a review
    And the document "Backup procedure" was submitted by alice
    And the document "Backup procedure" carries the tags "procedure, report"

  Scenario: A document without tags is accepted
    When she submits a document with the title "Meeting notes" and no tags
    Then the register holds a document "Meeting notes" that waits for a review

  Scenario: A document without a title is refused
    When she submits a document with the title "" and the tags "policy"
    Then the form says the title is required
    And the register holds no documents

  Scenario: A tag that is not on the list is refused
    When she submits a document with the title "Lunch menu" and the tags "food"
    Then the form says "food" is not a valid choice
    And the register holds no documents

  Scenario Outline: A title may be 200 characters long and no longer
    When she submits a document with a title of <length> characters
    Then the document is <outcome>

    Examples:
      | length | outcome                         |
      | 199    | accepted                        |
      | 200    | accepted                        |
      | 201    | refused because it is too long  |

  Scenario: A title is shown as text, never as markup
    Given she has submitted a document with the title "<script>alert(1)</script>" and no tags
    When she opens the list of documents
    Then the page shows the title "<script>alert(1)</script>" as plain text
