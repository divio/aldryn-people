/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global describe, it, browser */

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

});
