# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Response.satisfaction_level'
        db.add_column('core_response', 'satisfaction_level',
                      self.gf('django.db.models.fields.related.ForeignKey')(default="6", to=orm['core.SatisfactionLevel']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Response.satisfaction_level'
        db.delete_column('core_response', 'satisfaction_level_id')


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
            'security_answer': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'security_question': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
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
            'satisfaction_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SatisfactionLevel']", 'default':'6'})
        },
        'core.satisfactionlevel': {
            'Meta': {'object_name': 'SatisfactionLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.TextField', [], {})
        },
        'core.topic': {
            'Meta': {'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['core']