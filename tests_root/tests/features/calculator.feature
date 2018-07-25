@JIRA-1
Feature: Calculator
  As an user
  I want to be able to sum numbers


  @JIRA-2 @automated
  Scenario: Add two numbers
    Given I have powered calculator on
    When I enter 50 into the calculator
    When I enter 70 into the calculator
    When I press add
    Then The result should be 120 on the screen


  @JIRA-3 @automated
  Scenario Outline: Add two numbers with examples
    Given I have powered calculator on
    When I enter <number_1> into the calculator
    When I enter <number_2> into the calculator
    When I press add
    Then The result should be <result> on the screen
    Examples:
      | number_1 | number_2 | result |
      | 10       | 20       | 30     |
      | 50       | 60       | 120    |
