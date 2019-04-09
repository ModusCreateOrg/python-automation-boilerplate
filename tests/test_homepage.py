from pytest_bdd import scenarios, then, parsers

from page_objects.home_page import HomePage

scenarios('../features/home.feature', strict_gherkin=False)


@then(parsers.re('What user sees is "(?P<text>(.*)+)"'))
@then(parsers.re('Page innerText is "(?P<text>(.*)+)"'))
def inner_text_validation(selenium, base_url, variables, text):
    HomePage(selenium, base_url, variables['en']).inner_text_validation(text)


@then(parsers.re('Page textContent is "(?P<text>(.*)+)"'))
def text_content_validation(selenium, base_url, variables, text):
    HomePage(selenium, base_url, variables['en']).text_content_validation(text)
