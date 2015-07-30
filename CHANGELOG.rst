CHANGELOG
=========

1.0.0 (2015-07-29)
------------------

* Adds revisioning
* Names (and slugs) are now translatable
* Groups are now sortable
* Users are presented alphabetically
* New option to show ungrouped people in people plugin
* New groups list view
* Adds CMS Toolbar "people" when on Aldryn People views
* Numerous other UI/UX improvements
* Adds documentation
* Adds Django 1.8.x and django CMS 3.1.x support
* Adds configuration for frontend testing

0.5.3 (2015-07-08)
------------------

* Added another missing django >= 1.7 migration
* Fixed integrity error on automatic slug generation

0.5.2 (2015-04-25)
------------------

* Added missing django >= 1.7 migration
* Dropped support for django 1.4 & 1.5
* Updated requirements to require aldryn-common>=0.1.3

0.5.1 (2015-04-16)
------------------

* Use get_current_language from cms instead get_language from Django because Django bug #9340
