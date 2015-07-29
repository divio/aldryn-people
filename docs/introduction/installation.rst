############
Installation
############


*******************
Installing packages
*******************

We'll assume you have a django CMS (version 3.x) project up and running.

If you need to set up a new django CMS project, follow the instructions in the `django CMS tutorial
<http://docs.django-cms.org/en/develop/introduction/install.html>`_.

Then run either::

    pip install aldryn-people

or to install from the latest source tree::

    pip install -e git+https://github.com/aldryn/aldryn-people.git#egg=aldryn-people


***********
settings.py
***********

In your project's ``settings.py`` make sure you have all of::

    'aldryn_common',
    'aldryn_boilerplates',
    'aldryn_people',
    'parler',
    'aldryn_translation_tools',
    'sortedm2m',
    'easy_thumbnails'
    'filer',

listed in ``INSTALLED_APPS``, *after* ``'cms'``.

.. note::
   If you are using Django 1.6, add ``south`` to  ``INSTALLED_APPS``.


Aldryn Boilerplates
===================

This application uses (and will install) `Aldryn Boilerplates
<https://github.com/aldryn/aldryn-boilerplates>`_, which requires some basic configuration to get
you started.

Edit your settings so that they conform to::

    TEMPLATE_CONTEXT_PROCESSORS = [
        ...
        'aldryn_boilerplates.context_processors.boilerplate',
        ...
    ]

    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        # important - place immediately before AppDirectoriesFinder
        'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

    TEMPLATE_LOADERS = [
        'django.template.loaders.filesystem.Loader',
        # important! place right before django.template.loaders.app_directories.Loader
        'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
        'django.template.loaders.app_directories.Loader',
    ]

Now set the name of the boilerplate you'll use in your project, for example::

    ALDRYN_BOILERPLATE_NAME = 'bootstrap3'

.. note::
   Note that Aldryn People doesn't use the the traditional Django ``/templates`` and ``/static
   directories``. Instead, it employs `Aldryn Boilerplates
   <https://github.com/aldryn/aldryn-boilerplates>`_, which makes it possible to to support
   multiple different frontend schemes ('Boilerplates')and switch between them without the need for
   project-by-project file overwriting.

   Aldryn People's templates and staticfiles will be found in named directories in the
   ``/boilerplates`` directory.


**********************
Software version notes
**********************

South and migrations
====================

Aldryn People supports both South and Django 1.7 migrations. However, *if your project uses a
version of South older than 1.0.2*, you will need to add the following to your settings::

   MIGRATION_MODULES = [
       …
       'aldryn_people': 'aldryn_people.south_migrations',
       …
   ]


SortedM2M
=========

*When using this project with Django 1.7.4 or later*, please install ``django-sortedm2m`` version
0.8.2 or later, or use the version from the `from the django-sortedm2m GitHub repository
<https://github.com/gregmuellegger/django-sortedm2m>`_.


Python 3
========

Due to a dependency on the OSS project vobject_, which was last updated in 2009
and seems to strive to maintain Py2.4 compatibility, this project is currently
*not* Python 3 compatible. Pull requests for a Py3-compatible version of ``vobject``
would be graciously accepted.

.. _vobject: http://vobject.skyhouseconsulting.com/


****************************
Prepare the database and run
****************************

Now run ``python manage.py migrate`` to prepare the database for the new
application, then ``python manage.py runserver``.


****************
For Aldryn users
****************

On the Aldryn platform, the Addon is available from the `Marketplace
<http://www.aldryn.com/en/marketplace>`_.

You can also `install Aldryn People into any existing Aldryn project
<https://control.aldryn.com/control/?select_project_for_addon=aldryn-people>`_.

You can configure some settings in the Aldryn control panel, either at installation time or later.
