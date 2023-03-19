from decimal import Decimal
from django.conf import settings
from django.db import models

from store.models import Product

# Create your models here.


class AnonymousUser(models.Model):
    name = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='order_user')
    models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, null=True, blank=True, related_name='anony_order_user')
    full_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=255, blank=True)
    address1 = models.CharField(max_length=250, null=True)
    address2 = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    country_code =models.CharField(max_length=4, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_key = models.CharField(max_length=200, null=True)
    payment_option = models.CharField(max_length=255, blank=True, null=True)
    billing_status = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
