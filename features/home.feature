@home_screen @nondestructive
Feature: innerText vs textContent
  As a tester
  I want to check the text displayed on the web page
  To be sure that what is displayed is what I want


  @s1 @automated @chrome
  Scenario: text, innerText and textContent on Chrome
    Given User navigates to homepage
    Then Element text is "MODUS CREATE"
    Then Element innerText is "MODUS CREATE"
    Then Element textContent is "Modus Create"
    Then What user sees is "MODUS CREATE" from "text"
    Then What user sees is "MODUS CREATE" from "get_property('innerText')"


  @s1 @automated @edge
  Scenario: text, innerText and textContent on Edge
    Given User navigates to homepage
    Then Element text is "MODUS CREATE"
    Then Element innerText is "Modus Create"
    Then Element textContent is "Modus Create"
    Then What user sees is "MODUS CREATE" from "text"


  @s1 @automated @firefox
  Scenario: text, innerText and textContent on Firefox
    Given User navigates to homepage
    Then Element text is "MODUS CREATE"
    Then Element innerText is "MODUS CREATE"
    Then Element textContent is "Modus Create"
    Then What user sees is "MODUS CREATE" from "text"
    Then What user sees is "MODUS CREATE" from "get_property('innerText')"


  @s1 @automated @ie
  Scenario: text, innerText and textContent on Internet Explorer
    Given User navigates to homepage
    Then Element text is "MODUS CREATE"
    Then Element innerText is "Modus Create"
    Then Element textContent is "Modus Create"
    Then What user sees is "MODUS CREATE" from "text"


  @s1 @automated @safari
  Scenario: text, innerText and textContent on Safari
    Given User navigates to homepage
    Then Element text is "Modus Create"
    Then Element innerText is "MODUS CREATE"
    Then Element textContent is "Modus Create"
    Then What user sees is "MODUS CREATE" from "get_property('innerText')"
