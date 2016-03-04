/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global browser, by, element, expect */

// #############################################################################
// INTEGRATION TEST PAGE OBJECT

var page = {
    site: 'http://127.0.0.1:8000/en/',

    // log in
    editModeLink: element(by.css('.inner a[href="/?edit"]')),
    usernameInput: element(by.id('id_username')),
    passwordInput: element(by.id('id_password')),
    loginButton: element(by.css('input[type="submit"]')),
    userMenus: element.all(by.css('.cms-toolbar-item-navigation > li > a')),

    // adding new page
    modalCloseButton: element(by.css('.cms-modal-close')),
    userMenuDropdown: element(by.css(
        '.cms-toolbar-item-navigation-hover')),
    administrationOptions: element.all(by.css(
        '.cms-toolbar-item-navigation a[href="/en/admin/"]')),
    sideMenuIframe: element(by.css('.cms-sideframe-frame iframe')),
    pagesLink: element(by.css('.model-page > th > a')),
    addConfigsButton: element(by.css('.object-tools .addlink')),
    addPageLink: element(by.css('.object-tools .addlink')),
    titleInput: element(by.id('id_title')),
    slugErrorNotification: element(by.css('.errors.slug')),
    saveButton: element(by.css('.submit-row [name="_save"]')),
    editPageLink: element(by.css('.cms-tree-item-preview [href*="preview/"]')),
    testLink: element(by.cssContainingText('a', 'Test')),
    sideFrameClose: element(by.css('.cms-sideframe-close')),

    // adding new group
    breadcrumbs: element(by.css('.breadcrumbs')),
    breadcrumbsLinks: element.all(by.css('.breadcrumbs a')),
    groupsLink: element(by.css(
        '.model-group > th > [href*="/aldryn_people/group/"]')),
    editConfigsLink: element(by.css('.results th > a')),
    englishLanguageTab: element(by.css(
        '.parler-language-tabs > .empty > a[href*="language=en"]')),
    nameInput: element(by.id('id_name')),
    saveAndContinueButton: element(by.css('.submit-row [name="_continue"]')),
    successNotification: element(by.css('.messagelist .success')),

    // adding new people entry
    addPersonButton: element(by.css('.model-person .addlink')),
    editPersonButton: element(by.css('.model-person .changelink')),
    editPersonLinksTable: element(by.css('.results')),
    editPersonLinks: element.all(by.css(
        '.results th > [href*="/aldryn_people/person/"]')),

    // adding people block to the page
    aldrynPeopleBlock: element(by.css('.aldryn-people')),
    advancedSettingsOption: element(by.css(
        '.cms-toolbar-item-navigation [href*="advanced-settings"]')),
    modalIframe: element(by.css('.cms-modal-frame iframe')),
    applicationSelect: element(by.id('application_urls')),
    peopleOption: element(by.css('option[value="PeopleApp"]')),
    saveModalButton: element(by.css('.cms-modal-buttons .cms-btn-action')),
    peopleEntryLink: element(by.css('.aldryn-people-article > h2 > a')),
    personTitle: element(by.css('.aldryn-people-detail h2 > div')),

    // deleting people entry
    deleteButton: element(by.css('.deletelink-box a')),
    sidebarConfirmationButton: element(by.css('#content [type="submit"]')),

    cmsLogin: function (credentials) {
        // object can contain username and password, if not set it will
        // fallback to 'admin'
        credentials = credentials ||
            { username: 'admin', password: 'admin' };

        page.usernameInput.clear();

        // fill in email field
        page.usernameInput.sendKeys(
            credentials.username).then(function () {
            page.passwordInput.clear();

            // fill in password field
            return page.passwordInput.sendKeys(
                credentials.password);
        }).then(function () {
            return page.loginButton.click();
        }).then(function () {
            // this is required for django1.6, because it doesn't redirect
            // correctly from admin
            browser.get(page.site);

            // wait for user menu to appear
            browser.wait(browser.isElementPresent(
                page.userMenus.first()),
                page.mainElementsWaitTime);

            // validate user menu
            expect(page.userMenus.first().isDisplayed())
                .toBeTruthy();
        });
    }

};

module.exports = page;
