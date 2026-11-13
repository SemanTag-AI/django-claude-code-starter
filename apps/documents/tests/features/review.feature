Feature: A document is reviewed by somebody who did not submit it
  As somebody who is responsible for the register
  I want every document to be approved or rejected by a second person
  So that nobody signs off on their own work

  Background:
    Given the users alice and bob
    And a document "Access policy" that alice submitted and that waits for a review

  Scenario: The submitter gets no way to review their own document
    Given alice is signed in
    When she opens the document "Access policy"
    Then the page offers no review

  Scenario: The submitter is refused when she sends the approval anyway
    Given alice is signed in
    When she sends an approval of the document "Access policy"
    Then the request is refused
    And the document "Access policy" still waits for a review

  Scenario: A colleague is offered the review
    Given bob is signed in
    When he opens the document "Access policy"
    Then the page offers a review

  Scenario: A colleague approves the document
    Given bob is signed in
    When he sends an approval of the document "Access policy"
    Then the document "Access policy" is approved by bob

  Scenario: A colleague rejects the document
    Given bob is signed in
    When he sends a rejection of the document "Access policy"
    Then the document "Access policy" is rejected by bob

  Scenario: A document that was reviewed cannot be reviewed a second time
    Given the user carol
    And bob has approved the document "Access policy"
    And carol is signed in
    When she sends a rejection of the document "Access policy"
    Then the page says the document was already reviewed
    And the document "Access policy" is approved by bob

  Scenario: A decision other than approve or reject is refused
    Given bob is signed in
    When he sends the decision "waiting" for the document "Access policy"
    Then the request is not accepted
    And the document "Access policy" still waits for a review
