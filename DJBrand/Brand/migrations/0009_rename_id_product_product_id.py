# Generated by Django 4.2 on 2023-06-14 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0008_alter_product_id_alter_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='id',
            new_name='product_id',
        ),
    ]