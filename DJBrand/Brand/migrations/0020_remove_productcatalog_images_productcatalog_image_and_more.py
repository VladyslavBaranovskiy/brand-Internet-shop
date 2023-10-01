# Generated by Django 4.2 on 2023-06-16 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0019_remove_productcatalog_image_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcatalog',
            name='images',
        ),
        migrations.AddField(
            model_name='productcatalog',
            name='image',
            field=models.ImageField(default=1, upload_to='product_image/'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]