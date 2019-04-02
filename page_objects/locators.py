

class HomePageLocators:
    __parent = '//ion-page'
    __parent_app_stores = '%s//div[@class="app-store-btns"]' % __parent
    __parent_content = '%s//ion-content' % __parent
    __parent_dialog = '%s//div[@role="dialog"]' % __parent
    __parent_footer = '%s//div[@class="footer"]' % __parent
    __parent_header = '%s//ion-header' % __parent
    app_logo = '%s//img[@src="/img/Beep-Logo.e5d20974.svg"]' % __parent_header
    app_store_link_android = '%s//a[@href="https://mdus.co/beepandroid"]' % __parent_app_stores
    app_store_link_ios = '%s//a[@href="https://mdus.co/beepios"]' % __parent_app_stores
    app_title = '%s//h1' % __parent_content
    button = '%s//div[@class="square-btn"][.="%s"]' % (__parent_content, '%s')
    dialog_close_button = '%s//ion-icon[@name="close"]/parent::ion-button' % __parent_dialog
    dialog_done_button = '%s//ion-button[contains(.,"Done"]' % __parent_dialog
    dialog_paragraph = '%s//p' % __parent_dialog
    footer_link = '%s//h2' % __parent_footer
