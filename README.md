# Aldryn People

[![Build Status](https://travis-ci.org/aldryn/aldryn-people.svg?branch=master)](https://travis-ci.org/aldryn/aldryn-people)
[![Build Status](https://img.shields.io/coveralls/aldryn/aldryn-people.svg)](https://coveralls.io/r/aldryn/aldryn-people)


### Description

This add-on allows you to:

- add people/groups
- display them on CMS pages
- download vCards


## Installation & Usage


### Aldryn Platform Users


Choose a site you want to install the add-on to from the dashboard. Then go to **Apps** > **Install App** and click **Install** next to the newly installed **People** app.

Redeploy the site.


### Manual Installation

Run `pip install aldryn-people`.

Add below apps to ``INSTALLED_APPS``: ::

    INSTALLED_APPS = [
        …
        'aldryn_people',
        'hvad',
        'sortedm2m',
        …
    ]

### Download vCard

Create a CMS page and install the ``People`` app there (choose ``People`` from
the ``Advanced Settings -> Application`` dropdown).

Now redeploy/restart the site again.

The above CMS site has become a vCard download view.


### Available Plug-ins

``People`` plugin lets you display list of people on a CMS page.


## Python 3 compatibility

Due to dependency on [vobject](http://vobject.skyhouseconsulting.com/), which was last updated in 2009 and seems to strive to maintain Py2.4 compatibility, this project is currently *not* Python 3 compatible.
