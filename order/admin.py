from django.contrib import admin
from .models import *

# Register your models here.


class OrderItemsInline(admin.StackedInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    inlines = [OrderItemsInline]
    list_display = ['full_name', 'phone', 'total_paid']
    list_filter = ['created']
    ordering = ('-created',)
