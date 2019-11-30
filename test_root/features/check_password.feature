@password_screen @nondestructive
Feature: Password screen of Beep web app
    As a user of Beep web app
    I want to be able to provide my password on the Password page
    So that I know if my account data has been compromised


    Background:
        Given I load the Beep app

    @S1 @automated @web @mobile-web @mobile-app
    Scenario: I can navigate to the Password page
        When I click the <password> button
        Then I should be on the Password page
        Then I should see the Your password text field
        Then I should see the Back and Check button
