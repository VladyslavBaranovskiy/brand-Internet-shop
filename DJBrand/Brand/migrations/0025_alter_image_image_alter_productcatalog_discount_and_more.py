# Generated by Django 4.2 on 2023-06-19 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0024_alter_image_image_alter_productcatalog_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default=0, upload_to='product_images/', verbose_name='Фото'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productcatalog',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Якщо знижка є - введіть ціну, якщо немає то залиште 0', max_digits=8, null=True, verbose_name='Ціна зі знижкою'),
        ),
        migrations.AlterField(
            model_name='productcatalog',
            name='title',
            field=models.CharField(max_length=35, verbose_name='Назва товару'),
        ),
    ]
