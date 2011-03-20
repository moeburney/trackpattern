import os
import time
import urllib
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
from django.contrib.auth.models import User

class Group(models.Model):
    """
    represents a group
    """
    name = models.CharField(_('name'), max_length=50, blank=False, null=False)
    characteristics =  models.CharField(_('characteristics'), max_length=200, blank=True, null=True)
    connection = models.CharField(_('connection'), max_length=200, blank=True, null=True)
    # foreign key mappings goes here
    user = models.ForeignKey(User, blank=False, null=False)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def rank(self):
        group_avg_rank = self.customer_set.aggregate(models.Avg('rank'))
        return group_avg_rank['rank__avg']

class Product(models.Model):
    """
    represents a product
    """
    name = models.CharField(_('name'), max_length=50, blank=False, null=False)
    date_released = models.DateField(_('date released'), blank=False, null=False)
    current_price = models.DecimalField(_('current price'), max_digits=10, decimal_places=2)
    # foreign key mappings goes here
    user = models.ForeignKey(User, blank=False, null=False)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


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
    connection = models.CharField(_('connection'), max_length=200, blank=True, null=True)
    rank = models.PositiveIntegerField(_('rank'), default=0, choices=zip(range(1,11),range(1,11)))
    
    # foreign key mappings goes here
    user = models.ForeignKey(User, blank=False, null=False)
    group = models.ForeignKey(Group, blank=True, null=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def full_name(self):
        return '%s %s'% (self.first_name, self.last_name)
    
    def __unicode__(self):
        return self.full_name()

    
class Purchases(models.Model):
    """
    represents a purchase transaction
    """
    transaction_date = models.DateField(_('date'), blank=False, null=False)
    customer = models.ForeignKey(Customer, blank=False, null=False)
