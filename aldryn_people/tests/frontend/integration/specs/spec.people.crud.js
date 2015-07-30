/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global describe, it, browser, By, expect */

// #############################################################################
// INTEGRATION TEST
var peoplePage = require('../pages/page.people.crud.js');

describe('Aldryn People tests: ', function () {
    it('logs in to the site with valid username and password', function () {
        // go to the main page
        browser.get(peoplePage.site);

        // check if the page already exists
        peoplePage.testLink.isPresent().then(function (present) {
            if (present === true) {
                // go to the main page
                browser.get(peoplePage.site + '?edit');
            } else {
                // click edit mode link
                peoplePage.editModeLink.click();
            }

            // wait for username input to appear
            browser.wait(function () {
                return browser.isElementPresent(peoplePage.usernameInput);
            }, peoplePage.mainElementsWaitTime);

            // login to the site
            peoplePage.cmsLogin();
        });
    });

    it('creates a new test page', function () {
        // click the example.com link in the top menu
        peoplePage.userMenus.first().click().then(function () {
            // wait for top menu dropdown options to appear
            browser.wait(function () {
                return browser.isElementPresent(peoplePage.userMenuDropdown);
            }, peoplePage.mainElementsWaitTime);

            return peoplePage.administrationOptions.first().click();
        }).then(function () {
            // wait for modal iframe to appear
            browser.wait(function () {
                return browser.isElementPresent(peoplePage.sideMenuIframe);
            }, peoplePage.iframeWaitTime);

            // switch to sidebar menu iframe
            browser.switchTo().frame(browser.findElement(
                By.css('.cms_sideframe-frame iframe')));

            browser.wait(function () {
                return browser.isElementPresent(peoplePage.pagesLink);
            }, peoplePage.mainElementsWaitTime);

            peoplePage.pagesLink.click();

            // wait for iframe side menu to reload
            browser.wait(function () {
                return browser.isElementPresent(peoplePage.addConfigsButton);
            }, peoplePage.mainElementsWaitTime);

            // check if the page already exists and return the status
            return peoplePage.addPageLink.isPresent();
        }).then(function (present) {
            if (present === true) {
                // page is absent - create new page
                browser.wait(function () {
                    return browser.isElementPresent(peoplePage.addPageLink);
                }, peoplePage.mainElementsWaitTime);

                peoplePage.addPageLink.click();

                browser.wait(function () {
                    return browser.isElementPresent(peoplePage.titleInput);
                }, peoplePage.mainElementsWaitTime);

                peoplePage.titleInput.sendKeys('Test').then(function () {
                    peoplePage.saveButton.click();

                    return peoplePage.slugErrorNotification.isPresent();
                }).then(function (present) {
                    if (present === false) {
                        browser.wait(function () {
                            return browser.isElementPresent(peoplePage.editPageLink);
                        }, peoplePage.mainElementsWaitTime);

                        // wait till the editPageLink will become clickable
                        browser.sleep(500);

                        // validate/click edit page link
                        peoplePage.editPageLink.click();

                        // switch to default page content
                        browser.switchTo().defaultContent();

                        browser.wait(function () {
                            return browser.isElementPresent(peoplePage.testLink);
                        }, peoplePage.mainElementsWaitTime);

                        // validate test link text
                        peoplePage.testLink.getText().then(function (title) {
                            expect(title).toEqual('Test');
                        });
                    }
                });
            }
        });
    });

});
