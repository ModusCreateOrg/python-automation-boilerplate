from pytest_bdd import given, when

from test_root.page_objects.home_page import HomePage


@given('Beep app Homepage loads successfully')
def homepage_loads_successfully(selenium):
    selenium.switch_to_webview_context()

    HomePage(selenium).is_loaded()


@given('User clicks on "account" button')
def click_on_account(selenium):
    HomePage(selenium).go_to_account()


@given('User clicks on "password" button')
def click_on_password(selenium):
    HomePage(selenium).go_to_password()
