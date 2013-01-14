# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Requester'
        db.create_table('core_requester', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('core', ['Requester'])

        # Adding model 'SatisfactionLevel'
        db.create_table('core_satisfactionlevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core', ['SatisfactionLevel'])

        # Adding model 'DissatisfactionType'
        db.create_table('core_dissatisfactiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['DissatisfactionType'])

        # Adding model 'Topic'
        db.create_table('core_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['Topic'])

        # Adding model 'Level'
        db.create_table('core_level', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['Level'])

        # Adding model 'Request'
        db.create_table('core_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('requester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Requester'])),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('submission_date', self.gf('django.db.models.fields.DateField')()),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Topic'])),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Level'])),
        ))
        db.send_create_signal('core', ['Request'])

        # Adding model 'Response'
        db.create_table('core_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.OneToOneField')(related_name='response', unique=True, to=orm['core.Request'])),
            ('response_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('legal_pursue', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('legal_support', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('legal_ack', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('legal_ent', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('legal_sig', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('legal_tra', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('satisfaction_level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SatisfactionLevel'], null=True, blank=True)),
            ('legal_cost', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Response'])

        # Adding M2M table for field dissatisfaction_reason on 'Response'
        db.create_table('core_response_dissatisfaction_reason', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('response', models.ForeignKey(orm['core.response'], null=False)),
            ('dissatisfactiontype', models.ForeignKey(orm['core.dissatisfactiontype'], null=False))
        ))
        db.create_unique('core_response_dissatisfaction_reason', ['response_id', 'dissatisfactiontype_id'])


    def backwards(self, orm):
        # Deleting model 'Requester'
        db.delete_table('core_requester')

        # Deleting model 'SatisfactionLevel'
        db.delete_table('core_satisfactionlevel')

        # Deleting model 'DissatisfactionType'
        db.delete_table('core_dissatisfactiontype')

        # Deleting model 'Topic'
        db.delete_table('core_topic')

        # Deleting model 'Level'
        db.delete_table('core_level')

        # Deleting model 'Request'
        db.delete_table('core_request')

        # Deleting model 'Response'
        db.delete_table('core_response')

        # Removing M2M table for field dissatisfaction_reason on 'Response'
        db.delete_table('core_response_dissatisfaction_reason')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.dissatisfactiontype': {
            'Meta': {'object_name': 'DissatisfactionType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'core.level': {
            'Meta': {'object_name': 'Level'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'core.request': {
            'Meta': {'object_name': 'Request'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Level']"}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Requester']"}),
            'submission_date': ('django.db.models.fields.DateField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Topic']"})
        },
        'core.requester': {
            'Meta': {'object_name': 'Requester'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'core.response': {
            'Meta': {'object_name': 'Response'},
            'dissatisfaction_reason': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.DissatisfactionType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legal_ack': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'legal_cost': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'legal_ent': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'legal_pursue': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'legal_sig': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'legal_support': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'legal_tra': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'request': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'response'", 'unique': 'True', 'to': "orm['core.Request']"}),
            'response_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'satisfaction_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SatisfactionLevel']", 'null': 'True', 'blank': 'True'})
        },
        'core.satisfactionlevel': {
            'Meta': {'object_name': 'SatisfactionLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {})
        },
        'core.topic': {
            'Meta': {'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['core']