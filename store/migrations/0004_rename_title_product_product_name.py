# Generated by Django 4.1.1 on 2023-03-18 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_is_featured_alter_product_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='title',
            new_name='product_name',
        ),
    ]
