# Generated by Django 4.2 on 2023-06-14 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0014_rename_product_productcatalog'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcatalog',
            name='description_detail',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productcatalog',
            name='size',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
