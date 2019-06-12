# pylint: disable=line-too-long


class CommonLocators:

    def __init__(self):
        self.parent = '//ion-page'
        self.header = '%s//ion-header' % self.parent
        self.content = '%s//ion-content' % self.parent
        self.content_title = '%s//h1' % self.content


class HomePageLocators(CommonLocators):

    def __init__(self):
        super().__init__()
        self.header_logo = '%s//img' % self.header
        self.account_button = '(%s//div[@class="square-btn"])[position()=%s]' % (self.content, 1)
        self.password_button = '(%s//div[@class="square-btn"])[position()=%s]' % (self.content, 2)
        self.footer = '%s//div[@class="footer"]' % self.content
        self.footer_title = '%s//h2' % self.footer
        self.footer_link = '%s//span' % self.footer
        self.app_store_btn_ios = '(%s//div[@class="app-store-btns"]/a)[position()=%s]' % (self.content, 1)
        self.app_store_btn_android = '(%s//div[@class="app-store-btns"]/a)[position()=%s]' % (self.content, 2)


class AccountPageLocators(CommonLocators):

    def __init__(self):
        super().__init__()
        self.back_button = '%s//ion-back-button' % self.header
        self.title = '%s//ion-title' % self.header
        self.check_button = '%s//ion-button[.="%s"]' % (self.header, '%s')
        self.email_field_label = '%s//ion-label' % self.content
        self.email_field_input = '%s//ion-input' % self.content
        self.email_field_input_placeholder = '%s//input' % self.email_field_input
