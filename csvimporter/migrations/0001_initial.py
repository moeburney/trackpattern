# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'CSV'
        db.create_table('csvimporter_csv', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('csv_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ))
        db.send_create_signal('csvimporter', ['CSV'])


    def backwards(self, orm):
        # Deleting model 'CSV'
        db.delete_table('csvimporter_csv')


    models = {
        'csvimporter.csv': {
            'Meta': {'object_name': 'CSV'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'csv_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['csvimporter']
