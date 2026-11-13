Feature: Documents that wait too long for a review are overdue
  As somebody who is responsible for the register
  I want to see which documents have waited more than 30 days for a review
  So that no document stays unreviewed without anybody noticing

  The rule is "more than 30 full days", not "30 days or more". The second
  example pins that down, because it is the question people answer differently.
  The third pins down "full": 30 days and 23 hours is still day 30.

  Scenario Outline: A waiting document becomes overdue after 30 full days
    Given a document that was submitted <age> ago and waits for a review
    When somebody looks at the register today
    Then the document is <state>

    Examples:
      | age                  | state       |
      | 29 days              | not overdue |
      | 30 days              | not overdue |
      | 30 days and 23 hours | not overdue |
      | 31 days              | overdue     |
      | 0 days               | not overdue |

  Scenario Outline: A document that was reviewed is never overdue
    Given a document that was submitted 90 days ago and was <decision>
    When somebody looks at the register today
    Then the document is not overdue

    Examples:
      | decision |
      | approved |
      | rejected |
