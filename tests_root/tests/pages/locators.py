from selenium.webdriver.common.by import By


class GlobalLocators(object):
    back_button = (By.XPATH, '//ion-navbar/button[contains(@class, "back-button")]')
    next_button = (By.XPATH, '//ion-navbar/button[contains(@class, "next-button")]')
    alert_message = (By.CLASS_NAME, 'alert-message')
    button = (By.XPATH, '//button/*[contains(., "%s")]')

    button_list = {
        'disagree': 'Disagree',
        'continue': 'Continue',
        'done': 'Done'
    }


class WelcomeLocators(object):
    page_logo = (By.CLASS_NAME, 'logo')
    page_title = (By.XPATH, '//t-heading[@ng-reflect-text="Welcome"]')
    get_started_button = (By.XPATH, '//*[@class="button-inner"][contains(text(), "GET STARTED")]')
