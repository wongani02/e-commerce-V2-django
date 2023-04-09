from decimal import Decimal
import uuid

from django.conf import settings
from django.db import models

from store.models import Product
from checkout.models import DeliveryOptions

# Create your models here.


class AnonymousUser(models.Model):
    name = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    email = models.EmailField(max_length=255, blank=True)
    address1 = models.CharField(max_length=250, null=True)
    address2 = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Recieved', 'Recieved'),
        ('On Delivery', 'On Delivery'),
        ('Delivered', 'Delivered'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='order_user')
    anony_user = models.ForeignKey(AnonymousUser,
        on_delete=models.CASCADE,
        null=True, 
        blank=True, 
        related_name='anony_user_order')
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
    order_status = models.CharField(max_length=300, null=True, choices=STATUS, default='Pending')
    additional_text = models.TextField(null=True, blank=True)
    delivery_option = models.ForeignKey(DeliveryOptions, null=True, on_delete=models.DO_NOTHING, related_name='d_option')

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return 'Order for {}'.format(self.full_name) 


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return 'order items for {}-{}'.format(self.order.full_name, self.product.product_name)
