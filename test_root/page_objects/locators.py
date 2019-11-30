class ContextLocators:
    image = '//img[@alt="%s"]'
    title = '//ion-title'
    text_field_label = '//ion-label'


class ActionLocators:
    button = ContextLocators.image + '/parent::div'
    back_button = '//ion-back-button'
    check_button = '//ion-button[.="Check"]'
    link = '//a[contains(@href,"%s")]'
    text_field = '//input[@type="%s"]'
