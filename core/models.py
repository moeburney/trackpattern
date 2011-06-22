import os
import time
import urllib
from datetime import datetime
from django.db import models
from django.db.models import Sum, Avg, Count
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
from django.contrib.auth.models import User

class Group():
    """
    represents a virtual group
    note: no respctive database table
    """
    

    def __init__(self, user):
        self.user = user
        self.GROUP_DEFINITIONS = ({'id':0, 'name':'Silver (Prospective Buyers)'}, {'id':1, 'name':'Gold (First Time Buyers)'},{'id':2, 'name':'Platinum (Repeat Buyers)'})
        
    def get_group(self, id):
        id = int(id)
        if id < 2:
            customers = Customer.objects.filter(user=self.user).annotate(bought=Count('sale')).filter(bought=id)
        else:
            customers = Customer.objects.filter(user=self.user).annotate(bought=Count('sale')).filter(bought__gte=id)
        self.GROUP_DEFINITIONS[id]['customers'] = customers
        return self.GROUP_DEFINITIONS[id]
    
class Category(models.Model):
    """
    represents a group
    """
    CONNECTION_CHOICES = (
        (0, 'High'),
        (1, 'Medium'),
        (2, 'Low'),
        )
    
    name = models.CharField(_('name'), max_length=50, blank=False, null=False)
    characteristics =  models.CharField(_('characteristics'), max_length=200, blank=True, null=True)
    interests = models.CharField(_('core interests'), max_length=200, blank=True, null=True)
    connection = models.SmallIntegerField(_('connection'), choices=CONNECTION_CHOICES, default=2)
    
    # foreign key mappings goes here
    user = models.ForeignKey(User, blank=False, null=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def total_revenue_generated(self):
        """
        calculates total turnover generated by this category.
        boils down to sum of turnover generated by all customers in this category
        """
        turnover = Sale.objects.filter(customer__category=self).aggregate(turnover=Sum('price'))
        return turnover['turnover'] or 0.0
        

    def total_sales(self):
        return Sale.objects.filter(customer__category=self).count()

    def most_common_path(self):
        most_bought_products = Product.objects.filter(sale__customer__category=self).annotate(bought=Count('sale__product')).order_by('-bought')
        return ' > '.join(product.name for product in most_bought_products)
    
    def get_rank(self):
        groups_by_revenue = Category.objects.filter(user=self.user).annotate(revenue=Sum('customer__sale__price')).order_by('-revenue')
        counter = 0
        rank = len(categories_by_revenue)
        for each in categories_by_revenue:
            counter = counter + 1
            if each.pk == self.pk:
                rank = counter
                break
        return rank

    def gifts_sent(self):
        result = Customer.objects.filter(category=self).aggregate(total_gifts_sent=Sum('gifts_sent'))
        return result['total_gifts_sent'] or 0

    def surveys_sent(self):
        result = Customer.objects.filter(category=self).aggregate(total_suveys_sent=Sum('surveys_sent'))
        return result['total_suveys_sent'] or 0


    def last_activity(self):
        try:
            sale = Sale.objects.filter(customer__category=self).order_by('-transaction_date')[0]
            return sale.transaction_date
        except IndexError:
            return None
    
class Product(models.Model):
    """
    represents a product
    """
    IMPORTANCE_CHOICES = (
        (0, 'High'),
        (1, 'Medium'),
        (2, 'Low'),
        )
    name = models.CharField(_('name'), max_length=50, blank=False, null=False)
    date_released = models.DateField(_('date released'), blank=True, null=True)
    current_price = models.DecimalField(_('current price'), max_digits=10, decimal_places=2, blank=True, null=False, default=0)
    importance = models.SmallIntegerField(_('importance'), choices=IMPORTANCE_CHOICES, default=2)
    main_appeal = models.CharField(_('main appeal'), max_length=200, blank=True, null=False)
    surveys_sent = models.PositiveIntegerField(_('surveys sent'), default=0)
    
    # foreign key mappings goes here
    user = models.ForeignKey(User, blank=False, null=False)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_rank(self):
        """
        gets rank of this product among other products
        basing on purchases. highest purchases leads to highest rank
        """
        products = Product.objects.filter(user=self.user).annotate(bought=Count('sale')).order_by('-bought')
        rank = len(products)
        counter = 0
        for product in products:
            counter = counter + 1
            if product.pk == self.pk:
                rank = counter
                break
        return rank
    
    def most_bought_category(self):
        """
        gets the category name that bought most.
        if multiple categories applicable, returns a concatenated string
        """
        categories = Category.objects.filter(customer__sale__product=self).annotate(bought=Count('customer__sale__product')).order_by('-bought')
        if categories:
            return groups[0].name
        return ''

    def most_common_path(self):
        return ''

    def total_sales(self):
        return Sale.objects.filter(product=self).count()

    def total_turnover_generated(self):
        """
        calculates total turnover generated by this customer
        """
        result = Sale.objects.filter(product=self).aggregate(turnover=Sum('price'))
        return result['turnover'] or 0.0

    
class Customer(models.Model):
    """
    represents a customer entity.
    """

    CONNECTION_CHOICES = (
        (0, 'High'),
        (1, 'Medium'),
        (2, 'Low'),
        )
    
    first_name = models.CharField(_('first name'), max_length=50, blank=False, null=False)
    last_name =  models.CharField(_('last name'), max_length=50, blank=False, null=False)
    company_name = models.CharField(_('company name'), max_length=100, blank=True, null=False, default="")
    email = models.EmailField(_('email'), max_length=75, blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=15, blank=True, null=True)
    street = models.CharField(_('street'), max_length=100, blank=True, null=True)
    city = models.CharField(_('city'), max_length=100, blank=True, null=True)    
    state = models.CharField(_('state'), max_length=75, blank=True, null=False)    
    country = models.CharField(_('country'), max_length=75, blank=True, null=False)
    zipcode = models.CharField(_('zip'), max_length=10, blank=True, null=True)

    interests = models.CharField(_('core interests'), max_length=200, blank=True, null=False)
    connection = models.SmallIntegerField(_('connection'), choices=CONNECTION_CHOICES, default=2)
    gifts_sent = models.PositiveIntegerField(_('gifts sent'), default=0)
    surveys_sent = models.PositiveIntegerField(_('surveys sent'), default=0)
    
    user = models.ForeignKey(User, blank=False, null=False)
    #category = models.ForeignKey(Category, blank=False, null=False)

    class Meta:
        ordering = ['first_name', 'last_name']

    def full_name(self):
        return '%s %s'% (self.first_name, self.last_name)
    
    def __unicode__(self):
        return self.full_name()

    def group(self):
        """
        calculates customer's virtual group
        """
        sale_count = self.sale_set.count()
        group = Group(self.user)
        if not sale_count:
            return group.GROUP_DEFINITIONS[0]
        elif sale_count == 1:
            return group.GROUP_DEFINITIONS[1]
        else:
            return group.GROUP_DEFINITIONS[2]

    def path(self):
        """
        path represents list of products sold in order of date
        """
        sales = Sale.objects.filter(customer=self)
        return ' > '.join(sale.product.name for sale in sales)

    def total_turnover_generated(self):
        """
        calculates total turnover generated by this customer
        """
        turnover = Sale.objects.filter(customer=self).aggregate(turnover=Sum('price'))
        return turnover['turnover'] or 0.0

    def total_purchases(self):
        """
        gets the total number of sales made by this customer
        """
        return Sale.objects.filter(customer=self).count()


    
class Sale(models.Model):
    """
    represents a sale transaction
    """
    customer = models.ForeignKey(Customer, blank=False, null=False)
    product = models.ForeignKey(Product, blank=False, null=False)
    transaction_date = models.DateField(_('date'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, blank=False, null=False)
    
    shopping_cart_source = models.CharField('shopping cart source', max_length=100, blank=True, null=False)
    marketing_source = models.CharField('marketing source', max_length=100, blank=True, null=False)
    user = models.ForeignKey(User, blank=False, null=False)
    
    class Meta:
        ordering = ['transaction_date']

    def __unicode__(self):
        return '%s %s %s'%(self.customer, self.product, self.transaction_date)
    
