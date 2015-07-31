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
    // create random people entry name
    var personName = 'Test person ' + (Math.floor(Math.random() * 10001));

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
                return browser.isElementPresent(peoplePage.groupsLink);
            }, peoplePage.mainElementsWaitTime);

            peoplePage.groupsLink.click();

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

    it('creates a new people entry', function () {
        browser.wait(function () {
            return browser.isElementPresent(peoplePage.breadcrumbsLinks.first());
        }, peoplePage.mainElementsWaitTime);

        // click the Home link in breadcrumbs
        peoplePage.breadcrumbsLinks.first().click();

        browser.wait(function () {
            return browser.isElementPresent(peoplePage.addPersonButton);
        }, peoplePage.mainElementsWaitTime);

        peoplePage.addPersonButton.click();

        browser.wait(function () {
            return browser.isElementPresent(peoplePage.languageTabs.get(1));
        }, peoplePage.mainElementsWaitTime);

        // switch to English language tab
        peoplePage.languageTabs.get(1).click().then(function () {
            browser.wait(function () {
                return browser.isElementPresent(peoplePage.nameInput);
            }, peoplePage.mainElementsWaitTime);

            return peoplePage.nameInput.sendKeys(personName);
        }).then(function () {
            browser.wait(function () {
                return browser.isElementPresent(peoplePage.saveAndContinueButton);
            }, peoplePage.iframeWaitTime);

            browser.actions().mouseMove(peoplePage.saveAndContinueButton)
                .perform();
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
            // wait for person link to appear
            browser.wait(function () {
                return browser.isElementPresent(peoplePage.editPersonLinks.first());
            }, peoplePage.mainElementsWaitTime);

            // validate edit person link
            expect(peoplePage.editPersonLinks.first().isDisplayed())
                .toBeTruthy();
        });
    });

    it('adds a new people block on the page', function () {
        // go to the main page
        browser.get(peoplePage.site);

        browser.wait(function () {
            return browser.isElementPresent(peoplePage.testLink);
        }, peoplePage.mainElementsWaitTime);

        // add people to the page only if it was not added before
        peoplePage.aldrynPeopleBlock.isPresent().then(function (present) {
            if (present === false) {
                // click the Page link in the top menu
                return peoplePage.userMenus.get(1).click().then(function () {
                    // wait for top menu dropdown options to appear
                    browser.wait(function () {
                        return browser.isElementPresent(peoplePage.userMenuDropdown);
                    }, peoplePage.mainElementsWaitTime);

                    peoplePage.advancedSettingsOption.click();

                    // wait for modal iframe to appear
                    browser.wait(function () {
                        return browser.isElementPresent(peoplePage.modalIframe);
                    }, peoplePage.iframeWaitTime);

                    // switch to modal iframe
                    browser.switchTo().frame(browser.findElement(By.css(
                        '.cms_modal-frame iframe')));

                    // wait for Application select to appear
                    browser.wait(function () {
                        return browser.isElementPresent(peoplePage.applicationSelect);
                    }, peoplePage.mainElementsWaitTime);

                    // set Application
                    peoplePage.applicationSelect.click();
                    peoplePage.applicationSelect.sendKeys('People')
                        .then(function () {
                        peoplePage.applicationSelect.click();
                    });

                    // switch to default page content
                    browser.switchTo().defaultContent();

                    browser.wait(function () {
                        return browser.isElementPresent(peoplePage.saveModalButton);
                    }, peoplePage.mainElementsWaitTime);

                    browser.actions().mouseMove(peoplePage.saveModalButton)
                        .perform();
                    return peoplePage.saveModalButton.click();
                });
            }
        }).then(function () {
            // refresh the page to see changes
            browser.refresh();

            // wait for link to appear in aldryn people block
            browser.wait(function () {
                return browser.isElementPresent(peoplePage.peopleEntryLink);
            }, peoplePage.mainElementsWaitTime);

            peoplePage.peopleEntryLink.click();

            browser.wait(function () {
                return browser.isElementPresent(peoplePage.personTitle);
            }, peoplePage.mainElementsWaitTime);

            // validate person title
            expect(peoplePage.personTitle.isDisplayed()).toBeTruthy();
        });
    });

});
