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

from core.models import Customer, Product, Campaign


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


key_to_field_map = getattr(settings, 'CSVIMPORTER_KEY_TO_FIELD_MAP', lambda k: k.replace(' ', '_').lower())

def str_to_product(element, user):
    obj, created = Product.objects.get_or_create(name=element, user=user, defaults={})
    return obj


def str_to_customer(element, user):
    #cut out salutations
    #element = element.remove("Mr") etc.

    #first_name = element.split(' ')[0]
    #last_name = element.split(' ')[1]
    obj, created = Customer.objects.get_or_create(full_name=element, user=user, defaults={})
    return obj


def str_to_campaign(element, user):
    obj, created = Campaign.objects.get_or_create(campaign_name=element, user=user, defaults={})
    return obj


def str_to_company(element):
    #To be used after we add company name to customer model
    pass


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
            #mapped_field_name = self.klass.csvimporter['csv_associate'](field_name)
            #if mapped_field_name in [f.name for f in self.klass._meta.fields]:

            if key_to_field_map(field_name) in [f.name for f in self.klass._meta.fields]:
                self.fields[field_name].initial = key_to_field_map(field_name)
            else:
                _choices = copy(choices)
                #_choices.append((key_to_field_map(field_name), key_to_field_map(field_name)))
                self.fields[field_name] = forms.ChoiceField(choices=_choices, required=False)
                #self.fields[field_name].initial = key_to_field_map(field_name)


    def _validate(self, key, element, user):
        #This is still in pseudo code
        if key == "product":
            element = str_to_product(element, user)
        #elif key == "date_created":
        #    element = str_to_date(element)
        #elif key == "date_released":
        #    element = str_to_date(element)
        elif key == "customer":
            element = str_to_customer(element, user)
        elif key == "marketing_source":
            element = str_to_campaign(element, user)

        return element

    def save(self, request):
        # these are out here because we only need
        # to retreive them from settings the once.

        #transforms = self.klass.csvimporter.get(
        #    'csv_transform', lambda r, d: d)

        transforms = getattr(settings, 'CSVIMPORTER_DATA_TRANSFORMS', {})
        dups = 0
        ok = 0
        for row in self.reader:
            data = {}
            for field_name in self.reader.fieldnames:
                data[self.cleaned_data[field_name]] = row[field_name]
            transform_key = '%s.%s' % (self.instance.content_type.app_label,
                                       self.instance.content_type.model)
            #this line is giving an error, dict not callable
            #data = transforms(request, data)
            new_obj = self.klass()

            #hack to add the currently logged in user's id to the fields
            #data['user_id'] = request.user.id
            data['user'] = request.user
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
                data[key] = self._validate(key, data[key], request.user)
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
