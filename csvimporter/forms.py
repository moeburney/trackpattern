import re
from copy import copy

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db import IntegrityError
from django.contrib import messages
from django.utils.translation import ugettext as _

from csvimporter.models import CSV
from csvimporter.utils import create_csv_reader


class CSVForm(forms.ModelForm):
    def __init__(self, model=None, *args, **kwargs):
        self.model = model
        super(CSVForm, self).__init__(*args, **kwargs)
        content_types = ContentType.objects.all()
        self.fields['content_type'] = forms.ModelChoiceField(queryset=content_types)

        if self.model:
            self.fields['content_type'].initial = (
                content_types.get(model=self.model._meta.module_name))
            self.fields['content_type'].widget = forms.widgets.HiddenInput()

    class Meta:
        model = CSV


class CSVAssociateForm(forms.Form):
    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        self.reader = create_csv_reader(instance.csv_file.file)
        self.klass = self.instance.content_type.model_class()
        # pylint: disable-msg=W0212
        choices = ([(None, '---- (None)')] +
                   [(f.name, f.name) for f in self.klass._meta.fields])
        super(CSVAssociateForm, self).__init__(*args, **kwargs)
        for field_name in self.reader.fieldnames:
            self.fields[field_name] = forms.ChoiceField(choices=choices, required=False)
            mapped_field_name = self.klass.csvimporter['csv_associate'](field_name)
            if mapped_field_name in [f.name for f in self.klass._meta.fields]:
                self.fields[field_name].initial = mapped_field_name
            else:
                _choices = copy(choices)
                _choices.append((mapped_field_name, mapped_field_name))
                self.fields[field_name] = forms.ChoiceField(choices=_choices, required=False)
                self.fields[field_name].initial = mapped_field_name

    def save(self, request):
        # these are out here because we only need
        # to retreive them from settings the once.
        transforms = self.klass.csvimporter.get(
            'csv_transform', lambda r, d: d)
        dups = 0
        ok = 0
        for row in self.reader:
            data = {}
            for field_name in self.reader.fieldnames:
                data[self.cleaned_data[field_name]] = row[field_name]
            transform_key = '%s.%s' % (self.instance.content_type.app_label,
                                       self.instance.content_type.model)
            data = transforms(request, data)
            new_obj = self.klass()
            for key in data.keys():
                try:
                    field = new_obj._meta.get_field(key)
                except FieldDoesNotExist:
                    continue
                # Cleaning
                if type(data[key]) in (str, unicode):
                    data[key] = re.sub(
                        r"^ +$", "", data[key].encode()).decode()
                if type(field) in [models.IntegerField, models.FloatField]:
                    data[key] = data[key].replace(",", "")
                    if not data[key]:
                        data[key] = None
                setattr(new_obj, key, data[key])
            try:
                new_obj.save()
                ok += 1
            except IntegrityError, e:
                if 'unique' in str(e):
                    dups += 1
                else:
                    raise
        if ok:
            messages.info(request, _("Successfully imported %s records.") % ok)
        if dups:
            messages.warning(request,
                _("%s records skipped because of duplication.") % dups)
        self.instance.delete()
