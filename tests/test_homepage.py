from pytest_bdd import scenarios, then, parsers

from page_objects.home_page import HomePage

scenarios('../features/home.feature', strict_gherkin=False)


@then(parsers.re('What user sees is "(?P<text>.*)" from "(?P<method>.*)"'), converters=dict(text=str,method=str))
def what_user_sees(selenium,base_url, variables, text, method):
    HomePage(selenium,base_url, variables['en']).what_user_sees(text, method)


@then(parsers.re('Element text is "(?P<text>.*)"'), converters=dict(text=str))
def text_validation(selenium, base_url, variables, text):
    HomePage(selenium, base_url, variables['en']).text_validation(text)


@then(parsers.re('Element innerText is "(?P<text>.*)"'), converters=dict(text=str))
def inner_text_validation(selenium, base_url, variables, text):
    HomePage(selenium, base_url, variables['en']).inner_text_validation(text)


@then(parsers.re('Element textContent is "(?P<text>.*)"'), converters=dict(text=str))
def text_content_validation(selenium, base_url, variables, text):
    HomePage(selenium, base_url, variables['en']).text_content_validation(text)
