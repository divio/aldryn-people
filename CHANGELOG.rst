CHANGELOG
=========


2.0.0 (2018-01-17)
------------------

* Introduced django CMS 3.5 support
* Dropped aldryn-reversion/django-reversion support
* Dropped Django 1.6 and 1.7 support
* Added Django 1.10 support

1.2.2 (2016-09-05)
------------------

* Updated translations
* Fixed related_name inconsistency with django CMS 3.3.1
* Dropped support for djangoCMS < 3.2
* Introduced support for djangoCMS 3.4.0


1.2.1 (2016-05-17)
------------------

* Changes name and slug fields in admin to full width
* Add support for Django Reversion v1.10+
* Add support and test coverage for Python 3.5
* Add support and test coverage for Django v1.9
* Add support and test coverage for django CMS v3.3
* Updates testing tools and matrices


1.2.0 (2016-03-10)
------------------

* Remove unused render_placeholder configs
* Add static_placeholders where necessary
* Simplify templates


1.1.6 (2016-02-11)
------------------

* Add Django 1.9 compatibility
* Add stripped default django templates to `/aldryn_people/templates`


1.1.5 (2016-01-12)
------------------

* Improves compatibility with recent versions of django-reversion
* Adds integration tests against CMS 3.2


1.1.4 (2016-01-09)
------------------

* Adds support for reversion for wizards
* Cleanup and update test configuration
* Adds missing migrations


1.1.3 (2015-11-10)
------------------

* Remove visual from wizard form


1.1.2 (2015-11-10)
------------------

* Prevents (benign) JS errors on console.
* Better handle cases where there is no apphook present/published
* Disable the Group wizard (too infrequently used)


1.1.1 (2015-11-03)
------------------

* Relax Filer requirement restriction to allow v1.0+


1.1.0 (2015-10-31)
------------------

* Reimplements vCard downloads in a Py3 compatible way (Thanks, Adam Brenecki!)
* Solves an issue where "Menus could not be loaded" messages were occurring in
  certain situations.
* Expands test-coverage to include Python 3.3, 3.4
* Adds a CMS wizard to add a person (available when CMS 3.2.0 is released)
* Bumps CMS requirements to work with CMS 3.2


1.0.1 (2015-08-04)
------------------

* Fixes bug with empty value in aldryn config field validation
* Adds missing migration
* Fix South migration in Django 1.6.x
* Correct documentation issues
* Fixes an issue where the CMSToolbar may fail to load


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
* Adds static placeholders to group-list and group-detail templates


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
