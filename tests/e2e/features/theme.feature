Feature: A light and a dark mode
  As somebody who reads the register for hours
  I want the pages in a light or a dark theme
  So that I can read them in the light I work in

  The page follows the system until the visitor chooses. After that the choice wins.

  Scenario Outline: The page follows the system until the visitor chooses
    Given a visitor whose system prefers the <system> theme
    When the visitor opens the sign-in page
    Then the page is shown in the <system> theme

    Examples:
      | system |
      | light  |
      | dark   |

  Scenario: The switch changes the theme
    Given a visitor whose system prefers the light theme
    And the visitor has opened the sign-in page
    When the visitor uses the theme switch
    Then the page is shown in the dark theme
    And the theme switch says that the dark mode is on

  Scenario: The choice survives a reload
    Given a visitor whose system prefers the light theme
    And the visitor has opened the sign-in page
    And the visitor has used the theme switch
    When the visitor reloads the page
    Then the page is shown in the dark theme

  Scenario: The choice wins over the system
    Given a visitor whose system prefers the dark theme
    And the visitor has opened the sign-in page
    And the visitor has used the theme switch
    When the visitor reloads the page
    Then the page is shown in the light theme

  Scenario: The choice carries over to the pages behind the sign-in
    Given the user bob
    And a visitor whose system prefers the light theme
    And the visitor has opened the sign-in page
    And the visitor has used the theme switch
    When the visitor signs in as bob
    Then the page is shown in the dark theme
