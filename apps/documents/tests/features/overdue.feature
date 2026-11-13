Feature: Documents that wait too long for a review are overdue
  As somebody who is responsible for the register
  I want to see which documents have waited more than 30 days for a review
  So that no document stays unreviewed without anybody noticing

  The rule is "more than 30 full days", not "30 days or more". The second
  example pins that down, because it is the question people answer differently.

  Scenario Outline: A waiting document becomes overdue after 30 full days
    Given a document that was submitted <days> days ago and waits for a review
    When somebody looks at the register today
    Then the document is <state>

    Examples:
      | days | state       |
      | 29   | not overdue |
      | 30   | not overdue |
      | 31   | overdue     |
      | 0    | not overdue |

  Scenario Outline: A document that was reviewed is never overdue
    Given a document that was submitted 90 days ago and was <decision>
    When somebody looks at the register today
    Then the document is not overdue

    Examples:
      | decision |
      | approved |
      | rejected |
