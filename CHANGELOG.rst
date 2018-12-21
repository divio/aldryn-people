Changelog
=========

2.2.0 (2018-12-21)
==================

* Added support for Django 2.0 and 2.1
* Removed support for Django < 1.11
* Adapted testing infrastructure (tox/travis) to incorporate django CMS 3.6


2.1.0 (2018-01-30)
==================

* Added Django 1.11 support


2.0.0 (2018-01-17)
==================

* Introduced django CMS 3.5 support
* Dropped aldryn-reversion/django-reversion support
* Dropped Django 1.6 and 1.7 support
* Added Django 1.10 support


1.2.2 (2016-09-05)
==================

* Updated translations
* Fixed related_name inconsistency with django CMS 3.3.1
* Dropped support for djangoCMS < 3.2
* Introduced support for djangoCMS 3.4.0


1.2.1 (2016-05-17)
==================

* Changed name and slug fields in admin to full width
* Added support for Django Reversion v1.10+
* Added support and test coverage for Python 3.5
* Added support and test coverage for Django v1.9
* Added support and test coverage for django CMS v3.3
* Updated testing tools and matrices


1.2.0 (2016-03-10)
==================

* Removed unused render_placeholder configs
* Added static_placeholders where necessary
* Simplify templates


1.1.6 (2016-02-11)
==================

* Added Django 1.9 compatibility
* Added stripped default django templates to `/aldryn_people/templates`


1.1.5 (2016-01-12)
==================

* Improved compatibility with recent versions of django-reversion
* Added integration tests against CMS 3.2


1.1.4 (2016-01-09)
==================

* Added support for reversion for wizards
* Cleanup and update test configuration
* Added missing migrations


1.1.3 (2015-11-10)
==================

* Removed visual from wizard form


1.1.2 (2015-11-10)
==================

* Prevents (benign) JS errors on console.
* Better handle cases where there is no apphook present/published
* Disabled the Group wizard (too infrequently used)


1.1.1 (2015-11-03)
==================

* Relax Filer requirement restriction to allow v1.0+


1.1.0 (2015-10-31)
==================

* Reimplements vCard downloads in a Py3 compatible way (Thanks, Adam Brenecki!)
* Solved an issue where "Menus could not be loaded" messages were occurring in
  certain situations.
* Expands test-coverage to include Python 3.3, 3.4
* Added a CMS wizard to add a person (available when CMS 3.2.0 is released)
* Bumped CMS requirements to work with CMS 3.2


1.0.1 (2015-08-04)
==================

* Fixed bug with empty value in aldryn config field validation
* Added missing migration
* Fixed South migration in Django 1.6.x
* Correct documentation issues
* Fixed an issue where the CMSToolbar may fail to load


1.0.0 (2015-07-29)
==================

* Added revisioning
* Names (and slugs) are now translatable
* Groups are now sortable
* Users are presented alphabetically
* New option to show ungrouped people in people plugin
* New groups list view
* Added CMS Toolbar "people" when on Aldryn People views
* Numerous other UI/UX improvements
* Added documentation
* Added Django 1.8.x and django CMS 3.1.x support
* Added configuration for frontend testing
* Added static placeholders to group-list and group-detail templates


0.5.3 (2015-07-08)
==================

* Added another missing django >= 1.7 migration
* Fixed integrity error on automatic slug generation


0.5.2 (2015-04-25)
==================

* Added missing django >= 1.7 migration
* Dropped support for django 1.4 & 1.5
* Updated requirements to require aldryn-common>=0.1.3


0.5.1 (2015-04-16)
==================

* Use get_current_language from cms instead get_language from Django because Django bug #9340
