/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global describe, it, browser, By, expect */

// #############################################################################
// INTEGRATION TEST
var peoplePage = require('../pages/page.people.crud.js');
var cmsProtractorHelper = require('cms-protractor-helper');

describe('Aldryn People tests: ', function () {
    // create random people entry name
    var personName = 'Test person ' + cmsProtractorHelper.randomDigits(4);

    it('logs in to the site with valid username and password', function () {
        // go to the main page
        browser.get(peoplePage.site);

        // check if the page already exists
        return peoplePage.testLink.isPresent().then(function (present) {
            if (present === true) {
                // go to the main page
                browser.get(peoplePage.site + '?edit');
            } else {
                // click edit mode link
                peoplePage.editModeLink.click();
            }

            // wait for username input to appear
            cmsProtractorHelper.waitFor(peoplePage.usernameInput);

            // login to the site
            peoplePage.cmsLogin();
        });
    });

    it('creates a new test page', function () {
        // click the example.com link in the top menu
        return peoplePage.userMenus.first().click().then(function () {
            // wait for top menu dropdown options to appear
            cmsProtractorHelper.waitFor(peoplePage.userMenuDropdown);

            return peoplePage.administrationOptions.first().click();
        }).then(function () {
            // wait for modal iframe to appear
            cmsProtractorHelper.waitFor(peoplePage.sideMenuIframe);

            // switch to sidebar menu iframe
            browser.switchTo().frame(browser.findElement(
                By.css('.cms_sideframe-frame iframe')));

            cmsProtractorHelper.waitFor(peoplePage.pagesLink);

            peoplePage.pagesLink.click();

            // wait for iframe side menu to reload
            cmsProtractorHelper.waitFor(peoplePage.addConfigsButton);

            // check if the page already exists and return the status
            return peoplePage.addPageLink.isPresent();
        }).then(function (present) {
            if (present === true) {
                // page is absent - create new page
                cmsProtractorHelper.waitFor(peoplePage.addPageLink);

                peoplePage.addPageLink.click();

                cmsProtractorHelper.waitFor(peoplePage.titleInput);

                return peoplePage.titleInput.sendKeys('Test').then(function () {
                    peoplePage.saveButton.click();

                    return peoplePage.slugErrorNotification.isPresent();
                }).then(function (present) {
                    if (present === false) {
                        cmsProtractorHelper.waitFor(peoplePage.editPageLink);

                        // wait till the editPageLink will become clickable
                        browser.sleep(500);

                        // validate/click edit page link
                        peoplePage.editPageLink.click();

                        // switch to default page content
                        browser.switchTo().defaultContent();

                        cmsProtractorHelper.waitFor(peoplePage.testLink);

                        // validate test link text
                        return peoplePage.testLink.getText().then(function (title) {
                            expect(title).toEqual('Test');
                        });
                    }
                });
            }
        });
    });

    it('creates a new group', function () {
        // check if the focus is on sidebar ifarme
        return peoplePage.editPageLink.isPresent().then(function (present) {
            if (present === false) {
                // wait for modal iframe to appear
                cmsProtractorHelper.waitFor(peoplePage.sideMenuIframe);

                // switch to sidebar menu iframe
                return browser.switchTo().frame(browser.findElement(By.css(
                    '.cms_sideframe-frame iframe')));
            }
        }).then(function () {
            cmsProtractorHelper.waitFor(peoplePage.breadcrumbsLinks.first());

            // click the Home link in breadcrumbs
            peoplePage.breadcrumbsLinks.first().click();

            cmsProtractorHelper.waitFor(peoplePage.groupsLink);

            peoplePage.groupsLink.click();

            // wait for iframe side menu to reload
            cmsProtractorHelper.waitFor(peoplePage.addConfigsButton);

            // check if the group already exists and return the status
            return peoplePage.editConfigsLink.isPresent();
        }).then(function (present) {
            if (present === false) {
                // group is absent - create new group
                cmsProtractorHelper.waitFor(peoplePage.addConfigsButton);

                peoplePage.addConfigsButton.click();

                cmsProtractorHelper.waitFor(peoplePage.englishLanguageTab);

                // switch to English language tab
                return peoplePage.englishLanguageTab.click().then(function () {
                    cmsProtractorHelper.waitFor(peoplePage.nameInput);

                    return peoplePage.nameInput.sendKeys('Test group');
                }).then(function () {
                    browser.actions().mouseMove(
                        peoplePage.saveAndContinueButton).perform();
                    peoplePage.saveButton.click();

                    // wait for page to get auto reloaded
                    browser.sleep(1000);

                    // wait for modal iframe to appear
                    cmsProtractorHelper.waitFor(peoplePage.sideMenuIframe);

                    // switch to sidebar menu iframe again as the page was reloaded
                    return browser.switchTo().frame(browser.findElement(By.css(
                        '.cms_sideframe-frame iframe')));
                }).then(function () {
                    // wait for group link to appear
                    cmsProtractorHelper.waitFor(peoplePage.editConfigsLink);

                    // validate group link
                    expect(peoplePage.editConfigsLink.isDisplayed())
                        .toBeTruthy();
                });
            }
        });
    });

    it('creates a new people entry', function () {
        cmsProtractorHelper.waitFor(peoplePage.breadcrumbsLinks.first());

        // click the Home link in breadcrumbs
        peoplePage.breadcrumbsLinks.first().click();

        cmsProtractorHelper.waitFor(peoplePage.addPersonButton);

        peoplePage.addPersonButton.click();

        cmsProtractorHelper.waitFor(peoplePage.englishLanguageTab);

        // switch to English language tab
        return peoplePage.englishLanguageTab.click().then(function () {
            cmsProtractorHelper.waitFor(peoplePage.nameInput);

            return peoplePage.nameInput.sendKeys(personName);
        }).then(function () {
            cmsProtractorHelper.waitFor(peoplePage.saveAndContinueButton);

            browser.actions().mouseMove(peoplePage.saveAndContinueButton)
                .perform();
            peoplePage.saveButton.click();

            // wait for page to get auto reloaded
            browser.sleep(1000);

            // wait for modal iframe to appear
            cmsProtractorHelper.waitFor(peoplePage.sideMenuIframe);

            // switch to sidebar menu iframe again as the page was reloaded
            return browser.switchTo().frame(browser.findElement(By.css(
                '.cms_sideframe-frame iframe')));
        }).then(function () {
            // wait for person link to appear
            cmsProtractorHelper.waitFor(peoplePage.editPersonLinks.first());

            // validate edit person link
            expect(peoplePage.editPersonLinks.first().isDisplayed())
                .toBeTruthy();
        });
    });

    it('adds a new people block on the page', function () {
        // go to the main page
        browser.get(peoplePage.site);

        cmsProtractorHelper.waitFor(peoplePage.testLink);

        // add people to the page only if it was not added before
        return peoplePage.aldrynPeopleBlock.isPresent().then(function (present) {
            if (present === false) {
                // click the Page link in the top menu
                return peoplePage.userMenus.get(1).click().then(function () {
                    // wait for top menu dropdown options to appear
                    cmsProtractorHelper.waitFor(peoplePage.userMenuDropdown);

                    peoplePage.advancedSettingsOption.click();

                    // wait for modal iframe to appear
                    cmsProtractorHelper.waitFor(peoplePage.modalIframe);

                    // switch to modal iframe
                    browser.switchTo().frame(browser.findElement(By.css(
                        '.cms_modal-frame iframe')));

                    // set People Application
                    cmsProtractorHelper.selectOption(peoplePage.applicationSelect,
                        'People', peoplePage.peopleOption);

                    // switch to default page content
                    browser.switchTo().defaultContent();

                    cmsProtractorHelper.waitFor(peoplePage.saveModalButton);

                    browser.actions().mouseMove(peoplePage.saveModalButton)
                        .perform();
                    return peoplePage.saveModalButton.click();
                });
            }
        }).then(function () {
            // refresh the page to see changes
            browser.refresh();

            // wait for link to appear in aldryn people block
            cmsProtractorHelper.waitFor(peoplePage.peopleEntryLink);

            peoplePage.peopleEntryLink.click();

            cmsProtractorHelper.waitFor(peoplePage.personTitle);

            // validate person title
            expect(peoplePage.personTitle.isDisplayed()).toBeTruthy();
        });
    });

    it('deletes people entry', function () {
        // wait for modal iframe to appear
        cmsProtractorHelper.waitFor(peoplePage.sideMenuIframe);

        // switch to sidebar menu iframe
        browser.switchTo()
            .frame(browser.findElement(By.css('.cms_sideframe-frame iframe')));

        // wait for edit people entry link to appear
        cmsProtractorHelper.waitFor(peoplePage.editPersonLinks.first());

        // validate edit people entry links texts to delete proper people entry
        return peoplePage.editPersonLinks.first().getText().then(function (text) {
            // wait till horizontal scrollbar will disappear and
            // editPersonLinks will become clickable
            browser.sleep(1500);

            if (text === personName) {
                return peoplePage.editPersonLinks.first().click();
            } else {
                return peoplePage.editPersonLinks.get(1).getText()
                    .then(function (text) {
                    if (text === personName) {
                        return peoplePage.editPersonLinks.get(1).click();
                    } else {
                        return peoplePage.editPersonLinks.get(2).getText()
                            .then(function (text) {
                            if (text === personName) {
                                return peoplePage.editPersonLinks.get(2).click();
                            }
                        });
                    }
                });
            }
        }).then(function () {
            // wait for delete button to appear
            cmsProtractorHelper.waitFor(peoplePage.deleteButton);

            browser.actions().mouseMove(peoplePage.saveAndContinueButton)
                .perform();
            return peoplePage.deleteButton.click();
        }).then(function () {
            // wait for confirmation button to appear
            cmsProtractorHelper.waitFor(peoplePage.sidebarConfirmationButton);

            peoplePage.sidebarConfirmationButton.click();

            cmsProtractorHelper.waitFor(peoplePage.successNotification);

            // validate success notification
            expect(peoplePage.successNotification.isDisplayed()).toBeTruthy();

            // switch to default page content
            browser.switchTo().defaultContent();

            // refresh the page to see changes
            browser.refresh();
        });
    });

});
