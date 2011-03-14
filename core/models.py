import os
import time
import urllib
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
from django.contrib.auth.models import User


class Customer(models.Model):
    """
    represents a customer entity.
    """
    
    first_name = models.CharField(_('first name'), max_length=50, blank=False, null=False)
    last_name =  models.CharField(_('last name'), max_length=50, blank=False, null=False)
    email = models.EmailField(_('email'), max_length=75, blank=True, null=True)
    street = models.CharField(_('street'), max_length=100, blank=True, null=True)
    zipcode = models.CharField(_('zip'), max_length=10, blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=15, blank=True, null=True)
    # foreign key mappings goes here
    user = models.ForeignKey(User, blank=False, null=False)
    # product = models.ManyToManyField(Product)

    class Meta:
        ordering = ['first_name', 'last_name']

    def full_name(self):
        return '%s %s'% (self.first_name, self.last_name)
        
    def __unicode__(self):
        return self.full_name()
    
