# pylint: disable=line-too-long
# pylint: disable=no-member

from pytest_bdd import scenarios, then

from page_objects.account_page import AccountPage

scenarios('../features/homepage.feature'
          , strict_gherkin=False)


@then('"Account" loads successfully')
def account_loads_successfully(selenium, base_url):
    AccountPage(selenium).is_loaded()


@then('"Password" loads successfully')
def password_loads_successfully():
    raise NotImplementedError(u'STEP: Then "Password" loads successfully')
