###################
Using Aldryn People
###################

.. note::
   This part of the guide assumes that django CMS has been :doc:`appropriately installed and
   configured </introduction/installation>`, including Aldryn People, and that :doc:`a People page
   has been set up </introduction/basic_usage>`.


************
Add a person
************

Visit the People page. You should see that the django CMS toolbar now contains a new item, *People*.
Select *Add Person...* from this menu.

Provide some basic details, such as:

* ``Name``
* a ``Role`` (optional)
* ``User`` (optional) if you would like to have this Person associated with a Django User


Add the Person to a Group
=========================

People can optionally belong to Groups. In the *Groups* section in the *Add Person* form, add a new
Group, giving it a name such as "Staff". Save the Group.

.. The following notice can be removed once this issue is resolved:
   https://github.com/aldryn/aldryn-people/issues/71
..

   **Please note:** There is a known issue when creating the first group where
   the Add Group pop-up form will turn blank on submission and the Add/Edit
   form will not be properly updated. It is recommended that for this first
   group, create the group directly using the django CMS toolbar menu item
   "Add new group ..." in the "People" menu instead.

You'll see that the new Group now appears in the list of Groups, and that the Person has membership
of it (it is ticked, meaning the Person belongs to it).

Finally, **Save** the new Person.

The new Person will now appear in any Groups you have added it to, with a link to a profile page
with more information.

You can use the standard django CMS placeholder interface to add more content to your job openings.

You can edit People and Groups at any time via the admin, or if the page you're on has *People* in
django CMS toolbar, select "Person list..." or "Group list..." to get to the admin lists directly.

*******
Plugins
*******

The People page is a handy automatic listing of People in the system, but Aldryn People also
includes a plugin that can be inserted into any django CMS page - indeed, into any content.

For example, if you have a news article discussing a Person on your site, you can drop a People
plugin into that page to link to the Person's full profile.

First, create another Person so that you have at least two in the system.

Create a new django CMS page, and insert a People plugin. Choose which people are to be shown in
the list, and re-order them by dragging the list of available people.

Options are available to list people according to their groups, and to include vCards for each
person.
