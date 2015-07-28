###########
Basic usage
###########

Create a django CMS page to hook the Aldryn People application into. In its *Advanced settings*,
set its ``Application`` to *People*, and use the provided default *aldryn_people* in ``Application
configurations`` before saving.

If you are on the Aldryn platform, the Django project will restart itself to recognise the new
Apphook you have just created. If you are running the project elsewhere, you'll need to do this
manually, for example by stopping and restarting the runserver.

The page is now a landing page for lists of people; it will be empty until you create some.

The behaviour of the People system should be largely self-explanatory, but the :doc:`tutorial for
users </user/index>` will guide you through some basic steps if necessary.
