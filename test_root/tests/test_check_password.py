from pytest_bdd import then, scenarios

from page_objects.password_page import PasswordPage

scenarios('../features/check_password.feature', strict_gherkin=False)


@then("I should be on the Password page")
def should_be_on_password_page(selenium, base_url):
    PasswordPage(selenium, base_url).is_loaded()


@then("I should see the Your password text field")
def should_see_password_text_field(selenium, base_url):
    PasswordPage(selenium, base_url).validate_text_field()


@then("I should see the Back and Check button")
def should_see_back_and_check_button(selenium, base_url):
    PasswordPage(selenium, base_url).validate_action_buttons()
