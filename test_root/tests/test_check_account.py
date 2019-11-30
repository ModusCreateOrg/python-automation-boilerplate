from pytest_bdd import then, scenarios

from page_objects.account_page import AccountPage

scenarios('../features/check_account.feature', strict_gherkin=False)


@then("I should be on the Account page")
def should_be_on_account_page(selenium, base_url):
    AccountPage(selenium, base_url).is_loaded()


@then("I should see the Your username or email text field")
def should_see_email_text_field(selenium, base_url):
    AccountPage(selenium, base_url).validate_text_field()


@then("I should see the Back and Check button")
def should_see_back_and_check_button(selenium, base_url):
    AccountPage(selenium, base_url).validate_action_buttons()
