@account_screen @nondestructive
Feature: Account screen of Beep web app
    As a user of Beep web app
    I want to be able to provide my username on the Account page
    So that I know if my account data has been compromised


    Background:
        Given I load the Beep app

    @S1 @automated @web @mobile-web @mobile-app
    Scenario: I can navigate to the Account page
        When I click the <account> button
        Then I should be on the Account page
        Then I should see the Your username or email text field
        Then I should see the Back and Check button

    @S2 @manual
    Scenario: Functionality of "Your username or email" text box
        Given I am on https://beep.modus.app/#/acc Page
        When I tap  inside "Your username or email" text box
        Then I should see a cursor
        Then I should be able to type

    @S3 @manual
    Scenario: Acceptance of data by"Your username or email" text box
        Given I am on https://beep.modus.app/acc Page
        When I tap  inside "Your username or email" text box
        Then I should be able to add User name
        Then I should be able to add Email ID

    @S4.1 @manual
    Scenario: Activation of "Check" option
        Given I am on "https://beep.modus.app"
        Given I click on "Account field"
        When User should see "check" option
        Then I should be on https://beep.modus.app/acc Page
        Then I should see deactivated "Check" option

    @S4.2 @manual
    Scenario: Activation of "Check" option
        Given I am on https://beep.modus.app/#/acc Page
        When I tap  inside "Your username or email" text box
        When I don't type anything in "Your username or email" text box
        Then I should see deactivated "Check" option

    @S4.3 @manual
    Scenario: Activation of "Check" option
        Given I am on https://beep.modus.app/#/acc Page
        When I tap  inside "Your username or email" text box
        When I add spaces in  "Your username or email" text box
        Then I should see deactivated "Check" option


    @S4.4 @manual
    Scenario: Action when click on deactivated "Check" option
        Given I am on https://beep.modus.app/#/acc Page
        When I tap  inside "Your username or email" text box
        When I add spaces in  "Your username or email" text box
        Then I see deactivated "Check" option
        Then I click on "Check" Option
        Then I should "Check" option deactivated only
        Then I should see no validation and change for "Your username or email" text box

    @S4.5 @manual
    Scenario: Action when click on deactivated "Check" option
        Given I am on https://beep.modus.app/#/acc Page
        When I tap  inside "Your username or email" text box
        Then I see deactivated "Check" option
        Then I click on "Check" Option
        Then I should "Check" option deactivated only
        Then I should see no validation and change for "Your username or email" text box

    @S5.1 @manual
    Scenario: Verification of a non hacked Email ID
        Given I am on https://beep.modus.app/#/acc Page
        When I tap  inside "Your username or email" text box
        When User enters a non hacked Email ID
        When I click on "Check" Option
        Then I should redirects to "https://beep.modus.app/#/safe" Page
        Then I should see "Congratulations! Your account has not been compromised" message

    @S5.2 @manual
    Scenario: Verification of a non hacked Username
        Given I am on https://beep.modus.app/#/acc Page
        When I tap  inside "Your username or email" text box
        When User enters a non hacked Username
        When I click on "Check" Option
        Then I should redirects to "https://beep.modus.app/#/safe" Page
        Then I should see "Congratulations! Your account has not been compromised" message

    @S5.3 @manual
    Scenario: Verification of a hacked Email ID
        Given I am on https://beep.modus.app/#/acc Page
        When I tap  inside "Your username or email" text box
        When User enters a non hacked Email ID
        When I click on "Check" Option
        Then I should redirects to "https://beep.modus.app/#/breaches" Page
        Then I should display of websites from where it had been hacked

    @S5.4 @manual
    Scenario: Verification of a hacked Username
        Given I am on https://beep.modus.app/#/acc Page
        When I tap  inside "Your username or email" text box
        When User enters a non hacked Username
        When I click on "Check" Option
        Then I should redirects to "https://beep.modus.app/#/breaches" Page
        Then I should display of websites from where it had been hacked

    @S5.5 @manual
    Scenario: Verification of a invalid Email ID or Username
        Given I am on https://beep.modus.app/#/acc Page
        When I tap  inside "Your username or email" text box
        When User enters a invalid Username or Email ID
        Then I should see a validation message

    @S6 @manual
    Scenario: Verification on "back" button from Acc. Page
        Given I am on "https://beep.modus.app" Page
        When User click on left back button
        Then I should redirects to Home screen 'https://beep.modus.app/#/" Page
