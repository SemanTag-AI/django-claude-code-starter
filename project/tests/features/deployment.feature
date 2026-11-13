Feature: Settings for a server refuse to start half configured
  As somebody who puts the register on a server
  I want the application to stop when a secret or an address is missing
  So that it never runs with a value that was only meant for a laptop

  The complete set is: a secret key, the hosts it answers to, and the name, user,
  password and host of the database.

  Scenario Outline: The <environment> settings start when everything is given
    Given a server with the complete set of values
    When the application starts with the <environment> settings
    Then it starts
    And debug is off
    And browsers are told to use HTTPS for <duration>

    Examples:
      | environment | duration |
      | production  | a year   |
      | staging     | an hour  |

  Scenario Outline: Without <value> the production settings do not start
    Given a server with the complete set of values, except <value>
    When the application starts with the production settings
    Then it refuses and names <variable>

    Examples:
      | value                 | variable                 |
      | the secret key        | DJANGO_SECRET_KEY        |
      | the hosts             | DJANGO_ALLOWED_HOSTS     |
      | the database name     | DJANGO_DATABASE_NAME     |
      | the database user     | DJANGO_DATABASE_USER     |
      | the database password | DJANGO_DATABASE_PASSWORD |
      | the database host     | DJANGO_DATABASE_HOST     |

  Scenario: The development key is refused on a server
    Given a server with the complete set of values, but the secret key that ships with the code
    When the application starts with the production settings
    Then it refuses and names DJANGO_SECRET_KEY

  Scenario: Several hosts are given with commas between them
    Given a server with the complete set of values, and the hosts "register.example.org,www.example.org"
    When the application starts with the production settings
    Then it answers to "register.example.org" and to "www.example.org"

  Scenario: On a laptop the settings need nothing
    Given a laptop with no values at all
    When the application starts with the local settings
    Then it starts
    And debug is on

  Scenario: On a laptop debug can be switched off, but not with the key that ships with the code
    Given a laptop where only debug is switched off
    When the application starts with the local settings
    Then it refuses and names DJANGO_SECRET_KEY

  Scenario: The demo data is refused wherever debug is off
    Given a laptop where debug is switched off and a secret key of its own is given
    When somebody asks for the demo data with the local settings
    Then it refuses and says why
