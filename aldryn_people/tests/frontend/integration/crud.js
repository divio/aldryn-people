'use strict';

var helpers = require('djangocms-casper-helpers');
var globals = helpers.settings;
var casperjs = require('casper');
var cms = helpers(casperjs);

casper.test.setUp(function (done) {
    casper.start()
        .then(cms.login())
        .run(done);
});

casper.test.tearDown(function (done) {
    casper.start()
        .then(cms.logout())
        .run(done);
});

casper.test.begin('Test test', function (test) {
    casper
        .start(globals.adminUrl)
        .waitUntilVisible('#content', function () {
            test.assertVisible('#content', 'Admin loaded');
        })
        .run(function () {
            test.done();
        });
});
