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

    it('creates a new group', function () {
        // check if the focus is on sidebar ifarme
        peoplePage.editPageLink.isPresent().then(function (present) {
            if (present === false) {
                // wait for modal iframe to appear
                browser.wait(function () {
                    return browser.isElementPresent(peoplePage.sideMenuIframe);
                }, peoplePage.iframeWaitTime);

                // switch to sidebar menu iframe
                return browser.switchTo().frame(browser.findElement(By.css(
                    '.cms_sideframe-frame iframe')));
            }
        }).then(function () {
            browser.wait(function () {
                return browser.isElementPresent(peoplePage.breadcrumbsLinks.first());
            }, peoplePage.mainElementsWaitTime);

            // click the Home link in breadcrumbs
            peoplePage.breadcrumbsLinks.first().click();

            browser.wait(function () {
                return browser.isElementPresent(peoplePage.groupsLinks.first());
            }, peoplePage.mainElementsWaitTime);

            peoplePage.groupsLinks.first().click();

            // wait for iframe side menu to reload
            browser.wait(function () {
                return browser.isElementPresent(peoplePage.addConfigsButton);
            }, peoplePage.mainElementsWaitTime);

            // check if the group already exists and return the status
            return peoplePage.editConfigsLink.isPresent();
        }).then(function (present) {
            if (present === false) {
                // group is absent - create new group
                browser.wait(function () {
                    return browser.isElementPresent(peoplePage.addConfigsButton);
                }, peoplePage.mainElementsWaitTime);

                peoplePage.addConfigsButton.click();

                browser.wait(function () {
                    return browser.isElementPresent(peoplePage.languageTabs.get(1));
                }, peoplePage.mainElementsWaitTime);

                // switch to English language tab
                peoplePage.languageTabs.get(1).click().then(function () {
                    browser.wait(function () {
                        return browser.isElementPresent(peoplePage.nameInput);
                    }, peoplePage.mainElementsWaitTime);

                    return peoplePage.nameInput.sendKeys('Test group');
                }).then(function () {
                    browser.actions().mouseMove(
                        peoplePage.saveAndContinueButton).perform();
                    peoplePage.saveButton.click();

                    // wait for page to get auto reloaded
                    browser.sleep(1000);

                    // wait for modal iframe to appear
                    browser.wait(function () {
                        return browser.isElementPresent(peoplePage.sideMenuIframe);
                    }, peoplePage.iframeWaitTime);

                    // switch to sidebar menu iframe again as the page was reloaded
                    return browser.switchTo().frame(browser.findElement(By.css('.cms_sideframe-frame iframe')));
                }).then(function () {
                      // wait for group link to appear
                    browser.wait(function () {
                        return browser.isElementPresent(peoplePage.editConfigsLink);
                    }, peoplePage.mainElementsWaitTime);

                    // validate group link
                    expect(peoplePage.editConfigsLink.isDisplayed())
                        .toBeTruthy();
                });
            }
        });
    });

});
