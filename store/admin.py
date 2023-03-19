from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)

# Register your models here.


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin, admin.ModelAdmin):
    list_display= ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug', 'regular_price', 'in_stock', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ['in_stock', 'is_active']
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'author', 'slug', 'price', 'discount_price', 'in_stock', 'created', 'updated']
#     list_filter = ['in_stock', 'is_active']
#     list_editable = ['price', 'discount_price', 'in_stock']
#     prepopulated_fields = {'slug': ('name',)}