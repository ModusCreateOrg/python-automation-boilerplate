@home_screen @nondestructive
Feature: Home Screen of Beep Web App
  As a User
  I want to navigate to the appropriate screen
  So that I can check if my account name or password have been compromised


  @s1 @automated @web
  Scenario: The user can load the Beep homepage
    Given User navigates to Beep homepage
    Then Homepage content is loaded
    Then Beep logo is visible
    Then Beep title is visible
    Then Beep stores links are visible


  @s1 @automated @hybrid
  Scenario: The user can load Beep app
    Given User opens Beep app
    Then Homepage content is loaded
    Then Beep logo is visible
    Then Beep title is visible
