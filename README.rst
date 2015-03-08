.. image:: https://badge.fury.io/py/aldryn_people.svg
    :target: http://badge.fury.io/py/aldryn_people
.. image:: https://travis-ci.org/divio/django-cms.svg?branch=develop
    :target: https://travis-ci.org/divio/django-cms
.. image:: https://img.shields.io/coveralls/aldryn/aldryn-people.svg
    :target: https://coveralls.io/r/aldryn/aldryn-people

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
        'parler',
        'sortedm2m',
        'aldryn_people',
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

4) Install aldryn-boilerplates

5) (Re-)Start your application server.


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
