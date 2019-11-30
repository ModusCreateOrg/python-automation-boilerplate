from pytest_bdd import when, parsers

from page_objects.home_page import HomePage


@when(parsers.re("I click the <(?P<button_type>.*)> button"), converters=dict(button_type=str))
def click_password_button(selenium, base_url, button_type):
    HomePage(selenium, base_url).click_button('_%s_button' % button_type)
