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

  Scenario: The register itself refuses a review by the submitter
    When a review of the document "Access policy" by alice is written straight into the register
    Then the register refuses it
    And the document "Access policy" still waits for a review

  Scenario: The register itself refuses an approval without a reviewer
    When an approval of the document "Access policy" without a reviewer is written straight into the register
    Then the register refuses it
    And the document "Access policy" still waits for a review

  Scenario: A decision that is not on the list is not repeated back to the sender
    Given bob is signed in
    When he sends the decision "<script>alert(1)</script>" for the document "Access policy"
    Then the request is not accepted
    And the answer does not repeat what he sent

  Scenario: The register itself refuses a status that does not exist, even with a reviewer
    When the status "archived" with bob as reviewer is written straight into the register for the document "Access policy"
    Then the register refuses it
    And the document "Access policy" still waits for a review

  Scenario: A review sent without the form's protection against forged requests is refused
    Given bob is signed in in a client that checks forged requests
    When he sends an approval of the document "Access policy" without the form's token
    Then the request is refused
    And the document "Access policy" still waits for a review
