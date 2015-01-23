# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GroupTranslation'
        db.create_table(u'aldryn_people_group_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['aldryn_people.Group'])),
        ))
        db.send_create_signal(u'aldryn_people', ['GroupTranslation'])

        # Adding unique constraint on 'GroupTranslation', fields ['language_code', 'master']
        db.create_unique(u'aldryn_people_group_translation', ['language_code', 'master_id'])

        # Adding model 'Group'
        db.create_table(u'aldryn_people_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'aldryn_people', ['Group'])

        # Adding model 'PersonTranslation'
        db.create_table(u'aldryn_people_person_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('comment', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['aldryn_people.Person'])),
        ))
        db.send_create_signal(u'aldryn_people', ['PersonTranslation'])

        # Adding unique constraint on 'PersonTranslation', fields ['language_code', 'master']
        db.create_unique(u'aldryn_people_person_translation', ['language_code', 'master_id'])

        # Adding model 'Person'
        db.create_table(u'aldryn_people_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, null=True, blank=True)),
            ('mobile', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldryn_people.Group'], null=True, blank=True)),
        ))
        db.send_create_signal(u'aldryn_people', ['Person'])

        # Adding model 'PeoplePlugin'
        db.create_table(u'cmsplugin_peopleplugin', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'aldryn_people', ['PeoplePlugin'])

        # Adding M2M table for field people on 'PeoplePlugin'
        db.create_table(u'aldryn_people_peopleplugin_people', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('peopleplugin', models.ForeignKey(orm[u'aldryn_people.peopleplugin'], null=False)),
            ('person', models.ForeignKey(orm[u'aldryn_people.person'], null=False))
        ))
        db.create_unique(u'aldryn_people_peopleplugin_people', ['peopleplugin_id', 'person_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PersonTranslation', fields ['language_code', 'master']
        db.delete_unique(u'aldryn_people_person_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'GroupTranslation', fields ['language_code', 'master']
        db.delete_unique(u'aldryn_people_group_translation', ['language_code', 'master_id'])

        # Deleting model 'GroupTranslation'
        db.delete_table(u'aldryn_people_group_translation')

        # Deleting model 'Group'
        db.delete_table(u'aldryn_people_group')

        # Deleting model 'PersonTranslation'
        db.delete_table(u'aldryn_people_person_translation')

        # Deleting model 'Person'
        db.delete_table(u'aldryn_people_person')

        # Deleting model 'PeoplePlugin'
        db.delete_table(u'cmsplugin_peopleplugin')

        # Removing M2M table for field people on 'PeoplePlugin'
        db.delete_table('aldryn_people_peopleplugin_people')


    models = {
        u'aldryn_people.group': {
            'Meta': {'object_name': 'Group'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'aldryn_people.grouptranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'GroupTranslation', 'db_table': "u'aldryn_people_group_translation'"},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['aldryn_people.Group']"})
        },
        u'aldryn_people.peopleplugin': {
            'Meta': {'object_name': 'PeoplePlugin', 'db_table': "u'cmsplugin_peopleplugin'", '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['aldryn_people.Person']", 'null': 'True', 'blank': 'True'})
        },
        u'aldryn_people.person': {
            'Meta': {'object_name': 'Person'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_people.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'aldryn_people.persontranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'PersonTranslation', 'db_table': "u'aldryn_people_person_translation'"},
            'comment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['aldryn_people.Person']"})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['aldryn_people']