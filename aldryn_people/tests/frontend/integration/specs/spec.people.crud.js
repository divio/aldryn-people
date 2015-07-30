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
    it('opens the main page', function () {
        // go to the main page
        browser.get(peoplePage.site);
    });

});
