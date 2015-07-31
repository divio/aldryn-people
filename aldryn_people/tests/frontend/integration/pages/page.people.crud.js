/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global element, by, browser, expect */

// #############################################################################
// INTEGRATION TEST PAGE OBJECT

var peoplePage = {
    site: 'http://127.0.0.1:8000/en/',
    mainElementsWaitTime: 12000,
    iframeWaitTime: 15000,

    // log in
    editModeLink: element(by.css('.inner a[href="/?edit"]')),
    usernameInput: element(by.id('id_cms-username')),
    passwordInput: element(by.id('id_cms-password')),
    loginButton: element(by.css('.cms_form-login input[type="submit"]')),
    userMenus: element.all(by.css('.cms_toolbar-item-navigation > li > a')),
    testLink: element(by.css('.selected a')),

    // adding new page
    userMenuDropdown: element(by.css(
        '.cms_toolbar-item-navigation-hover')),
    administrationOptions: element.all(by.css(
        '.cms_toolbar-item-navigation a[href="/en/admin/"]')),
    sideMenuIframe: element(by.css('.cms_sideframe-frame iframe')),
    pagesLink: element(by.css('.model-page > th > a')),
    addConfigsButton: element(by.css('.object-tools .addlink')),
    addPageLink: element(by.css('.sitemap-noentry .addlink')),
    titleInput: element(by.id('id_title')),
    slugErrorNotification: element(by.css('.errors.slug')),
    saveButton: element(by.css('.submit-row [name="_save"]')),
    editPageLink: element(by.css('.col1 [href*="preview/"]')),

    // adding new group
    breadcrumbsLinks: element.all(by.css('.breadcrumbs a')),
    groupsLink: element(by.css(
        '.model-group > th > [href*="/aldryn_people/group/"]')),
    editConfigsLink: element(by.css('.results th > a')),
    languageTabs: element.all(by.css('.parler-language-tabs > .empty > a')),
    nameInput: element(by.id('id_name')),
    saveAndContinueButton: element(by.css('.submit-row [name="_continue"]')),
    successNotification: element(by.css('.messagelist .success')),

    // adding new people entry
    addPersonButton: element(by.css('.model-person .addlink')),
    editPersonLinks: element.all(by.css(
        '.results th > [href*="/aldryn_people/person/"]')),

    cmsLogin: function (credentials) {
        // object can contain username and password, if not set it will
        // fallback to 'admin'
        credentials = credentials ||
            { username: 'admin', password: 'admin' };

        peoplePage.usernameInput.clear();

        // fill in email field
        peoplePage.usernameInput.sendKeys(
            credentials.username).then(function () {
            peoplePage.passwordInput.clear();

            // fill in password field
            return peoplePage.passwordInput.sendKeys(
                credentials.password);
        }).then(function () {
            peoplePage.loginButton.click();

            // wait for user menu to appear
            browser.wait(browser.isElementPresent(
                peoplePage.userMenus.first()),
                peoplePage.mainElementsWaitTime);

            // validate user menu
            expect(peoplePage.userMenus.first().isDisplayed())
                .toBeTruthy();
        });
    }

};

module.exports = peoplePage;
