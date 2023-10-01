# Generated by Django 4.2 on 2023-06-13 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0005_product_alter_profile_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='name',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=0, upload_to='product_image/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.DeleteModel(
            name='Basket',
        ),
    ]
