from pytest_bdd import scenarios, then

from page_objects.home_page import HomePage

scenarios('../features/home.feature', strict_gherkin=False)


@then("Beep logo is visible")
def logo_visible(selenium, base_url, variables):
    HomePage(selenium, base_url, variables['en']).logo_visible()


@then("Beep title is visible")
def title_visible(selenium, base_url, variables):
    HomePage(selenium, base_url, variables['en']).title_visible()


@then("Beep stores links are visible")
def stores_links_visible(selenium, base_url, variables):
    HomePage(selenium, base_url, variables['en']).store_links_visible()


@then("Homepage content is loaded")
def homepage_content_loaded(selenium, base_url, variables):
    HomePage(selenium, base_url, variables['en']).is_loaded()
