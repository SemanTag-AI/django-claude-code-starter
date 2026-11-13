Feature: Finding your way through the register
  As somebody who uses the register
  I want one menu that leads to every page
  So that I never have to type an address

  Background:
    Given the user bob
    And the user alice, who submitted the document "Access policy"

  Scenario: Signing in leads to the dashboard
    Given a visitor who has opened the sign-in page
    When the visitor signs in as bob
    Then the page with the heading "Dashboard" is open
    And the menu shows that bob is signed in

  Scenario Outline: The menu leads to every page
    Given bob is signed in in the browser
    When he follows "<link>" in the menu
    Then the page with the heading "<heading>" is open
    And the menu marks "<link>" as the current page

    Examples:
      | link         | heading      |
      | Dashboard    | Dashboard    |
      | Documents    | Documents    |
      | New document | New document |

  Scenario: A colleague approves a document in the browser
    Given bob is signed in in the browser
    And he has opened the document "Access policy" from the dashboard
    When he presses "Approve"
    Then the page says "The document was approved."
    And the page offers no review any more

  Scenario: Signing out closes the register
    Given bob is signed in in the browser
    When he presses "Sign out"
    Then the sign-in page is open

  Scenario: On a phone the menu stays out of the way
    Given bob is signed in in the browser on a phone
    When he looks at the dashboard
    Then the menu is out of view

  Scenario: On a phone the menu opens on request
    Given bob is signed in in the browser on a phone
    When he presses "Menu"
    Then the menu is in view
