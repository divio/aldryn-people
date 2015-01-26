# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.utils.translation import override, force_text

from ..models import Person, Group

from . import BasePeopleTest


class TestBasicPeopleModels(TransactionTestCase):

    def test_create_person(self):
        """We can create a person with a name."""
        name = 'Tom Test'
        person = Person.objects.create(name=name)
        self.assertEqual(person.name, name)
        self.assertEqual(Person.objects.all()[0], person)

    def test_delete_person(self):
        """We can delete a person."""
        name = 'Person Delete'
        Person.objects.create(name=name)
        Person.objects.get(name=name).delete()
        self.assertFalse(Person.objects.filter(name=name))

    def test_str(self):
        name = 'Person Str'
        person = Person.objects.create(name=name)
        self.assertEqual(force_text(person), name)

    def test_absolute_url(self):
        slug = 'person-slug'
        person = Person.objects.create(slug=slug)
        # This isn't a translation test, per se, but let's make sure that we
        # have a predictable language prefix, regardless of the tester's locale.
        with override('en'):
            self.assertEqual(
                person.get_absolute_url(),
                '/en/people/{0}/'.format(slug)
            )
            # Now test that it will work when there's no slug too.
            person.slug = ''
            self.assertEqual(
                person.get_absolute_url(),
                '/en/people/{0}/'.format(person.pk),
            )

    def test_auto_slugify(self):
        name = 'Melchior Hoffman'
        slug = 'melchior-hoffman'
        person = Person.objects.create(name=name)
        person.save()
        self.assertEquals(person.slug, slug)


class TestBasicGroupModel(TransactionTestCase):

    def test_create_group(self):
        """We can create a group with a name."""
        group = Group.objects.create(name='group_b')
        self.assertTrue(group.name, 'group_b')

    def test_delete_group(self):
        """We can delete a group."""
        name = 'Group Delete'
        Group.objects.create(name=name)
        group = Group.objects.translated(name=name)
        if group:
            group[0].delete()
        self.assertFalse(Group.objects.translated(name=name))

    def test_create_another_group(self):
        """we create a group."""
        name = 'Gruppe Neu'
        group = Group.objects.create(name=name)
        self.assertEqual(group.name, name)
        self.assertEqual(Group.objects.all()[0], group)

    def test_add_person_to_group(self):
        """We create a person and add her to the created group."""
        personname = 'Daniel'
        person = Person.objects.create(name=personname)
        name = 'Group One'
        group = Group.objects.create(name=name)
        person.group = group
        person.save()
        self.assertIn(person, group.person_set.all())


class TestPersonModelTranslation(BasePeopleTest):

    def test_person_translatable(self):
        person1 = self.reload(self.person1, 'en')
        self.assertEqual(
            person1.function,
            self.data['person1']['en']['function']
        )
        person1 = self.reload(self.person1, 'de')
        self.assertEqual(
            person1.safe_translation_getter('function'),
            self.data['person1']['de']['function']
        )

    def test_comment(self):
        person1 = self.reload(self.person1, 'en')
        self.assertEqual(
            person1.comment,
            self.data['person1']['en']['description']
        )
        person1 = self.reload(self.person1, 'de')
        self.assertEqual(
            person1.comment,
            self.data['person1']['de']['description']
        )

    def test_get_vcard(self):
        person1 = self.reload(self.person1, 'en')
        # Test with no group
        vcard_en = 'BEGIN:VCARD\r\nVERSION:3.0\r\nFN:person1\r\nN:;person1;;;\r\nTITLE:function1\r\nEND:VCARD\r\n'  # flake8: noqa
        self.assertEqual(
            person1.get_vcard(),
            vcard_en
        )
        # Test with a group and other fields populated
        group1 = self.reload(self.group1, 'en')
        group1.address = '123 Main Street'
        group1.city = 'Anytown'
        group1.postal_code = '12345'
        group1.phone = '+1 (234) 567-8903'
        group1.fax = '+1 (234) 567-8904'
        group1.website = 'www.groupwebsite.com'
        group1.save()
        person1.group = group1
        person1.email = 'person@org.org'
        person1.phone = '+1 (234) 567-8900'
        person1.mobile = '+1 (234) 567-8901'
        person1.fax = '+1 (234) 567-8902'
        person1.website = 'www.website.com'
        person1.save()
        vcard_en = 'BEGIN:VCARD\r\nVERSION:3.0\r\nADR;TYPE=WORK:;;123 Main Street;Anytown;;12345;\r\nEMAIL:person@org.org\r\nFN:person1\r\nN:;person1;;;\r\nORG:group1\r\nTEL;TYPE=WORK:+1 (234) 567-8900\r\nTEL;TYPE=CELL:+1 (234) 567-8901\r\nTEL;TYPE=FAX:+1 (234) 567-8902\r\nTEL;TYPE=WORK:+1 (234) 567-8903\r\nTEL;TYPE=FAX:+1 (234) 567-8904\r\nTITLE:function1\r\nURL:www.website.com\r\nURL:www.groupwebsite.com\r\nEND:VCARD\r\n'  # flake8: noqa
        self.assertEqual(
            person1.get_vcard(),
            vcard_en
        )
        # Ensure this works for other langs too
        person1 = self.reload(self.person1, 'de')
        vcard_de = 'BEGIN:VCARD\r\nVERSION:3.0\r\nADR;TYPE=WORK:;;123 Main Street;Anytown;;12345;\r\nEMAIL:person@org.org\r\nFN:person1\r\nN:;person1;;;\r\nORG:Gruppe1\r\nTEL;TYPE=WORK:+1 (234) 567-8900\r\nTEL;TYPE=CELL:+1 (234) 567-8901\r\nTEL;TYPE=FAX:+1 (234) 567-8902\r\nTEL;TYPE=WORK:+1 (234) 567-8903\r\nTEL;TYPE=FAX:+1 (234) 567-8904\r\nTITLE:Funktion1\r\nURL:www.website.com\r\nURL:www.groupwebsite.com\r\nEND:VCARD\r\n'  # flake8: noqa
        with override('de'):
            self.assertEqual(
                person1.get_vcard(),
                vcard_de
            )


class TestGroupModelTranslation(BasePeopleTest):

    def test_group_translation(self):
        group1 = self.reload(self.group1, 'en')
        self.assertEqual(group1.name, self.data['group1']['en']['name'])
        group1 = self.reload(self.group1, 'de')
        self.assertEqual(group1.name, self.data['group1']['de']['name'])

    def test_company_name(self):
        group1 = self.reload(self.group1, 'en')
        self.assertEqual(
            group1.company_name,
            self.data['group1']['en']['name'],
        )
        group1 = self.reload(self.group1, 'de')
        self.assertEqual(
            group1.company_name,
            self.data['group1']['de']['name'],
        )

    def test_company_description(self):
        group1 = self.reload(self.group1, 'en')
        self.assertEqual(
            group1.company_description,
            self.data['group1']['en']['description'],
        )
        group1 = self.reload(self.group1, 'de')
        self.assertEqual(
            group1.company_description,
            self.data['group1']['de']['description'],
        )

    def test_str(self):
        group1 = self.reload(self.group1, 'en')
        self.assertEqual(
            force_text(group1),
            self.data['group1']['en']['name'],
        )
        group1 = self.reload(self.group1, 'de')
        self.assertEqual(
            force_text(group1),
            self.data['group1']['de']['name'],
        )
