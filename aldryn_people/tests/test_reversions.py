# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from reversion import revision_context_manager
    from reversion import default_revision_manager
except ImportError:
    from reversion.revisions import revision_context_manager
    from reversion.revisions import default_revision_manager

import six

from django.db import transaction

from . import BasePeopleTest
from ..models import Person, Group


class RevisionTestCase(BasePeopleTest):
    data_raw = {
        'group': {
            'en': {
                'name': 'group{0}',
                'description': 'description{0}'
            },
            'de': {
                'name': 'Gruppe{0}',
                'description': 'Beschreibung{0}'
            },
        },
        'person': {
            'en': {
                'function': 'function{0}',
                'description': 'description-{0}-en'
            },
            'de': {
                'function': 'Funktion{0}',
                'description': 'Beschreibung-{0}-de'
            },
        },

    }

    def make_new_values(self, values_dict, replace_with):
        """
        Replace formatting symbol {0} with replace_with param.
        Returns new dictionary with same keys and replaced symbols.
        """
        new_dict = {}
        for key, value in values_dict.items():
            new_val = value.format(replace_with)
            new_dict[key] = new_val
        return new_dict

    def create_revision(self, obj, **kwargs):
        with transaction.atomic():
            with revision_context_manager.create_revision():
                # populate event with new values
                for prop, value in six.iteritems(kwargs):
                    setattr(obj, prop, value)
                obj.save()

    def revert_to(self, object_with_revision, revision_number):
        """
        Revert <object with revision> to revision number.
        """
        # get by position, since reversion_id is not reliable,
        version = list(reversed(
            default_revision_manager.get_for_object(
                object_with_revision)))[revision_number - 1]
        version.revision.revert()

    def test_person_revision_is_created(self):
        values = self.make_new_values(self.data_raw['person']['en'], 1)
        with transaction.atomic():
            with revision_context_manager.create_revision():
                person = Person.objects.create(**values)
        self.assertEqual(
            len(default_revision_manager.get_for_object(person)), 1)

    def test_group_revision_is_created(self):
        values = self.make_new_values(self.data_raw['group']['en'], 1)
        with transaction.atomic():
            with revision_context_manager.create_revision():
                group = Group.objects.create(**values)
        self.assertEqual(
            len(default_revision_manager.get_for_object(group)), 1)

    def test_people_revision_is_reverted(self):
        rev_1_values = self.make_new_values(
            self.data_raw['person']['en'], 1)
        # rev 1
        self.person1.set_current_language('en')
        self.create_revision(self.person1, **rev_1_values)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.person1)), 1)
        # check that values are actually changed
        self.assertEqual(self.person1.function, rev_1_values['function'])
        self.assertEqual(self.person1.description, rev_1_values['description'])

        # rev 2
        rev_2_values = self.make_new_values(
            self.data_raw['person']['en'], 2)
        self.create_revision(self.person1, **rev_2_values)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.person1)), 2)
        # check that values are actually changed
        self.assertEqual(self.person1.function, rev_2_values['function'])
        self.assertEqual(self.person1.description, rev_2_values['description'])

        # revert
        self.revert_to(self.person1, 1)
        self.person1 = Person.objects.get(pk=self.person1.pk)
        # check previous values
        self.assertEqual(
            self.person1.function, rev_1_values['function'])
        self.assertEqual(
            self.person1.description, rev_1_values['description'])

    def test_group_revision_is_reverted(self):
        rev_1_values = self.make_new_values(
            self.data_raw['group']['en'], 1)
        # rev 1
        self.group1.set_current_language('en')
        self.create_revision(self.group1, **rev_1_values)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.group1)), 1)
        # check that values are actually changed
        self.assertEqual(self.group1.name, rev_1_values['name'])
        self.assertEqual(self.group1.description, rev_1_values['description'])

        # rev 2
        rev_2_values = self.make_new_values(
            self.data_raw['group']['en'], 2)
        self.create_revision(self.group1, **rev_2_values)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.group1)), 2)
        # check that values are actually changed
        self.assertEqual(self.group1.name, rev_2_values['name'])
        self.assertEqual(self.group1.description, rev_2_values['description'])

        # revert
        self.revert_to(self.group1, 1)
        self.group1 = Group.objects.get(pk=self.group1.pk)
        # check previous values
        self.assertEqual(
            self.group1.name, rev_1_values['name'])
        self.assertEqual(
            self.group1.description, rev_1_values['description'])

    def test_person_revisions_with_diverged_translations(self):
        rev_1_values_en = self.make_new_values(
            self.data_raw['person']['en'], 1)
        # rev 1: en 1 de 0
        self.person1.set_current_language('en')
        self.create_revision(self.person1, **rev_1_values_en)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.person1)), 1)
        # check that values are actually changed
        self.assertEqual(self.person1.function, rev_1_values_en['function'])
        self.assertEqual(
            self.person1.description, rev_1_values_en['description'])

        # rev 2: en 1 de 1
        rev_2_values_de = self.make_new_values(
            self.data_raw['person']['de'], 1)

        self.person1.set_current_language('de')
        self.create_revision(self.person1, **rev_2_values_de)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.person1)), 2)
        # check that values are actually changed
        self.person1 = Person.objects.get(pk=self.person1.pk)
        self.person1.set_current_language('de')
        self.assertEqual(self.person1.function, rev_2_values_de['function'])
        self.assertEqual(
            self.person1.description, rev_2_values_de['description'])

        # rev 3: en 1 de 2
        rev_3_values_de = self.make_new_values(
            self.data_raw['person']['de'], 1)
        self.person1.set_current_language('de')
        self.create_revision(self.person1, **rev_3_values_de)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.person1)), 3)
        # check that values are actually changed
        self.person1 = Person.objects.get(pk=self.person1.pk)
        self.person1.set_current_language('de')
        self.assertEqual(self.person1.function, rev_3_values_de['function'])
        self.assertEqual(
            self.person1.description, rev_3_values_de['description'])

        # check that en values are left the same
        self.person1.set_current_language('en')
        self.assertEqual(self.person1.function, rev_1_values_en['function'])
        self.assertEqual(
            self.person1.description, rev_1_values_en['description'])

        # revert to rev2 en 1 de 1
        self.revert_to(self.person1, 2)
        self.person1 = Person.objects.get(pk=self.person1.pk)

        # check previous values for en
        self.person1.set_current_language('en')
        self.assertEqual(
            self.person1.function, rev_1_values_en['function'])
        self.assertEqual(
            self.person1.description, rev_1_values_en['description'])

        # check previous values for de
        self.person1.set_current_language('de')
        self.assertEqual(
            self.person1.function, rev_2_values_de['function'])
        self.assertEqual(
            self.person1.description, rev_2_values_de['description'])

    def test_person_revision_with_fk_relations(self):
        """
        Tests against recovering object with fk relations, NOTE though
        at time of writing this test cases aldryn-reversion DOES restores
        ALL OBJECTS THAT ARE PRESENT IN REVISION, which means that from history
        view it would also restore related objects to state of currently
        restored revision.
        Also this test case doesn't checks against that behavior,
        so be careful.
        """
        # rev 1 user1 group 1
        user1 = self.create_user('rev1_user', 'rev1_user')
        rev_1_values = self.make_new_values(
            self.data_raw['person']['en'], 1)
        rev_1_values['user'] = user1
        rev_1_values['groups'] = [self.group1]
        self.person1.set_current_language('en')
        self.create_revision(self.person1, **rev_1_values)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.person1)), 1)
        self.assertEqual(self.person1.user, user1)
        self.assertIn(self.group1, self.person1.groups.all())

        # rev 2 user 2 group 2
        user2 = self.create_user('rev2_user', 'rev2_user')
        rev_2_values = self.make_new_values(
            self.data_raw['person']['en'], 2)
        rev_2_values['user'] = user2
        rev_2_values['groups'] = [self.group2]
        self.create_revision(self.person1, **rev_2_values)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.person1)), 2)
        self.assertEqual(self.person1.user, user2)
        self.assertIn(self.group2, self.person1.groups.all())

        # revert to rev 1 with user 1
        self.revert_to(self.person1, 1)
        self.person1 = Person.objects.get(pk=self.person1.pk)

        self.person1.set_current_language('en')
        self.assertEqual(self.person1.user, user1)
        self.assertNotEqual(self.person1.user, user2)
        self.assertIn(self.group1, self.person1.groups.all())

    def test_group_revisions_with_diverged_translations(self):
        rev_1_values_en = self.make_new_values(
            self.data_raw['group']['en'], 1)
        # rev 1: en 1 de 0
        self.group1.set_current_language('en')
        self.create_revision(self.group1, **rev_1_values_en)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.group1)), 1)
        # check that values are actually changed
        self.assertEqual(self.group1.name, rev_1_values_en['name'])
        self.assertEqual(
            self.group1.description, rev_1_values_en['description'])

        # rev 2: en 1 de 1
        rev_2_values_de = self.make_new_values(
            self.data_raw['group']['de'], 1)

        self.group1.set_current_language('de')
        self.create_revision(self.group1, **rev_2_values_de)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.group1)), 2)
        # check that values are actually changed
        self.group1 = Group.objects.get(pk=self.group1.pk)
        self.group1.set_current_language('de')
        self.assertEqual(self.group1.name, rev_2_values_de['name'])
        self.assertEqual(
            self.group1.description, rev_2_values_de['description'])

        # rev 3: en 1 de 2
        rev_3_values_de = self.make_new_values(
            self.data_raw['group']['de'], 1)
        self.group1.set_current_language('de')
        self.create_revision(self.group1, **rev_3_values_de)
        self.assertEqual(
            len(default_revision_manager.get_for_object(self.group1)), 3)
        # check that values are actually changed
        self.group1 = Group.objects.get(pk=self.group1.pk)
        self.group1.set_current_language('de')
        self.assertEqual(self.group1.name, rev_3_values_de['name'])
        self.assertEqual(
            self.group1.description, rev_3_values_de['description'])

        # check that en values are left the same
        self.group1.set_current_language('en')
        self.assertEqual(self.group1.name, rev_1_values_en['name'])
        self.assertEqual(
            self.group1.description, rev_1_values_en['description'])

        # revert to rev2 en 1 de 1
        self.revert_to(self.group1, 2)
        self.group1 = Group.objects.get(pk=self.group1.pk)

        # check previous values for en
        self.group1.set_current_language('en')
        self.assertEqual(
            self.group1.name, rev_1_values_en['name'])
        self.assertEqual(
            self.group1.description, rev_1_values_en['description'])

        # check previous values for de
        self.group1.set_current_language('de')
        self.assertEqual(
            self.group1.name, rev_2_values_de['name'])
        self.assertEqual(
            self.group1.description, rev_2_values_de['description'])
