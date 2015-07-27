.. image:: https://badge.fury.io/py/aldryn_people.svg
    :target: http://badge.fury.io/py/aldryn_people
.. image:: https://travis-ci.org/divio/django-cms.svg?branch=develop
    :target: https://travis-ci.org/divio/django-cms
.. image:: https://img.shields.io/coveralls/aldryn/aldryn-people.svg
    :target: https://coveralls.io/r/aldryn/aldryn-people
.. image:: https://codeclimate.com/github/aldryn/aldryn-people/badges/gpa.svg
   :target: https://codeclimate.com/github/aldryn/aldryn-people
   :alt: Code Climate

===============
Aldryn People
===============


Description
~~~~~~~~~~~

This add-on allows you to:

- add people/groups
- display them on CMS pages
- download vCards


Installation & Usage
--------------------


Aldryn Platform Users
~~~~~~~~~~~~~~~~~~~~~

1) Choose a site you want to install the add-on to from the dashboard.

2) Go to **Apps** > **Install App**

3) Click **Install** next to the **People** app.

4) Redeploy the site.


Manual Installation
~~~~~~~~~~~~~~~~~~~

1) Run `pip install aldryn-people`.

2) Add below apps to ``INSTALLED_APPS``: ::

    INSTALLED_APPS = [
        …
        'aldryn_boilerplates',
        'aldryn_people',
        'aldryn_translation_tools',
        'easy_thumbnails'
        'filer',
        'parler',
        'sortedm2m',
        …
    ]

3) Run migrations: `python manage.py migrate aldryn_people`.

   NOTE: aldryn_people supports both South and Django 1.7 migrations. However,
   If your project uses a version of South older than 1.0.2, you may need to add
   the following to your settings: ::

   MIGRATION_MODULES = [
       …
       'aldryn_people': 'aldryn_people.south_migrations',
       …
   ]

4) Install aldryn-boilerplates according to the instructions.

5) Install django-filer according to its instructions. In particular, ensure
   you've added the following to your settings: ::

    THUMBNAIL_PROCESSORS = (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        #'easy_thumbnails.processors.scale_and_crop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    )

6) (Re-)Start your application server.


Other Settings
~~~~~~~~~~~~~~

PEOPLE_PLUGIN_STYLES
^^^^^^^^^^^^^^^^^^^^

You can optionally supply a list of CSS class names in the form of a
comma-delimited list for the setting ``PEOPLE_PLUGIN_STYLES``. These items will
then be available in the plugins as styles.


ALDRYN_PEOPLE_USER_THRESHOLD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can optionally also add a setting ``ALDRYN_PEOPLE_USER_THRESHOLD`` with an
integer defining the number of (admin) users for which the user interface will
use a "raw ID field" rather than a drop-down for associating a person with
a user.  The default is 50 users.


Download vCard
~~~~~~~~~~~~~~

Create a CMS page and install the ``People`` app there (choose ``People`` from
the ``Advanced Settings -> Application`` dropdown).

Now redeploy/restart the site again.

The above CMS site has become a vCard download view.


Available Plug-ins
~~~~~~~~~~~~~~~~~~

``People`` plugin lets you display list of people on a CMS page.


NOTES
-----

SortedM2M
~~~~~~~~~

When using this project with Django 1.7.4 or later, please install the latest
version of `django-sortedm2m from its GitHub repository`__. Or, a version from
PyPI which is 0.8.2 or later.

__ https://github.com/gregmuellegger/django-sortedm2m

HVAD > Parler
~~~~~~~~~~~~~

This project was converted from using django-hvad to django-parler from version
0.4.0. If you require HVAD in your project, checkout git tag v0.3.5_.

.. _v0.3.5: https://github.com/aldryn/aldryn-people/tree/0.3.5

Python 3 (in-)compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Due to a dependency on the OSS project vobject_, which was last updated in 2009
and seems to strive to maintain Py2.4 compatibility, this project is currently
*not* Python 3 compatible. Pull requests for a Py3-compatible version of vobject
would be graciously accepted.

.. _vobject: http://vobject.skyhouseconsulting.com/
