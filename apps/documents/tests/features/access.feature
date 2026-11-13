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
      | the start page               |
      | the dashboard                |
      | the list of documents        |
      | the form for a new document  |
      | the document "Access policy" |

  Scenario Outline: A signed-in user can open every page
    Given bob is signed in
    When he opens <page>
    Then the page opens

    Examples:
      | page                         |
      | the dashboard                |
      | the list of documents        |
      | the form for a new document  |
      | the document "Access policy" |

  Scenario: The start page leads a signed-in user to the dashboard
    Given bob is signed in
    When he opens the start page
    Then he is sent to the dashboard

  Scenario: The sign-in page opens for everybody
    When a visitor opens the sign-in page
    Then the page opens

  Scenario: Signing in with the right password leads to the dashboard
    When bob signs in with the right password
    Then he is sent to the dashboard

  Scenario: Signing in with a wrong password is refused
    When bob signs in with a wrong password
    Then the sign-in page says the name and password do not match

  Scenario: After signing out the register is closed again
    Given bob is signed in
    When he signs out
    And a visitor opens the dashboard
    Then the visitor is sent to the sign-in page

  Scenario: A document that does not exist is reported as not found
    Given bob is signed in
    When he opens a document that does not exist
    Then the page is not found

  Scenario: A visitor cannot send a review
    When a visitor sends an approval of the document "Access policy"
    Then the visitor is sent to the sign-in page
    And the document "Access policy" still waits for a review
