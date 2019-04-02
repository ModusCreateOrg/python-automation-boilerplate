@home_screen @nondestructive
Feature: Home Screen of Beep Web App
  As a User
  I want to navigate to the appropriate screen
  So that I can check if my account name or password have been compromised

  Background:
    Given User navigates to Beep homepage

  @s1 @automated
  Scenario: The user can load the Beep homepage
    Then Homepage content is loaded
    Then Beep logo is visible
    Then Beep title is visible
    Then Beep stores links are visible
