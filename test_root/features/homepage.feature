@Home_Screen
Feature: Home Screen of Beep Web App
  As a User
  I want to navigate to the appropriate screen
  So that I can check if my account name or password have been compromised


  Background:
    Given Beep app Homepage loads successfully


  @automated
  Scenario: User navigates to Account
    Given User clicks on "account" button
    Then "Account" loads successfully

  @automated
  Scenario: User navigates to Password
    Given User clicks on "password" button
    Then "Password" loads successfully
