#########
Reference
#########

********
Settings
********


PEOPLE_PLUGIN_STYLES
====================

You can optionally supply a list of CSS class names in the form of a
comma-delimited list for the setting ``PEOPLE_PLUGIN_STYLES``. These items will
then be available in the plugins as styles.


ALDRYN_PEOPLE_USER_THRESHOLD
============================

You can optionally also add a setting ``ALDRYN_PEOPLE_USER_THRESHOLD`` with an
integer defining the number of (admin) users for which the user interface will
use a "raw ID field" rather than a drop-down for associating a person with
a user.  The default is 50 users. The change may not occur until the project is
restarted.

