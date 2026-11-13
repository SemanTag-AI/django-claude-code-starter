Feature: Only signed-in users see the register
  As somebody who is responsible for the register
  I want every page to ask for a sign-in
  So that documents are not readable by anybody who knows the address

  Background:
    Given the users alice and bob
    And a document "Access policy" that alice submitted and that waits for a review

  Scenario Outline: A visitor who is not signed in is sent to the sign-in page
    When a visitor opens <page>
    Then the visitor is sent to the sign-in page

    Examples:
      | page                         |
      | the dashboard                |
      | the list of documents        |
      | the form for a new document  |
      | the document "Access policy" |

  Scenario Outline: A signed-in user can open every page
    Given bob is signed in
    When he opens <page>
    Then the page opens
    And the page shows no leftover template code
    And the title of the page is "<title>"

    Examples:
      | page                         | title         |
      | the dashboard                | Dashboard     |
      | the list of documents        | Documents     |
      | the form for a new document  | New document  |
      | the document "Access policy" | Access policy |

  Scenario: The start page opens for everybody and says what the register is for
    When a visitor opens the start page
    Then the page opens
    And the page says what the register is for
    And the page offers the sign-in
    And the page shows no leftover template code

  Scenario: Signing in from the start page leads to the dashboard
    Given a visitor who has opened the start page
    When bob signs in with the form on that page
    Then he is sent to the dashboard

  Scenario: After signing in a visitor lands on the page that was asked for
    Given a visitor who was sent to the sign-in page from the list of documents
    When bob signs in with the form on that page
    Then he is sent to the list of documents

  Scenario: The start page leads a signed-in user to the dashboard
    Given bob is signed in
    When he opens the start page
    Then he is sent to the dashboard

  Scenario: The sign-in page opens for everybody
    When a visitor opens the sign-in page
    Then the page opens
    And the page shows no leftover template code

  Scenario: Signing in with the right password leads to the dashboard
    When bob signs in with the right password
    Then he is sent to the dashboard

  Scenario: Signing in with a wrong password is refused
    When bob signs in with a wrong password
    Then the sign-in page says the name and password do not match

  Scenario: After signing out the register is closed again
    Given bob was signed in and has signed out
    When a visitor opens the dashboard
    Then the visitor is sent to the sign-in page

  Scenario: The health address answers without a sign-in
    When a visitor opens the health address
    Then the page opens

  Scenario: A document that does not exist is reported as not found
    Given bob is signed in
    When he opens a document that does not exist
    Then the page is not found

  Scenario: A visitor cannot send a review
    When a visitor sends an approval of the document "Access policy"
    Then the visitor is sent to the sign-in page
    And the document "Access policy" still waits for a review
