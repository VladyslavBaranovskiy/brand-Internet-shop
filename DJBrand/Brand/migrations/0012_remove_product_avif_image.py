# Generated by Django 4.2 on 2023-06-14 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0011_product_avif_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='avif_image',
        ),
    ]
