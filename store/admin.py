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
    BlogPost,
    BlogImage,
    About
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
    list_display = ['product_name', 'regular_price', 'in_stock', 'created_at']
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ['created_at']
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]


class BlogImageInline(admin.TabularInline):
    model = BlogImage


@admin.register(BlogPost)
class BlogPostModelAdmin(admin.ModelAdmin):
    inlines = [BlogImageInline]
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'created']
    list_filter = [
        'created'
    ]
    ordering = ('-created',)

admin.site.register(About)
admin.site.site_header = "Pressons by Nana Administration"
admin.site.site_title = "Pressons by Nana"
admin.site.index_title = "Pressons by Nana"