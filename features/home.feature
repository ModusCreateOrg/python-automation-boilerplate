@home_screen @nondestructive
Feature: innerText vs textContent
  As a tester
  I want to check the text displayed on the web page
  To be sure that what is displayed is what I want


  @s1 @automated @innerText
  Scenario: innerText value is what you see
    Given User navigates to "scripts/demo_app.html" homepage
    Then Element innerText is "MODUS CREATE"


  @s1 @automated @textContent
  Scenario: textContent value is not what you see
    Given User navigates to "scripts/demo_app.html" homepage
    Then Element textContent is "Modus Create"
    Then What user sees is "MODUS CREATE"
