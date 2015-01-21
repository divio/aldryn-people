# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..models import Person, Group

from . import BasePeopleTest


class TestPeopleModels(BasePeopleTest):

    def test_create_person(self):
        """
        We can create a person with a name
        """
        name = 'Tom Test'
        person = Person.objects.create(name=name)
        self.assertEqual(person.name, name)
        self.assertEqual(Person.objects.all()[0], person)

    def test_delete_person(self):
        """
        We can delete a person
        """
        name = 'Person Delete'
        Person.objects.create(name=name)
        Person.objects.get(name=name).delete()
        self.assertFalse(Person.objects.filter(name=name))

    def test_create_group(self):
        """
        We can create a group with a name
        """
        group = Group.objects.create(name='group_b')
        self.assertTrue(group.name, 'group_b')

    def test_delete_group(self):
        """
        We can delete a group
        """
        name = 'Gruop Delete'
        Group.objects.create(name=name)
        Group.objects.using_translations().get(name=name).delete()
        self.assertFalse(Group.objects.using_translations().filter(name=name))

    def test_create_another_group(self):
        """
        we create a group
        """
        name = 'Gruppe Neu'
        group = Group.objects.create(name=name)
        self.assertEqual(group.name, name)
        self.assertEqual(Group.objects.all()[0], group)

    def test_add_person_to_group(self):
        """
        We create a person and add her to the created group
        """
        personname = 'Daniel'
        person = Person.objects.create(name=personname)
        name = 'Group One'
        group = Group.objects.create(name=name)
        person.group = group
        person.save()
        self.assertIn(person, group.person_set.all())
