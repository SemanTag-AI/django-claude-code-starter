Feature: Text stays readable in the light and in the dark theme
  As somebody who does not see contrast well
  I want every text to stand out from what is behind it
  So that I can read the register in either theme

  The measure is the contrast ratio of the Web Content Accessibility Guidelines.
  Ordinary text needs at least 4.5 to 1.

  Scenario Outline: <text> on <background> in the <theme> theme
    Given the colours of the <theme> theme
    When the contrast of "<text>" on "<background>" is worked out
    Then it is at least 4.5 to 1

    Examples:
      | theme | text      | background  |
      | light | content   | page        |
      | light | content   | surface     |
      | light | content   | sidebar     |
      | light | muted     | page        |
      | light | muted     | surface     |
      | light | muted     | sidebar     |
      | light | accent    | page        |
      | light | accent    | surface     |
      | light | on-accent | accent      |
      | light | on-accent | accent-hover |
      | light | ok        | ok-soft     |
      | light | warn      | warn-soft   |
      | light | danger    | danger-soft |
      | light | danger    | surface     |
      | dark  | content   | page        |
      | dark  | content   | surface     |
      | dark  | content   | sidebar     |
      | dark  | muted     | page        |
      | dark  | muted     | surface     |
      | dark  | muted     | sidebar     |
      | dark  | accent    | page        |
      | dark  | accent    | surface     |
      | dark  | on-accent | accent      |
      | dark  | on-accent | accent-hover |
      | dark  | ok        | ok-soft     |
      | dark  | warn      | warn-soft   |
      | dark  | danger    | danger-soft |
      | dark  | danger    | surface     |
