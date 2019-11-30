@home_screen @nondestructive
Feature: Home Screen of Beep Web App
    As a User
    I want to navigate to the appropriate screen
    So that I can check if my account name or password have been compromised

    Background:
        Given I load the Beep app

    @S1 @automated @web @mobile-web
    Scenario: I can load the Beep homepage on web
        Then I should see app logo
        Then I should see the <account> button
        Then I should see the <password> button
        Then I should see the <how_does_it_work> link
        Then I should see the <app_store> link
        Then I should see the <google_play> link

    @S1 @automated @mobile-app
    Scenario: I can load the Beep homepage on mobile-app
        Then I should see app logo
        Then I should see the <account> button
        Then I should see the <password> button
        Then I should see the <how_does_it_work> link

    @automated @web @visual-regression @this
    Scenario: Homepage visual regression
        Then The app logo default visual is valid
        Then The account button default visual is valid
        Then The password button default visual is valid
