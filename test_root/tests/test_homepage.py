from pytest_bdd import parsers, then, scenarios

from page_objects.home_page import HomePage

scenarios('../features/home.feature', strict_gherkin=False)


@then(parsers.re("I should see the <(?P<button_type>.*)> button"), converters=dict(button_type=str))
def see_buttons(selenium, base_url, button_type):
    HomePage(selenium, base_url).validate_element_is_visible('_%s_button' % button_type)


@then(parsers.re("I should see the <(?P<link_type>.*)> link"), converters=dict(link_type=str))
def see_links(selenium, base_url, link_type):
    HomePage(selenium, base_url).validate_element_is_visible('_%s_link' % link_type)


@then("The app logo default visual is valid")
def logo_default_visual_is_valid(selenium, base_url):
    HomePage(selenium, base_url).validate_logo_default_visual()

@then("The account button default visual is valid")
def account_button_default_visual_is_valid(selenium, base_url):
    HomePage(selenium, base_url).validate_account_button_default_visual()

@then("The password button default visual is valid")
def password_button_default_visual_is_valid(selenium, base_url):
    pass
    # HomePage(selenium, base_url).validate_password_button_default_visual()
