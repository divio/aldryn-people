=============
Aldryn People
=============

.. image:: https://travis-ci.org/aldryn/aldryn-people.svg?branch=master
    :target: https://travis-ci.org/aldryn/aldryn-people

.. image:: https://img.shields.io/coveralls/aldryn/aldryn-people.svg
  :target: https://coveralls.io/r/aldryn/aldryn-people

This add-on allows you to:

- add people/groups
- display them on CMS pages
- download vCards

Installation
============

Aldryn Platform Users
---------------------

Choose a site you want to install the add-on to from the dashboard. Then go to ``Apps -> Install app`` and click ``Install`` next to ``People`` app.

Redeploy the site.

Manual Installation
-------------------

Run `pip install aldryn-people`.

Add below apps to ``INSTALLED_APPS``: ::

    INSTALLED_APPS = [
        …
        'aldryn_people',
        'hvad',
        'sortedm2m',
        'django-phonenumber-field',
        …
    ]

Download vCard
==============

Create a CMS page and install the ``People`` app there (choose ``People`` from the ``Advanced Settings -> Application`` dropdown).

Now redeploy/restart the site again.

The above CMS site has become a vCard download view.


Available Plug-ins
==================

``People`` plugin lets you display list of people on a CMS page.
