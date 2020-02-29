from pytest_bdd import then

from page_objects.home_page import HomePage


@then("I should see app logo")
def see_app_logo(selenium, base_url):
    HomePage(selenium, base_url).validate_element_is_visible('_logo')
