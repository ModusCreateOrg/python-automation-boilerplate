from pytest_bdd import given

from page_objects.home_page import HomePage


@given("User navigates to Beep homepage")
def navigate_to_homepage(selenium, base_url, variables):
    if ('orig_os' in selenium.desired_capabilities and selenium.desired_capabilities['orig_os'] != 'ios') \
            or 'orig_os' not in selenium.desired_capabilities:
        selenium.maximize_window()
    HomePage(selenium, base_url, variables['en']).open()
