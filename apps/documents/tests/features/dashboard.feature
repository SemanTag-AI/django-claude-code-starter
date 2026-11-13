Feature: The dashboard counts where the documents stand
  As somebody who is responsible for the register
  I want to see at a glance how many documents wait, are overdue or were reviewed
  So that I know where to look first

  Background:
    Given the users alice and bob

  Scenario: The tiles count the documents per status
    Given these documents:
      | title            | submitted by | days ago | status   |
      | Access policy    | alice        | 2        | waiting  |
      | Backup procedure | bob          | 30       | waiting  |
      | Supplier list    | alice        | 31       | waiting  |
      | Privacy notice   | alice        | 60       | approved |
      | Old contract     | bob          | 90       | rejected |
    And bob is signed in
    When he opens the dashboard
    Then the dashboard shows these numbers:
      | tile     | number |
      | waiting  | 3      |
      | overdue  | 1      |
      | approved | 1      |
      | rejected | 1      |

  Scenario: The dashboard lists what waits for a review by the signed-in user
    Given these documents:
      | title            | submitted by | days ago | status   |
      | Access policy    | alice        | 2        | waiting  |
      | Backup procedure | bob          | 3        | waiting  |
      | Privacy notice   | alice        | 60       | approved |
    And bob is signed in
    When he opens the dashboard
    Then the list of documents to review holds "Access policy"
    And the list of documents to review does not hold "Backup procedure"
    And the list of documents to review does not hold "Privacy notice"

  Scenario: An overdue document is marked on the dashboard
    Given these documents:
      | title         | submitted by | days ago | status  |
      | Supplier list | alice        | 31       | waiting |
    And bob is signed in
    When he opens the dashboard
    Then the document "Supplier list" is marked as overdue

  Scenario: An empty register shows zeros and says so
    Given bob is signed in
    When he opens the dashboard
    Then the dashboard shows these numbers:
      | tile     | number |
      | waiting  | 0      |
      | overdue  | 0      |
      | approved | 0      |
      | rejected | 0      |
    And the dashboard says there are no documents yet

  Scenario: The list of documents to review starts with the longest wait and shows five at most
    Given these documents:
      | title      | submitted by | days ago | status  |
      | Document A | alice        | 1        | waiting |
      | Document B | alice        | 5        | waiting |
      | Document C | alice        | 3        | waiting |
      | Document D | alice        | 40       | waiting |
      | Document E | alice        | 2        | waiting |
      | Document F | alice        | 4        | waiting |
      | Document G | bob          | 50       | waiting |
    And bob is signed in
    When he opens the dashboard
    Then the list of documents to review holds, in this order:
      | title      |
      | Document D |
      | Document B |
      | Document F |
      | Document C |
      | Document E |
    And the dashboard says that 6 documents wait for his review
