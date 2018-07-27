# coding=utf-8
from selenium.webdriver.common.by import By


class GlobalLocators(object):
    back_arrow = (By.XPATH, '//ion-icon[@name="arrow-dropleft"]')
    back_button = (By.XPATH, '//ion-navbar/button[contains(@class, "back-button")]')
    next_arrow = (By.XPATH, '//ion-icon[@name="arrow-dropright"]')
    more_info_btn = (By.XPATH, '//*[contains(@class, "button-inner")]//*[@name="more"]/../..')
    alert_message = (By.CLASS_NAME, 'alert-message')
    button = (By.XPATH, '//button/*[contains(., "%s")]')
    navbar_button = (By.XPATH, '//a[contains(@class, "tab-button")]//ion-icon[@ng-reflect-name="%s"]/..')

    button_list = {
        'disagree': 'Disagree',
        'accept_terms': 'Accept Terms',
        'start_quitting': 'Start Quitting',
        'continue': 'Continue',
        'skip_this_step': 'I don\'t have a code, skip this step',
        'done': 'Done',
        'get_started': 'GET STARTED',
        'change_quit_day': 'CHANGE QUIT DAY',
        'lets_do_it': 'LETS DO IT',
        'create_my_account': 'CREATE MY ACCOUNT',
        'connect_with_facebook': 'CONNECT WITH FACEBOOK',
        'sign_in_with_facebook': 'SIGN IN WITH FACEBOOK',
        'sign_in_to_my_account': 'SIGN IN TO MY ACCOUNT',
        'sign_in': 'SIGN IN',
        'register': 'REGISTER',
        'go': 'GO',
        'add': 'Add',
        'set': 'Set',
        'reset': 'Reset',
        'not_right_now': 'Not Right Now',
        'cancel': 'Cancel',
        'ok': 'OK',
        'got_it': 'Got it!',
        'lets prepare': 'LET\'S PREPARE!'
    }

    footer_nav_list = {
        'quit_plan': 'quitplan',
        'quitspiration': 'quitspiration',
        'support': 'support',
    }


class WelcomeLocators(object):
    page_modal = (By.XPATH, '//page-welcome-screen-modal')
    page_logo = (By.CLASS_NAME, 'qc-logo')
    page_title = (By.XPATH, '//t-heading[@ng-reflect-text="Welcome to Quitter\'s Circle!"]')
    get_started_button = (By.XPATH, '//*[@class="button-inner"][contains(text(), "GET STARTED")]')

    # Images
    step_one_image = (By.XPATH, '//div/img[contains(@src, "understand-img.png")]')
    step_two_image = (By.XPATH, '//div/img[contains(@src, "prepare-img.png")]')
    step_three_image = (By.XPATH, '//div/img[contains(@src, "maintain-img.png")]')
