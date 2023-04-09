import uuid

from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

# Create your models here.


class Category(MPTTModel):
    """
    Category Table implimented with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    img = models.ImageField(
        help_text=_("category image"),
        null=True,
        upload_to='cat_imgs',
        blank=True)
    slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse('store:category-list', args=[self.slug])
    
    def get_blog_cat_url(self):
        return reverse('store:blog-category-list', args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    ProductType Table will provide a list of the different types
    of products that are for sale.
    """

    name = models.CharField(verbose_name=_("Product Name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    The Product Specification Table contains product
    specifiction or features for the product types.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The Product table containing all product items.
    """
    product_url = models.UUIDField(_('safe url'), null=True, default=uuid.uuid4, editable=False)
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT, null=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    product_name = models.CharField(
        verbose_name=_("Product name"),
        help_text=_("Required"),
        max_length=255,
        null=True,
    )
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(max_length=255, null=True)
    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 999999999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=10,
        decimal_places=2,
        null=True,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 999999999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 999.99."),
            },
        },
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    in_stock = models.PositiveIntegerField(_('items in stock'), null=True, default=1)
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    is_featured = models.BooleanField(_("product promotion"), default=False, null=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, null=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)
    # is_digital = models.BooleanField(_("digital product"), default=False)
    # digital_product = models.FileField(upload_to='digital-product/', blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse('store:product-detail', args=[self.slug])

    def __str__(self):
        return self.product_name


class ProductSpecificationValue(models.Model):
    """
    The Product Specification Value table holds each of the
    products individual specification .
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_spec_value')
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Product specification value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    The Product Image table.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a product image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


#blog tables
class BlogPost(models.Model):
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(null=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, related_name='blog_cats')
    content = RichTextField(null=True)
    cover_img = models.ImageField(upload_to='blog_cover_img', null=True)
    author = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(
        verbose_name=_("blog visibility"),
        help_text=_("Change blog visibility"),
        default=True,
    )
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class BlogImage(models.Model):
    """
    The Product Image table.
    """

    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="blog_images")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a product image"),
        upload_to="blog_images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


#contact table
class About(models.Model):
    company_name = models.CharField(max_length=600, null=True, help_text="Name of your company")
    logo = models.ImageField(null=True, blank=True, upload_to='logo/')
    instagram_link = models.URLField(null=True, blank=True, help_text="link to your instagram")
    twitter_link = models.URLField(null=True, blank=True, help_text="link to your twitter")
    facebook_link = models.URLField(null=True, blank=True, help_text="link to your facebook")
    whatsapp_link = models.URLField(null=True, blank=True, help_text="link to your what's app")
    about_text = RichTextField(null=True, help_text="what is your company like?")
    phone_number = models.CharField(max_length=10, null=True, blank=True, help_text="your phone number")
    other_number = models.CharField(max_length=10, null=True, blank=True, help_text="other phone number")
    email = models.EmailField(null=True, blank=True, help_text="your email")
    address = models.CharField(max_length=300, blank=True, null=True)
    district = models.CharField(null=True, max_length=300, help_text="where are you based?")
    location = models.CharField(max_length=300, null=True, help_text="eg area 18")

    class Meta:
        verbose_name = _("About  Us")
        verbose_name_plural = _("About Us")

    def __str__(self):
        return 'do not add, just edit this one'