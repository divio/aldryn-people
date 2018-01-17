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


Django Parler
=============

This application uses (and will install) `Django Parler
<https://github.com/edoburu/django-parler>`_, which requires some additions to
your project's settings. It is best to consult Parler’s documentation, but to
get started, consider adding the following to your project settings::

    PARLER_LANGUAGES = {
        1: (
            {'code': 'en', },
            {'code': 'de', },
            {'code': 'fr', },
        ),
        'default': {
            'fallbacks': ['en', 'fr', 'de', ],
            'hide_untranslated': False,
        }
    }

Modify according to your project's languages, of course. The choices you make
for languages, ``fallback`` and ``hide_untranslated`` should be identical to the choices
made in CMS_SETTINGS for best results.

    **Notice:** At the time of this writing, `Django Parler`_ is at version 1.4
    which supports a single fallback per language. In projects that involve
    more than 2 languages this may present an issue where some views appear
    empty when viewed in a language other than a person or groups’ native
    language and the one, designated fallback language.

    Fortunately, the current "master" branch of the project includes support
    for multiple fallbacks, much like django CMS. If your project uses more
    than 2 languages, consider installing the pre-release version of Parler
    as follows: ::

        pip install https://github.com/edoburu/django-parler/archive/master.zip

    Then, change the setting ``'fallback': 'en',`` (for example) to
    ``'fallbacks': ['en', 'fr', 'de', ]`` (also for example).

.. Django Parler: https://github.com/edoburu/django-parler



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

SortedM2M
=========

Please install ``django-sortedm2m`` version
0.8.2 or later, or use the version from the `from the django-sortedm2m GitHub repository
<https://github.com/gregmuellegger/django-sortedm2m>`_.


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
