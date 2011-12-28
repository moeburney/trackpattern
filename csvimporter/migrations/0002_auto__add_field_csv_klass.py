# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding field 'CSV.klass'
        db.add_column('csvimporter_csv', 'klass',
            self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True,
                blank=True), keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CSV.klass'
        db.delete_column('csvimporter_csv', 'klass_id')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'csvimporter.csv': {
            'Meta': {'object_name': 'CSV'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'csv_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.related.ForeignKey', [],
                          {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['csvimporter']
