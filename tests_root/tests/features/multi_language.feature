@JIRA-4
Feature: Multiple languages
  As an user
  I want to test the app in multiple languages


  @JIRA-5 @automated @market_en
  Scenario: Add two numbers
    When I have text <dad>
    When I have text <loves>
    When I have text <mom>
    When I merge the texts
    Then I get text <dad> <loves> <mom>
